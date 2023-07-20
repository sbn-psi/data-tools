#!/usr/bin/env python3
import argparse
import sys
import csv

COLUMN_ATTRIBUTES = ('NAME', 'BYTES', 'DATA_TYPE', 'START_BYTE', 'OFFSET', 'UNIT', 'ITEMS', 'ITEM_BYTES')


def read_one_csv_row(filename) -> dict:
    with open(filename) as f:
        d = csv.DictReader(f)
        return d.__next__()


def write_columndefs(columndefs, filename):
    with open(filename, 'w') as f:
        w = csv.DictWriter(f, COLUMN_ATTRIBUTES)
        w.writeheader()
        w.writerows(columndefs)


def extract_columndef(prefix, column_name, row):
    return dict([(x, row.get(f'{prefix}{column_name}.{x}', '')) for x in COLUMN_ATTRIBUTES])


def extract_columndefs(prefix, filename):
    row = read_one_csv_row(filename)
    fields = row.keys()
    column_fields = [x.removeprefix(prefix) for x in fields if x.startswith(prefix)]
    column_names = set([x.split('.')[0] for x in column_fields])
    return [extract_columndef(prefix, column_name, row) for column_name in column_names]


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--input-file", default="out.csv",
                           help="The input file. This should be the output of `pds3tocsv.py`. Defaults to `out.csv`.")
    argparser.add_argument("--output-file", default="columns.csv",
                           help="The table of column definitions to write to. Defaults to `columns.csv`.")
    argparser.add_argument("--object-name", default="TABLE",
                           help="The name of the data object to traverse. Defaults to `TABLE`.")
    argparser.add_argument("--columns-name", default="COLUMN",
                           help="The type of object underneath the data object to traverse. Defaults to `COLUMNS`.")
    args = argparser.parse_args()

    prefix = f'{args.object_name}.{args.columns_name}.'
    columndefs = extract_columndefs(prefix, args.input_file)
    write_columndefs(sorted(columndefs, key=lambda x: int(x['START_BYTE'])), args.output_file)


if __name__ == '__main__':
    sys.exit(main())