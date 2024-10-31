#! /usr/bin/env python3
"""
Handles processing inventory files. This includes reading, writing,
and merging inventories.
"""
import argparse
import sys
import re

import inventory

RECORDS_REGEX = r"\<records\>\d*\<\/records\>"


def main():
    parser = argparse.ArgumentParser(description='Merge together PDS4 collection inventory files')
    parser.add_argument('files', nargs='+', help='The inventory files to merge together')
    parser.add_argument('--output', help='The destination file')
    parser.add_argument('--labelsrc', help='The input label file')
    parser.add_argument('--labeldest', help='The output label file')
    args = parser.parse_args()

    invs = [open(infile).readlines() for infile in args.files]
    merged = invmerge(max, *invs)
    contents = '\r\n'.join(sorted(merged)) + '\r\n'

    records = len(merged)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(contents)
    else:
        print(contents)

    if args.labelsrc and args.labeldest:
        update_label_count(args.labelsrc, args.labeldest, records)


def update_label_count(labelsrc, labeldest, record_count):
    with open(labelsrc) as infile:
        contents = infile.read()
    new_contents = re.sub(RECORDS_REGEX, "<records>{}</records>".format(record_count), contents)
    with open(labeldest, "w") as outfile:
        outfile.write(new_contents)
        

def invmerge(win_func, *invs):
    """
    Merge two inventories together, using win_func to pick the version that wins
    """
    dicts = [inventory.inventory_to_dict(inv) for inv in invs]
    keys = set().union(*[set(d.keys()) for d in dicts])
    
    merged = dict(
        [(key, fetch(win_func, key, *dicts)) for key in keys])

    return [member_type + ',' + lid + '::' + vid for (lid, (vid, member_type)) in merged.items()]


def fetch(func, key, *dicts):
    """
    Get the value associated with the key for each dictionary, then use func to select
    one.
    """
    return func(x[key] for x in dicts if key in x)


if __name__ == "__main__":
    sys.exit(main())
