#!/usr/bin/env python3

import argparse
import sys
import os.path


def read_headers(file_name):
    """
    Read the entire header from an IMG file.
    """
    lines = []
    with open(file_name, 'rb') as infile:
        while True:
            line = str(infile.readline(), encoding='utf-8').strip()
            lines.append(line)
            if line == 'END':
                return lines


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
