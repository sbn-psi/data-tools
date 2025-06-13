#!/usr/bin/env python3

import argparse
import sys
import os.path

def read_headers(file_name):
    '''
    Read the entire header from an IMG file.
    '''
    lines = []
    print(file_name)
    with open(file_name, 'rb') as infile:
        while True:
            line = str(infile.readline(), encoding='utf-8').strip()
            lines.append(line)
            print(line)
            if line == 'END':
                return lines
            
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs='+', help="The filename of the file to convert")
    args = parser.parse_args()

    for filename in args.filename:
        base, ext = os.path.splitext(filename)
        if ext == '.img':
            outfile =  base + ".lbl"
            contents = read_headers(filename)
            with open(outfile, "w") as f:
                f.write('\r\n'.join(contents))


if __name__ == '__main__':
    sys.exit(main())
