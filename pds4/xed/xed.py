#!/usr/bin/env python
import sys
import argparse
import shutil
import json

from lxml import etree


def replace(elements, args):
    for e in elements:
        e.text = args["value"]


def insert_text(elements, args, nsid=None):
    require(args, "name")
    for e in elements:
        n = text_element(args["name"], args.get("value"), nsid)
        e.append(n)


def insert_xml(elements, args):
    require(args, "value")
    for e in elements:
        n = xml_element(args["value"])
        e.append(n)


def insert_text_after(elements, args, nsid=None):
    require(args, "name", "value")
    for e in elements:
        parent = e.find("..")
        idx = parent.index(e)
        n = text_element(args["name"], args["value"], nsid)
        parent.insert(idx + 1, n)


def insert_xml_after(elements, args):
    require(args, "value")
    for e in elements:
        parent = e.find("..")
        idx = parent.index(e)
        n = xml_element(args["value"])
        parent.insert(idx + 1, n)


def delete(elements, _):
    for e in elements:
        e.find("..").remove(e)


def empty(elements, _):
    for e in elements:
        for s in e:
            e.remove(s)


def text_element(name, value=None, nsid=None):
    n = etree.Element(element_name(name, nsid))
    if value:
        n.text = value
    return n


def xml_element(value=None):
    n = etree.XML(value)
    return n


def element_name(name, nsid=None):
    _ns = "{" + (NSMAP[nsid] if nsid is not None else NSMAP["pds"]) + "}"
    return f'{_ns}{name}'


def ns(nsid, mission=False, version=1):
    mission_interfix = "mission/" if mission else ""
    return nsid, f'http://pds.nasa.gov/pds4/{mission_interfix}{nsid}/v{version}'


def require(args, *params):
    for param in params:
        if not param in args:
            raise Exception(f"Missing parameter: {param}")


def process_command(xmldoc, args):
    require(args, "command", "path")

    f = FUNCS[args["command"]]
    elements = xmldoc.xpath(args["path"], namespaces=NSMAP)

    f(elements, args)


def process_json(xmldoc, jsonfile):
    with open(jsonfile) as jsoninput:
        cmds = json.load(jsoninput)
        for cmd in cmds:
            process_command(xmldoc, cmd)


DICTIONARIES=("pds", "cart", "disp", "ebt", "geom", "img", "img_surface", "ml", "msn", "msn_surface", "msss_cam_nh",
              "multi", "nucspace", "particle", "proc", "radar", "rings", "sb", "speclib", "sp", "survey")

MISSION_DICTIONARIES=("apollo", "cassini", "chan1", "clementine", "clipper", "clps", "dawn", "hyb2", "hst", "insignt",
                      "juno", "kplo", "ladee", "lro", "mgn", "mars20202", "mvn", "mer", "mess", "mro", "msl", "near",
                      "nh", "ody", "orex", "vikinglander", "vg1", "vg2", "vgr")

FUNCS = dict((x.__name__, x) for x in [replace, insert_xml, insert_text, insert_text_after, insert_xml_after,
                                       delete, empty])

NSMAP = dict([ns(n) for n in DICTIONARIES] + [ns(n, mission=True) for n in MISSION_DICTIONARIES])


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

    filenames = args.filename if args.filename else ['-']

    for filename in filenames:
        xmldoc: etree = etree.parse(filename)

        if args.command:
            process_command(xmldoc, vars(args))
        if args.json:
            process_json(xmldoc, args.json)

        if args.inplace and not filename == "-":
            bakfile = filename + ".bak"
            shutil.copy(filename, bakfile)
            with open(filename, "w") as outfile:
                outfile.write(etree.tostring(xmldoc, method="xml", encoding="unicode"))
        else:
            print(etree.tostring(xmldoc, method="xml", encoding="unicode"))


if __name__ == "__main__":
    sys.exit(main())