#!/usr/bin/env python3

import sys

import preflight
import product

def main():
    files = sys.argv[1:]
    products = (product.Product(f) for f in files)
    passing = preflight.preflight_products(products)
    print("\n".join([f"{p.labelfilename} : OK" for p in passing]))


if __name__ == "__main__":
    sys.exit(main())
