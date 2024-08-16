#!/usr/bin/env python
import sys
import argparse
import shutil

from lxml import etree


DICTIONARIES=("pds", "cart", "disp", "ebt", "geom", "img", "img_surface", "ml", "msn", "msn_surface", "msss_cam_nh",
              "multi", "nucspace", "particle", "proc", "radar", "rings", "sb", "speclib", "sp", "survey")

MISSION_DICTIONARIES=("apollo", "cassini", "chan1", "clementine", "clipper", "clps", "dawn", "hyb2", "hst", "insignt",
                      "juno", "kplo", "ladee", "lro", "mgn", "mars20202", "mvn", "mer", "mess", "mro", "msl", "near",
                      "nh", "ody", "orex", "vikinglander", "vg1", "vg2", "vgr")


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
        n = element(name, nsmap, value, nsid)
        e.append(n)


def insert_after(xmldoc, nsmap, args):
    do_insert_after(xmldoc, nsmap, args.path, args.name, args.value)


def do_insert_after(xmldoc, nsmap, path, name, value, nsid=None):
    elements = xmldoc.xpath(path, namespaces=nsmap)

    for e in elements:
        parent = e.find("..")
        idx = parent.index(e)
        n = element(name, nsmap, value, nsid)
        parent.insert(idx+1, n)


def delete(xmldoc, nsmap, args):
    do_delete(xmldoc, nsmap, args.path)


def do_delete(xmldoc, nsmap, path):
    elements = xmldoc.xpath(path, namespaces=nsmap)
    for e in elements:
        e.find("..").remove(e)


def empty(xmldoc, nsmap, args):
    do_empty(xmldoc, nsmap, args.path)


def do_empty(xmldoc, nsmap, path):
    elements = xmldoc.xpath(path, namespaces=nsmap)
    for e in elements:
        for s in e:
            e.remove(s)


def element(name, nsmap, value=None, nsid=None):
    n = etree.Element(element_name(name, nsmap, nsid))
    if value:
        n.text = value
    return n


def element_name(name, nsmap, nsid=None):
    _ns = "{" + (nsmap[nsid] if nsid is not None else nsmap["pds"]) + "}"
    return f'{_ns}{name}'


def ns(nsid, mission=False, version=1):
    mission_interfix = "mission/" if mission else ""
    return nsid, f'http://pds.nasa.gov/pds4/{mission_interfix}{nsid}/v{version}'


FUNCS = dict((x.__name__, x) for x in [replace, insert_text, insert_after, delete, empty])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", required=True)
    parser.add_argument("--path")
    parser.add_argument("--name")
    parser.add_argument("--value")
    parser.add_argument("--inplace", action="store_true")
    parser.add_argument("filename", nargs='+')

    args = parser.parse_args()
    nsmap = dict([ns(n) for n in DICTIONARIES] + [ns(n, mission=True) for n in MISSION_DICTIONARIES])

    for filename in args.filename:
        xmldoc: etree = etree.parse(filename)
        f = FUNCS[args.command]
        f(xmldoc, nsmap, args)
        if args.inplace and not filename == "-":
            bakfile = filename + ".bak"
            shutil.copy(filename, bakfile)
            with open(filename, "w") as outfile:
                outfile.write(etree.tostring(xmldoc, method="xml", encoding="unicode"))
        else:
            print(etree.tostring(xmldoc, method="xml", encoding="unicode"))


if __name__ == "__main__":
    sys.exit(main())