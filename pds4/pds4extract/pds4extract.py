#!/usr/bin/env python3
from lib2to3.pgen2.token import NAME
import sys
import argparse
import csv
from typing import Dict
#import xml.etree
from lxml import etree


DISCIPLINE_ABBREVIATIONS = ["pds", "cart", "disp", "ebt", "geom", "img", "img_surface", "ml", "msn", "msn_surface", "msss_cam_mh", "multi", "nucspec", "particle", "proc", "radar", "rings", "speclib", "sp", "survey"]
DISCIPLINE_NAMESPACES= dict((a, f"http://pds.nasa.gov/pds4/{a}/v1") for a in DISCIPLINE_ABBREVIATIONS)
NAMESPACES = DISCIPLINE_NAMESPACES

DEFAULT_PATHS = {
    "lid": "/pds:Product_Observational/pds:Identification_Area/pds:logical_identifier",
    "vid": "/pds:Product_Observational/pds:Identification_Area/pds:version_id",
    "title": "/pds:Product_Observational/pds:Identification_Area/pds:title",
    "startdate": "/pds:Product_Observational/pds:Observation_Area/pds:Time_Coordinates/pds:start_date_time",
    "stopdate": "/pds:Product_Observational/pds:Observation_Area/pds:Time_Coordinates/pds:stop_date_time",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-filename", action="store_true")
    parser.add_argument("--spec")
    parser.add_argument("labels", nargs="+")

    args = parser.parse_args()
    
    paths = extract_paths(args.spec) if args.spec else DEFAULT_PATHS
    result = (extract_xml(label, paths, args.include_filename) for label in args.labels)

    w = csv.DictWriter(sys.stdout, fieldnames=get_keys(paths, args.include_filename))
    w.writeheader()
    w.writerows(result)

def extract_paths(specfile):
    with open(specfile) as f:
        r = csv.DictReader(f, fieldnames=["name", "path"])
        return dict((row["name"], row["path"]) for row in r)

def get_keys(paths, include_filename):
    keys = list(paths.keys())
    return ["filename"] + keys if include_filename else keys

def extract_xml(filename, paths, include_filename):
    doc = etree.parse(filename)
    result = extract_values(doc, paths)
    if (include_filename):
        result["filename"] = filename

    return result

def extract_values(doc, paths:Dict):
    return dict((name, extract_value(doc, path)) for (name, path) in paths.items())

def extract_value(doc, path):
    return ";".join(x.text for x in doc.xpath(path, namespaces=NAMESPACES))

if __name__ == '__main__':
    sys.exit(main())