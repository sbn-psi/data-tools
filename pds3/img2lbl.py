#!/usr/bin/env python3

import argparse
import itertools
import sys
import os.path


def read_headers(file_name):
    """
    Read the entire header from an IMG file.
    """
    with open(file_name, 'rb') as infile:
        lines = (str(x, encoding='utf-8').strip() for x in infile)
        return list(itertools.chain(itertools.takewhile(lambda x: x != 'END', lines), ['END']))


def extract_label(filename):
    """
    Extract the label from an img file and save it as an lbl file.
    """
    base, ext = os.path.splitext(filename)
    if ext == '.img':
        outfile = base + ".lbl"
        contents = read_headers(filename)
        with open(outfile, "w") as f:
            f.write('\r\n'.join(contents))


def main():
    parser = argparse.ArgumentParser(description=
                                     "Extracts the attached PDS3 label from an img "
                                     "file and saves it as a detached label ")
    parser.add_argument("filename", nargs='+', help="The filename of the file to convert")
    args = parser.parse_args()

    for filename in args.filename:
        extract_label(filename)


if __name__ == '__main__':
    sys.exit(main())
