#! /usr/bin/env python3
import argparse
import sys
import datetime
import sqlite3

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instrument', required=True)
    parser.add_argument('--loc', required=True)
    parser.add_argument('--proclevel', required=True)
    parser.add_argument('filename')
    args = parser.parse_args()

    parsed = (parse_line(line, args.instrument, args.loc) for line in open(args.filename))
    ready_to_insert = ((args.instrument, args.loc, args.proclevel) + line for line in parsed)

    c = sqlite3.connect('checksums.sqlite')
    c.executemany("insert into element values(?,?,?,?,?,?,?,?,?)", ready_to_insert)
    c.commit()


def parse_line(line, instrument, loc):
    filename, component, local_id, sha256sum = line.strip().split(";")
    datestr = filename.split("_")[0]
    dateval = datetime.datetime.strptime(datestr, "%Y%m%dT%H%M%SS%f")
    stamp = round(dateval.timestamp()*1000)

    return (filename, dateval, stamp, component, local_id, sha256sum)

if __name__ == '__main__':
    sys.exit(main())