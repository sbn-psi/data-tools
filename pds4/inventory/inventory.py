import itertools
import os
import xml.etree.ElementTree


def get_product_filenames(dirname):
    files = itertools.chain.from_iterable(
        (os.path.join(path, filename) for filename in filenames) for (path,_,filenames) in os.walk(dirname) if not 'SUPERSEDED' in path
    )
    files = (x for x in files if _is_product(x))
    return files

def _is_product(filename):
    basename = os.path.basename(filename)
    return filename.endswith('.xml') and not extract_product_type(filename) in ('Product_Collection','Product_Bundle')


def extract_product_type(filename):
    for (_, elem) in xml.etree.ElementTree.iterparse(filename):
        if elem.tag.startswith("{http://pds.nasa.gov/pds4/pds/v1}Product"):
            return elem.tag.replace("{http://pds.nasa.gov/pds4/pds/v1}","")


def iter_extract_lidvid(filename):
    lid=""
    for (event, elem) in xml.etree.ElementTree.iterparse(filename):
        #print (elem.text)
        if elem.tag=="{http://pds.nasa.gov/pds4/pds/v1}logical_identifier":
            lid=elem.text
        if elem.tag=="{http://pds.nasa.gov/pds4/pds/v1}version_id":
            return lid + "::" + elem.text


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
