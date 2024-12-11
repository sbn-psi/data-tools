#! /usr/bin/env python3

import sys
import argparse
import inventory


def main():
    parser = argparse.ArgumentParser(description='Validate a PDS4 collection inventory against the directory')
    parser.add_argument('--inventory', help='The inventory file', required=True)
    parser.add_argument('--directory', help='The directory with the products', required=True)
    args = parser.parse_args()

    provided_inventory = read_inventory(args.inventory)
    primary_lidvids = set(k + "::" + provided_inventory[k][0]
                          for k in provided_inventory.keys() if provided_inventory[k][1] == 'P')
    all_lidvids = set(k + "::" + provided_inventory[k][0]
                      for k in provided_inventory.keys())

    filenames = inventory.get_basic_product_filenames(args.directory, False)
    discovered_lidvids = set(inventory.extract_lidvid(filename) for filename in filenames)

    print("Discovered, but not in inventory:")
    for x in discovered_lidvids - all_lidvids:
        print(x) 

    print("In inventory, but not discovered:")
    for x in primary_lidvids - discovered_lidvids:
        print(x) 


def read_inventory(filename):
    with open(filename) as f:
        return inventory.inventory_to_dict(f.readlines())


if __name__ == "__main__":
    sys.exit(main())
