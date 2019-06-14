#! /usr/bin/env python3
'''
Handles processing inventory files. This includes reading, writing,
and merging inventories.
'''
import os
import iotools
import argparse
import sys

INVENTORY_FILENAME_TEMPLATE = 'collection_{collection_id}_{major}.{minor}.csv'

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(description='Merge together PDS4 collection inventory files')
    parser.add_argument('files', nargs='+', help='The inventory files to merge together')
    parser.add_argument('--output', help='The destination file')
    args = parser.parse_args()

    invs = [open(infile).readlines() for infile in args.files]
    merged = invmerge(max, *invs)
    contents = '\r\n'.join(sorted(merged)) + '\r\n'
    if (args.output):
        with open(args.output, 'w') as f:
            f.write(contents)
    else:
        print(contents)

def invmerge(win_func, *invs):
    '''
    Merge two inventories together, using win_func to pick the version that wins
    '''
    dicts = [inventory_to_dict(inv) for inv in invs]
    keys = set().union(*[set(d.keys()) for d in dicts])
    
    merged = dict(
        [(key, fetch(win_func, key, *dicts)) 
        for key in keys])

    return [member_type + ',' + lid + '::' + vid for (lid, (vid, member_type)) in merged.items()]

def fetch(func, key, *dicts):
    '''
    Get the value associated with the key for each dictionary, then use func to select
    one.
    '''
    return func(x[key] for x in (dicts) if key in x)

def inventory_to_dict(inventory):
    '''
    Convert a list of inventory lines to a dictionary of LID to (VID, member_type)
    '''
    return dict(invline_to_tuple(x) for x in inventory)

def invline_to_tuple(invline):
    '''
    Convert an inventory line to a tuple of (LID, (VID, member_type))
    '''
    member_type, lidvid = [x.strip() for x in invline.split(',')]
    lid, vid = [x.strip() for x in lidvid.split('::')]
    return (lid, (vid, member_type))

if __name__ == "__main__":
    sys.exit(main())