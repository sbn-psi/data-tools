#!/usr/bin/env python3

import argparse
from os.path import basename
import sys
import os
import os.path
import itertools
import re

NEW_HEADER='''<?xml-model href="https://pds.nasa.gov/pds4/pds/v1/PDS4_PDS_1F00.sch" schematypens="http://purl.oclc.org/dsdl/schematron"?>
<?xml-model href="https://pds.nasa.gov/pds4/img/v1/PDS4_IMG_1F00_1810.sch" schematypens="http://purl.oclc.org/dsdl/schematron"?>
<?xml-model href="https://pds.nasa.gov/pds4/geom/v1/PDS4_GEOM_1F00_1910.sch" schematypens="http://purl.oclc.org/dsdl/schematron"?>
<?xml-model href="https://pds.nasa.gov/pds4/disp/v1/PDS4_DISP_1F00_1500.sch" schematypens="http://purl.oclc.org/dsdl/schematron"?>
<Product_Observational xmlns="http://pds.nasa.gov/pds4/pds/v1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:img="http://pds.nasa.gov/pds4/img/v1" xmlns:geom="http://pds.nasa.gov/pds4/geom/v1" xmlns:disp="http://pds.nasa.gov/pds4/disp/v1" xsi:schemaLocation="http://pds.nasa.gov/pds4/pds/v1 https://pds.nasa.gov/pds4/pds/v1/PDS4_PDS_1F00.xsd http://pds.nasa.gov/pds4/img/v1 https://pds.nasa.gov/pds4/img/v1/PDS4_IMG_1F00_1810.xsd http://pds.nasa.gov/pds4/geom/v1 https://pds.nasa.gov/pds4/geom/v1/PDS4_GEOM_1F00_1910.xsd http://pds.nasa.gov/pds4/disp/v1 https://pds.nasa.gov/pds4/disp/v1/PDS4_DISP_1F00_1500.xsd">'''

LOCAL_IDENTIFIERS=["primary_image","x_coordinate","y_coordinate","z_coordinate","latitude","longitude","Center_distance","incidence_angle","emission_angle","phase_angle","horizontal_pixel_scale","vertical_pixel_scale","slope","elevation","gravitational_acceleration","gravitational_potential"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('srcdir')
    parser.add_argument('destdir')
    args = parser.parse_args()
    
    process_directory(args.srcdir, args.destdir)

def process_directory(srcdir, destdir):
    srcfiles = sorted(find_files(srcdir))
    destfiles = sorted(find_files(destdir))
    filemap = mapfiles(srcfiles, destfiles)
    for destfile in filemap.keys():
        srcfile = filemap[destfile][0]
        new_contents = merge_discipline_area(srcfile, destfile)
        if new_contents:
            with open (destfile + ".new", "w") as f:
                f.write(new_contents)

def merge_discipline_area(srcfile, destfile):
    with open(srcfile) as f:
        src_contents = f.read()
    with open(destfile) as f:
        dest_contents = f.read()

    geometry_area = extract_geometry_area(src_contents)
    if geometry_area:
        new_geometry_area = "\n".join(replace_identifier_reference(geometry_area, "image", identifier) for identifier in LOCAL_IDENTIFIERS)
        newlabel = replace_header(inject_geometry_area(dest_contents, new_geometry_area))
        print(newlabel)
        return newlabel
    else:
        return None

def replace_header(contents):
    return re.sub("\<Product_Observational.*\>", NEW_HEADER, contents)

def replace_identifier_reference(value:str, old_reference, new_reference):
    old_str = "<local_identifier_reference>" + old_reference + "</local_identifier_reference>"
    new_str = "<local_identifier_reference>" + new_reference + "</local_identifier_reference>"
    return value.replace(old_str, new_str)

def inject_geometry_area(contents, geometry_area):
    return contents.replace("    </Discipline_Area>", geometry_area + "    </Discipline_Area>")

def extract_geometry_area(contents):
    if "<geom:Geometry>" in contents:
        discipline_contents = contents.split("<geom:Geometry>")[1].split("</geom:Geometry>")[0]
        return "      <geom:Geometry>" + discipline_contents + "</geom:Geometry>\n"
    return None
 
def mapfiles(srcfiles, destfiles):
    filemap = {}
    for destfile in destfiles:
        matchlist = [srcfile for srcfile in srcfiles if matches(srcfile, destfile)]
        filemap[destfile] = matchlist
    return filemap

def matches(srcfile, destfile):
    srcbase = basename(srcfile)
    destbase = basename(destfile)
    result = extract_met(srcbase) == extract_met(destbase)
    return result

def extract_met(filename):
    return filename.split('_')[1]

def find_files(dirname):
    return itertools.chain.from_iterable(append_filenames(dirname, filenames) for dirname, _, filenames in os.walk(dirname))
        
def append_filenames(dirname, filenames):
    return (os.path.join(dirname, filename) for filename in filenames if filename.endswith(".xml") and filename.startswith("st_"))

if __name__ == '__main__':
    sys.exit(main())