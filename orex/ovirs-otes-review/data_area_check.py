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
import base64
import struct

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", help="The path to the PDS4 label file.", required=True)
    parser.add_argument("--output", help="The path to the output CSV file.", required=True)
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
    names = x.find_all("name")
    exclude_bytes = []

    for y in names:
        if "sclk" in y.text:
            exclude_bytes.append(found_time(y))
    
    name = x.name
    offset = int(x.find("offset").text)
    local_identifier = get_local_identifier(x)
    size = get_size(x)
    record_length = get_record_length(x)
    records = get_records(x)
    
    checksum = get_checksum(data_file, offset, size, record_length, records, exclude_bytes)

    return {
        "section": "ModifiedComponent", 
        "offset":offset, 
        "local_identifier": local_identifier, 
        "size":size, 
        "sha-256": checksum
    }

def get_record_length(x):
    if x.find("record_length") != None:
        return int(x.find("record_length").text)
    else:
        return None

def get_records(x):
    if x.find("records") != None:
        return int(x.find("records").text)
    else:
        return None

def found_time(element):
    field_location = int(element.find_next("field_location").text)
    field_length = int(element.find_next("field_length").text)
    return {
        "start_byte": field_location,
        "end_byte": field_location + field_length
    }

'''
Calculates the checksum of a section of the file.
'''
def get_checksum(data_file, offset, size, record_length, records, exclude_bytes):
    start = None
    end = None

    m = hashlib.sha256()
    contents = data_file.read()
    with open('test.csv','w') as file:
        if records != None and record_length != None and len(exclude_bytes) > 0:
            # for index in exclude_bytes:
            #     if start == None or index["start_byte"] < start:
            #         start = index["start_byte"]
            #     if end == None or index["end_byte"] > end:
            #         end = index["end_byte"]

            section = contents[offset:offset+(records*record_length)] # because these are bytes!
            
            for i in range(0,len(section),record_length):
                record = section[i:i+record_length]
                fmt = '<IHHH' + ('f' * 349) + 'ff' + ('f' * 349)
                unpacked_record = struct.unpack(fmt , record)
                write_to_file(unpacked_record,file)
                line2 = record[:start] + record[end:]
                m.update(line2)
            return m.hexdigest()
        else:
            data_file.seek(offset)
            m.update(data_file.read(size))
            return m.hexdigest()

def write_to_file(line,file):
    file.write(str(line) + "\n")

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