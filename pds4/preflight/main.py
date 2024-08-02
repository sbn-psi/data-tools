#!/usr/bin/env python3

import sys

import preflight
import product


def main():
    files = sys.argv[1:]
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


if __name__ == "__main__":
    sys.exit(main())
