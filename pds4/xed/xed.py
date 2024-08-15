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

    for e in elements:
        n = etree.SubElement(e, element_name(name, nsmap, nsid))
        n.text = value


def element_name(name, nsmap, nsid=None):
    _ns = "{" + (nsmap[nsid] if nsid is not None else nsmap["pds"]) + "}"
    return f'{_ns}{name}'


def ns(nsid, mission=False, version=1):
    if mission:
        return nsid, f'http://pds.nasa.gov/pds4/mission/{nsid}/v{version}'
    else:
        return nsid, f'http://pds.nasa.gov/pds4/{nsid}/v{version}'


FUNCS = dict((x.__name__, x) for x in [replace, insert_text])


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
    f = FUNCS[args.command]
    f(xmldoc, nsmap, args)
    print(etree.tostring(xmldoc, method="xml", encoding="unicode"))


if __name__ == "__main__":
    sys.exit(main())