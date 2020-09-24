#! /usr/bin/env python3

import sys

def main(argv=None):
    if not argv:
        argv = sys.argv

    filename1 = argv[1]
    filename2 = argv[2]

    inventory1 = set(open(x.strip() for x in filename1).readlines)
    inventory2 = set(open(x.strip() for x in filename2).readlines)

    print ("Extras in: " + filename1)
    for x in inventory1 - inventory2:
        print(x)

    print("Extras in: " + filename2):
    for x in inventory2 - inventory1:
        print(X)

if __name__ == "__main__":
    sys.exit(main())