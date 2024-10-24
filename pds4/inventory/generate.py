#! /usr/bin/env python3

import sys
import inventory
import argparse
import logging
from multiprocessing import pool
from functools import partial

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("outfilepath")
    parser.add_argument("dirname")
    parser.add_argument("--deep-product-check", action='store_true')
    parser.add_argument("--logfile")
    parser.add_argument("--processes", type=int, default=1)

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        filename=args.logfile if args.logfile else None
    )

    build_inventory(args.dirname, args.outfilepath, args.deep_product_check, args.processes)

def build_inventory(dirname, outfilename, deep, processes):
    filenames = get_filenames(dirname, processes, deep)
    lidvids = sorted(get_lidvids(filenames, processes))
    records = ("P," + lidvid for lidvid in lidvids)

    with open(outfilename,"w") as f:
        for r in records:
            f.write(r + "\r\n")


def get_filenames(dirname, processes, deep):
    filenames = inventory.get_all_product_filenames(dirname)
    if processes == 1:
        return (x for x in filenames if inventory.is_product(x, deep=deep))
    else:
        with pool.Pool(processes=processes) as p:
            f = partial(squelch_collections, deep=deep)
            return (x for x in p.map(f, filenames) if x is not None)


def squelch_collections(filename, deep):
    if inventory.is_product(filename, deep=deep):
        return filename
    return None


def get_lidvids(filenames, processes):
    if processes == 1:
        return (inventory.iter_extract_lidvid(filename, sink=logging.info) for filename in filenames)
    else:
        logging.warning("Logging will go to stdout during multiprocessing phase")
        with pool.Pool(processes=processes) as p:
            return p.map(inventory.iter_extract_lidvid, filenames)

if __name__ == '__main__':
    main()