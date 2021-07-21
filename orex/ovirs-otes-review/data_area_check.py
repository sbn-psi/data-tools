#!/usr/bin/env python3
'''
Gets the checksums for data products. Instead of simply getting the checksum for
each file, this script gets the checksum for each segment of the file,
as defined by the product label.
'''
import argparse
import bs4
import sys
import math
import hashlib
import os.path
import operator
import functools


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", help="", required=True)
    args = parser.parse_args()
    label_dir = os.path.dirname(args.label)
    
    with open(args.label) as label_file:
        label = bs4.BeautifulSoup(label_file, "lxml-xml")

    if label.find("Product_Observational"):
        file_area = label.find("File_Area_Observational")
        data_file_name = label.find("File").find("file_name").text
        segments = [x for x in file_area if x.name and not x.name == 'File']

        with open(os.path.join(label_dir, data_file_name), 'rb') as data_file:
            for x in segments:
                segment = analyze_segment(x, data_file)
                cprint(os.path.basename(args.label), segment["section"], segment["local_identifier"], segment["sha-256"])

'''
Prints a list of elements, delimited with a semicolon.
'''
def cprint(*args):
    print(";".join(str(x) for x in args))

'''
Compiles the information about a specific part of the product.

x is the xml element that describes the part of the product (such as a specific header or table entry)
'''
def analyze_segment(x, data_file):
    name = x.name
    offset = int(x.find("offset").text)
    local_identifier = get_local_identifier(x)
    size = get_size(x)

    checksum = get_checksum(data_file, offset, size)

    return {
        "section": name, 
        "offset":offset, 
        "local_identifier": local_identifier, 
        "size":size, 
        "sha-256": checksum
    }

'''
Calculates the checksum of a section of the file.
'''
def get_checksum(data_file, offset, size):
    if size:
        data_file.seek(offset)
        m = hashlib.sha256()
        m.update(data_file.read(size))
        return m.hexdigest()
    return None

'''
Gets the value of the local_identifier attribute for a component of the product,
if it exists.
'''
def get_local_identifier(element):
    local_identifier = element.find("local_identifier")
    return local_identifier.text if local_identifier else None

'''
Calculate the size of a section of the file. This uses a jump table to choose
the correct sizing function.
'''
def get_size(element):
    if element.name in SIZE_FUNCS:
        return SIZE_FUNCS[element.name](element)
    return None

'''
Gets the size of a header area
'''
def get_header_size(element):
    return int(element.find("object_length").text)


'''
Gets the size of a binary table
'''
def get_table_binary_size(element):
    records = int(element.find("records").text)
    record_length = int(element.find("Record_Binary").find("record_length").text)
    return records * record_length

'''
Gets the size of an Array_*D element.
'''
def get_array_size(element):
    axes = [int(x.find("elements").text) for x in element.find_all("Axis_Array")]
    data_type = element.find("Element_Array").find("data_type").text
    data_size = DATA_SIZES[data_type]
    return data_size * functools.reduce(operator.mul, axes, 1)

SIZE_FUNCS = {
    "Header": get_header_size,
    "Table_Binary": get_table_binary_size,
    "Array_3D": get_array_size,
    "Array_2D": get_array_size,
    "Array_2D_Spectrum": get_array_size,

}

DATA_SIZES = {
    "UnsignedMSB2": 2,
    "SignedMSB4": 4,
    "IEEE754MSBDouble": 8

}


if __name__ == "__main__":
    sys.exit(main())