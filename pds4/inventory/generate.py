#! /usr/bin/env python3

import sys
import inventory
import argparse
import logging

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("outfilepath")
    parser.add_argument("dirname")
    parser.add_argument("--deep-product-check", action='store_true')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    build_inventory(args.dirname, args.outfilepath, args.deep_product_check)

def build_inventory(dirname, outfilename, deep):
    filenames = inventory.get_product_filenames(dirname, deep=deep)
    lidvids = sorted(inventory.iter_extract_lidvid(filename) for filename in filenames)
    records = ("P," + lidvid for lidvid in lidvids)

    with open(outfilename,"w") as f:
        for r in records:
            f.write(r + "\r\n")

if __name__ == '__main__':
    main()