#! /usr/bin/env python3

import inventory
import argparse
import logging
from multiprocessing import pool
from functools import partial


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("outfilepath")
    parser.add_argument("dirname")
    parser.add_argument("--deep-product-check", action='store_true')
    parser.add_argument("--logfile")
    parser.add_argument("--debug", action='store_true')
    parser.add_argument("--quiet", action='store_true')
    parser.add_argument("--tolerant", action='store_true')
    parser.add_argument("--processes", type=int, default=1)

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.WARNING if args.quiet else logging.DEBUG if args.debug else logging.INFO,
        filename=args.logfile
    )

    p = pool.Pool(processes=args.processes) if args.processes > 1 else None
    build_inventory(args.dirname, args.outfilepath, args.deep_product_check, args.tolerant, p)


def build_inventory(dirname, outfilename, deep, tolerant, pool_):
    filenames = peeks(get_filenames(dirname, pool_, deep), logging.DEBUG)
    lidvids = peeks(get_lidvids(filenames, pool_, tolerant), logging.INFO)
    records = ("P," + lidvid for lidvid in lidvids)

    with open(outfilename, "w") as f:
        for r in sorted(records):
            f.write(r + "\r\n")


def get_filenames(dirname, processes, deep):
    filenames = inventory.get_all_product_filenames(dirname)
    func = partial(squelch_collections, deep=deep)
    return (x for x in do_map(func, filenames, processes) if x is not None)


def squelch_collections(filename, deep):
    if inventory.is_product(filename, deep=deep):
        return filename
    return None


def get_lidvids(filenames, pool_, tolerant):
    func = partial(inventory.iter_extract_lidvid, tolerant=tolerant)
    return do_map(func, filenames, pool_)


def do_map(func, items, pool_):
    if pool_ is None:
        return (func(x) for x in items)
    else:
        return pool_.imap_unordered(func, items, 1024)


def peeks(items, level):
    return (peek(x, level) for x in items)


def peek(x, level):
    logging.log(level, x)
    return x


if __name__ == '__main__':
    main()
