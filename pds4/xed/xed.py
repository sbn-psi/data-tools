#!/usr/bin/env python
import sys
import argparse
from lxml import etree


def replace(xmldoc, nsmap, args):
    print("replace", args, file=sys.stderr)
    do_replace(xmldoc, nsmap, args.path, args.value)


def do_replace(xmldoc: etree, nsmap, path, value):
    print("replace", path, value, file=sys.stderr)
    elements = xmldoc.xpath(path, namespaces=nsmap)

    if not elements:
        print("Could not find element at path: " + path, file=sys.stderr)
    else:
        print(f"{len(elements)} elements found")

    for e in elements:
        e.text = value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", required=True)
    parser.add_argument("--path")
    parser.add_argument("--value")
    parser.add_argument("filename")

    args = parser.parse_args()
    nsmap = {"pds": "http://pds.nasa.gov/pds4/pds/v1"}

    xmldoc: etree = etree.parse(args.filename)
    if args.command == "replace":
        replace(xmldoc, nsmap, args)

    print(etree.tostring(xmldoc, method="xml", encoding="unicode"))


if __name__ == "__main__":
    sys.exit(main())