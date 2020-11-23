#! /usr/bin/env python3
from jinja2 import Environment, FileSystemLoader, select_autoescape

import json
import os
import sys
import argparse

ENVIRONMENT=Environment(loader=FileSystemLoader('templates'), lstrip_blocks=True, trim_blocks=True)
DOCUMENT_TEMPLATE=ENVIRONMENT.get_template("document.xml.jinja")

def main():
    parser = build_parser()
    args = parser.parse_args()

    bundles = json.load(open(args.bundle_file))
    bundle = bundles[0]
    document_filename = os.path.basename(args.document_file)
    document_extension = document_filename.split(".")[-1]
    product_id = "urn:nasa:pds:" + bundle["bundle_id"] + ":document:" + filename_to_id(document_filename)
    label_filename = args.document_file.replace(document_extension, "xml")
    
    with open(label_filename, "w") as output_file:
        output_file.write(DOCUMENT_TEMPLATE.render(bundle=bundle, 
                                                 product_title=args.product_title, 
                                                 author_list=args.author_list,
                                                 description=args.description,
                                                 modification_date=args.modification_date,
                                                 publication_date=args.publication_date,
                                                 file_name=document_filename,
                                                 product_id=product_id))

def build_parser():
    parser = argparse.ArgumentParser(description='Validate a PDS4 collection inventory against the directory')
    parser.add_argument('--bundle-file', dest='bundle_file', help='The JSON file that describes the bundle', required=True)
    parser.add_argument('--document-file', dest='document_file', help='The document file to label', required=True)
    parser.add_argument('--modification-date', dest='modification_date', help='If enabled, will not preprocess the data and label files', required=True)
    parser.add_argument('--publication-date', dest='publication_date', help='If enabled, will not validate the data', required=True)
    parser.add_argument('--product-title', dest='product_title', help='If enabled, will not validate the data', required=True)
    parser.add_argument('--description', dest='description', help='If enabled, will not move the data', required=True)
    parser.add_argument('--author-list', dest='author_list', help='If enabled, will not move the data', required=True)
    return parser

def filename_to_id(filename):
    return filename

if __name__ == "__main__":
    main()