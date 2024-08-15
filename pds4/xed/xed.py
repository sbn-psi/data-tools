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


def insert_after(xmldoc, nsmap, args):
    do_insert_after(xmldoc, nsmap, args.path, args.name, args.value)


def do_insert_after(xmldoc, nsmap, path, name, value, nsid=None):
    elements = xmldoc.xpath(path, namespaces=nsmap)

    for e in elements:
        n = etree.Element(element_name(name, nsmap, nsid))
        n.text = value
        parent = e.find("..")
        idx = parent.index(e)
        parent.insert(idx+1, n)


def element_name(name, nsmap, nsid=None):
    _ns = "{" + (nsmap[nsid] if nsid is not None else nsmap["pds"]) + "}"
    return f'{_ns}{name}'


def ns(nsid, mission=False, version=1):
    mission_interfix = "mission/" if mission else ""
    return nsid, f'http://pds.nasa.gov/pds4/{mission_interfix}{nsid}/v{version}'


FUNCS = dict((x.__name__, x) for x in [replace, insert_text, insert_after])


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