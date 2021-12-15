#! /usr/bin/env python3

import sys
import itertools
import os
import xml.etree.ElementTree
import inventory

def main(argv=None):
    if not argv:
        argv = sys.argv
    outfilepath = argv[1]
    dirname = argv[2]
    
    build_inventory(dirname, outfilepath)

def build_inventory(dirname, outfilename):
    filenames = inventory.get_product_filenames(dirname)
    lidvids = (inventory.iter_extract_lidvid(filename) for filename in filenames)
    records = ("P," + lidvid for lidvid in lidvids)

    with open(outfilename,"w") as f:
        for r in records:
            f.write(r + "\r\n")

if __name__ == '__main__':
    main()