#! /usr/bin/env python3

import sys
import inventory
import argparse
import logging

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("outfilepath")
    parser.add_argument("dirname")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    build_inventory(args.dirname, args.outfilepath)

def build_inventory(dirname, outfilename):
    filenames = inventory.get_product_filenames(dirname)
    lidvids = sorted(inventory.iter_extract_lidvid(filename) for filename in filenames)
    records = ("P," + lidvid for lidvid in lidvids)

    with open(outfilename,"w") as f:
        for r in records:
            f.write(r + "\r\n")

if __name__ == '__main__':
    main()