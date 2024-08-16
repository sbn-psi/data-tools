#!/usr/bin/env python
import sys
import argparse
import shutil
import json

from lxml import etree


DICTIONARIES=("pds", "cart", "disp", "ebt", "geom", "img", "img_surface", "ml", "msn", "msn_surface", "msss_cam_nh",
              "multi", "nucspace", "particle", "proc", "radar", "rings", "sb", "speclib", "sp", "survey")

MISSION_DICTIONARIES=("apollo", "cassini", "chan1", "clementine", "clipper", "clps", "dawn", "hyb2", "hst", "insignt",
                      "juno", "kplo", "ladee", "lro", "mgn", "mars20202", "mvn", "mer", "mess", "mro", "msl", "near",
                      "nh", "ody", "orex", "vikinglander", "vg1", "vg2", "vgr")


def replace(xmldoc, nsmap, args):
    require(args, "path")
    elements = xmldoc.xpath(args["path"], namespaces=nsmap)
    for e in elements:
        e.text = args["value"]


def insert_text(xmldoc, nsmap, args):
    require(args, "path", "name", "value")
    elements = xmldoc.xpath(args["path"], namespaces=nsmap)
    for e in elements:
        n = element(args["name"], nsmap, args["value"], None)
        e.append(n)


def insert_text_after(xmldoc, nsmap, args):
    require(args, "path", "name", "value")
    elements = xmldoc.xpath(args["path"], namespaces=nsmap)
    for e in elements:
        parent = e.find("..")
        idx = parent.index(e)
        n = element(args["name"], nsmap, args["value"], None)
        parent.insert(idx + 1, n)


def delete(xmldoc, nsmap, args):
    require(args, "path")
    elements = xmldoc.xpath(args["path"], namespaces=nsmap)
    for e in elements:
        e.find("..").remove(e)


def empty(xmldoc, nsmap, args):
    require(args, "path")
    elements = xmldoc.xpath(args["path"], namespaces=nsmap)
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


def require(args, *params):
    for param in params:
        if not param in args:
            raise Exception(f"Missing parameter: {param}")


FUNCS = dict((x.__name__, x) for x in [replace, insert_text, insert_text_after, delete, empty])


def process_command(xmldoc, nsmap, args):
    f = FUNCS[args["command"]]
    f(xmldoc, nsmap, args)


def process_json(xmldoc, nsmap, jsonfile):
    with open(jsonfile) as jsoninput:
        cmds = json.load(jsoninput)
        for cmd in cmds:
            process_command(xmldoc, nsmap, cmd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command")
    parser.add_argument("--path")
    parser.add_argument("--name")
    parser.add_argument("--value")
    parser.add_argument("--json")
    parser.add_argument("--inplace", action="store_true")
    parser.add_argument("filename", nargs='*')

    args = parser.parse_args()
    nsmap = dict([ns(n) for n in DICTIONARIES] + [ns(n, mission=True) for n in MISSION_DICTIONARIES])

    filenames = args.filename if args.filename else ['-']

    for filename in filenames:
        xmldoc: etree = etree.parse(filename)

        if args.command:
            process_command(xmldoc, nsmap, vars(args))
        if args.json:
            process_json(xmldoc, nsmap, args.json)

        if args.inplace and not filename == "-":
            bakfile = filename + ".bak"
            shutil.copy(filename, bakfile)
            with open(filename, "w") as outfile:
                outfile.write(etree.tostring(xmldoc, method="xml", encoding="unicode"))
        else:
            print(etree.tostring(xmldoc, method="xml", encoding="unicode"))


if __name__ == "__main__":
    sys.exit(main())