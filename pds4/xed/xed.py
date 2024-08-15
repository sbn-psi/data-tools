#!/usr/bin/env python
import sys
import argparse
from lxml import etree


def replace(xmldoc, nsmap, args):
    do_replace(xmldoc, nsmap, args.path, args.value)


def do_replace(xmldoc: etree, nsmap, path, value):
    print("replace", path, value, file=sys.stderr)
    elements = xmldoc.xpath(path, namespaces=nsmap)

    for e in elements:
        e.text = value


def insert_text(xmldoc, nsmap, args):
    do_insert_text(xmldoc, nsmap, args.path, args.name, args.value)


def do_insert_text(xmldoc, nsmap, path, name, value, nsid=None):
    elements = xmldoc.xpath(path, namespaces=nsmap)
    n = "{" + (nsmap[nsid] if nsid is not None else nsmap["pds"]) + "}"

    for e in elements:
        n = etree.SubElement(e, f'{n}{name}')
        n.text = value


def ns(nsid, version=1, mission=False):
    if mission:
        return nsid, f'http://pds.nasa.gov/pds4/mission/{nsid}/v{version}'
    else:
        return nsid, f'http://pds.nasa.gov/pds4/{nsid}/v{version}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", required=True)
    parser.add_argument("--path")
    parser.add_argument("--name")
    parser.add_argument("--value")
    parser.add_argument("filename")

    args = parser.parse_args()
    nsmap = dict([ns(n) for n in ["pds"]])

    print(nsmap, file=sys.stderr)

    xmldoc: etree = etree.parse(args.filename)
    if args.command == "replace":
        replace(xmldoc, nsmap, args)
    elif args.command == "insert_text":
        insert_text(xmldoc, nsmap, args)

    print(etree.tostring(xmldoc, method="xml", encoding="unicode"))


if __name__ == "__main__":
    sys.exit(main())