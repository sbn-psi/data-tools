import itertools
import os

import logging

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

logger = logging.getLogger(__name__)
NON_PRODUCT_FRAGMENTS=('bundle', 'collection')
NON_PRODUCT_ELEMENTS=('Product_Collection', 'Product_Bundle')


def get_all_product_filenames(dirname):
    return itertools.chain.from_iterable(
        (os.path.join(path, filename) for filename in filenames) for (path,_,filenames) in os.walk(dirname) if not 'SUPERSEDED' in path
    )


def get_product_filenames(dirname, deep):
    return (x for x in get_all_product_filenames(dirname) if is_product(x, deep))


def is_product(filename, deep=False):
    if deep:
        return filename.endswith('.xml') and not extract_product_type(filename) in NON_PRODUCT_ELEMENTS
    return filename.endswith('.xml') and not any(x in filename for x in NON_PRODUCT_FRAGMENTS)


def extract_product_type(filename):
    try:
        for (_, elem) in etree.iterparse(filename, events=['start']):
            tag = elem.tag
            if tag.startswith("{http://pds.nasa.gov/pds4/pds/v1}Product"):
                return tag.replace("{http://pds.nasa.gov/pds4/pds/v1}","")
        raise Exception(f"Could not find product type for: {filename}")
    except Exception as e:
        raise Exception(f"Could not parse product: {filename}") from e


def iter_extract_lidvid(filename):
    lid=""
    try:
        for (_, elem) in etree.iterparse(filename):
            if elem.tag=="{http://pds.nasa.gov/pds4/pds/v1}logical_identifier":
                lid=elem.text
            elif elem.tag=="{http://pds.nasa.gov/pds4/pds/v1}version_id":
                lidvid = lid + "::" + elem.text
                return lidvid
            elif elem.tag=="{http://pds.nasa.gov/pds4/pds/v1}Identification_Area":
                raise Exception(f"Missing LID or VID for: {filename}")
    except Exception as e:
        raise Exception(f"Could not parse product: {filename}") from e


def inventory_to_dict(inventory):
    '''
    Convert a list of inventory lines to a dictionary of LID to (VID, member_type)
    This will fail if there are duplicate LIDs in the inventory
    '''
    return dict(_invline_to_tuple(x) for x in inventory)

def _invline_to_tuple(invline):
    '''
    Convert an inventory line to a tuple of (LID, (VID, member_type))
    '''
    member_type, lidvid = [x.strip() for x in invline.split(',')]
    lid, vid = [x.strip() for x in lidvid.split('::')]
    return (lid, (vid, member_type))
