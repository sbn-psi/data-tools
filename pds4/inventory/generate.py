#! /usr/bin/env python3

from bs4 import BeautifulSoup
import sys
import itertools
import os

def main(argv=None):
    if not argv:
        argv = sys.argv
    outfilepath = argv[1]
    dirname = argv[2]
    
    build_inventory(dirname, outfilepath)

def build_inventory(dirname, outfilename):
    filenames = get_product_filenames(dirname)
    lidvids = [extract_lidvid(filename) for filename in filenames]
    records = ["P," + lidvid for lidvid in sorted(set(lidvids))]

    with open(outfilename,"w") as f:
        f.write("\r\n".join(records))

def get_product_filenames(dirname):
    files = itertools.chain.from_iterable(
        (os.path.join(path, filename) for filename in filenames) for (path,_,filenames) in os.walk(dirname)
    )
    files = [x for x in files if is_product(x)]
    return files

def is_product(filename):
    basename = os.path.basename(filename)
    return filename.endswith('.xml') and not basename.startswith('collection') and not basename.startswith('bundle')


def extract_lidvid(filename):
    with open(filename) as f:
        soup = BeautifulSoup(f, "lxml-xml")
    identification_area = soup.find("Identification_Area")
    lid = identification_area.logical_identifier.string
    vid = identification_area.version_id.string
    return lid + "::" + vid

if __name__ == '__main__':
    main()