#! /usr/bin/env python3
from jinja2 import Environment, FileSystemLoader, select_autoescape

import json
import os
import sys

ENVIRONMENT=Environment(loader=FileSystemLoader('templates'), lstrip_blocks=True, trim_blocks=True)
BUNDLE_TEMPLATE=ENVIRONMENT.get_template("bundle-dawn-grand.xml.jinja")
COLLECTION_TEMPLATE=ENVIRONMENT.get_template("collection.xml.jinja")

def main():
    bundle_file = sys.argv[1]
    if not bundle_file:
        sys.exit("No bundle file provided")
    bundles = json.load(open(bundle_file))

    for bundle in bundles:
        process_bundle(bundle)
        for collection in bundle["collections"]:
            process_collection(bundle, collection)

def process_bundle(bundle):
    bundle_id = bundle["bundle_id"]
    
    os.makedirs(bundle_id, exist_ok=True)

    bundle_output_path = os.path.join(bundle_id, "bundle_" + bundle_id + ".xml")
    with open(bundle_output_path, "w") as output_file:
        output_file.write(BUNDLE_TEMPLATE.render(**bundle))

def process_collection(bundle, collection):
    bundle_id = bundle["bundle_id"]
    collection_id = collection["collection_id"]
    collection_dir = build_collection_dir(bundle_id, collection_id)

    inventory_path = os.path.join(collection_dir, "collection_inventory_" + collection_id + ".csv")
    inventory_count = count_records(inventory_path)

    collection_output_path = os.path.join(collection_dir, "collection_" + collection_id + ".xml")
    with open(collection_output_path, "w") as output_file:
        output_file.write(COLLECTION_TEMPLATE.render(bundle=bundle, collection=collection, inventory_count=inventory_count))


def build_collection_dir(bundle_id, collection_id):
    collection_dir = os.path.join(bundle_id, collection_id)
    os.makedirs(os.path.join(bundle_id, collection_id), exist_ok=True)
    return collection_dir

def count_records(inventory_path):
    if os.path.exists(inventory_path):
        return len(open(inventory_path).readlines())
    return 0


if __name__ == "__main__":
    main()