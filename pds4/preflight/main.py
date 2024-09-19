#!/usr/bin/env python3

import sys
import os
import os.path
import itertools
from typing import Iterable

import preflight
import product


def main():
    params = sys.argv[1:]
    files = build_file_lists(params)
    products = (product.Product(f) for f in files)
    preflights = preflight.preflight_products(products)
    has_warnings = False
    for status in preflights:
        if status.messages:
            print(f"{status.candidate.labelfilename}: WARNING")
            print("\n".join(f"- {m}" for m in status.messages))
            has_warnings = True
        else:
            print(f"{status.candidate.labelfilename}: OK")

    if has_warnings:
        print("WARNINGs encountered")
        return 1
    else:
        print("All OK")
        return 0


def build_file_lists(params: Iterable[str]) -> Iterable[str]:
    return itertools.chain.from_iterable(build_file_list(f) for f in params)


def build_file_list(f: str) -> Iterable[str]:
    if os.path.isfile(f) and f.endswith('.xml'):
        return [f]
    elif os.path.isdir(f):
        return itertools.chain.from_iterable(
            (os.path.join(dirpath, filename) for filename in filenames if is_product_label(filename))
            for dirpath, _, filenames in os.walk(f)
        )
    else:
        raise Exception(f"Invalid parameter: {f}")


def is_product_label(filename):
    return filename.endswith('.xml') and 'collection' not in filename and 'bundle' not in filename


if __name__ == "__main__":
    sys.exit(main())
