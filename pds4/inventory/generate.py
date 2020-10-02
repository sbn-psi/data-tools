#! /usr/bin/env python3

from bs4 import BeautifulSoup
import sys
import itertools
import os
import xml.etree.ElementTree

def main(argv=None):
    if not argv:
        argv = sys.argv
    outfilepath = argv[1]
    dirname = argv[2]
    
    build_inventory(dirname, outfilepath)

def build_inventory(dirname, outfilename):
    filenames = get_product_filenames(dirname)
    lidvids = (iter_extract_lidvid(filename) for filename in filenames)
    records = ("P," + lidvid for lidvid in lidvids)

    with open(outfilename,"w") as f:
        for r in records:
            f.write(r + "\r\n")

def get_product_filenames(dirname):
    files = itertools.chain.from_iterable(
        (os.path.join(path, filename) for filename in filenames) for (path,_,filenames) in os.walk(dirname)
    )
    files = (x for x in files if is_product(x))
    return files

def is_product(filename):
    basename = os.path.basename(filename)
    return filename.endswith('.xml') and not basename.startswith('collection') and not basename.startswith('bundle')


def iter_extract_lidvid(filename):
    lid=""
    for (event, elem) in xml.etree.ElementTree.iterparse(filename):
        #print (elem.text)
        if elem.tag=="{http://pds.nasa.gov/pds4/pds/v1}logical_identifier":
            lid=elem.text
        if elem.tag=="{http://pds.nasa.gov/pds4/pds/v1}version_id":
            return lid + "::" + elem.text

if __name__ == '__main__':
    main()