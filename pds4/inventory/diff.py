#! /usr/bin/env python3

import sys

def main(argv=None):
    if not argv:
        argv = sys.argv

    filename1 = argv[1]
    filename2 = argv[2]

    inventory1 = set(open(filename1.strip()).readlines())
    inventory2 = set(open(filename2.strip()).readlines())

    print ("Extras in: " + filename1)
    for x in inventory1 - inventory2:
        print(x)

    print("Extras in: " + filename2)
    for x in inventory2 - inventory1:
        print(x)

if __name__ == "__main__":
    sys.exit(main())