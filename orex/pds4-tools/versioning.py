#!/usr/bin/env python3
'''
This script will incement the major version number of the specified products.
It is assumed that the version number in the label itself is correct, and the version
just needs to be added on to the filename.

Usage:

versioning.py <label_file>...
'''

import re
import os
import sys
from bs4 import BeautifulSoup

LABELFILE_PARSE_VERSIONED_REGEX = r'(.+)_(\d+)_(\d+)\.xml'
LABELFILE_PARSE_UNVERSIONED_REGEX = r'(.+)\.xml'

DATAFILE_PARSE_VERSIONED_REGEX = r'(.+)_(\d+)\.([a-z0-9]+)'
DATAFILE_PARSE_UNVERSIONED_REGEX = r'(.+)\.([a-z0-9]+)'

def main(argv=None):
    ''' Entry point into the script '''
    if argv is None:
        argv = sys.argv
    filepaths = argv[1:]

    for filepath in filepaths:
        dirname, filename = os.path.split(filepath)
        increment_product(dirname, filename)


def increment_product(path, labelfile):
    '''
    Increments the version number of the specified product
    '''
    label = read_label(path, labelfile)
    datafile = extract_datafile(label)

    new_labelfile = increment_labelfile(labelfile)

    if datafile:
        new_datafile = increment_datafile(datafile)
        contents = inject_datafile(label, datafile, new_datafile)
        with open(new_labelfile, "w") as outfile:
            outfile.write(contents)
        rename(path, datafile, new_datafile)
    else:
        rename(path, labelfile, new_labelfile)

def read_label(path, labelfile):
    '''
    Reads in a product label file as a string
    '''
    with open(os.path.join(path, labelfile)) as infile:
        return infile.read()

def extract_datafile(label):
    ''' Finds the data filename referenced in a product '''
    soup = BeautifulSoup(label, 'lxml-xml')
    if soup.Product_Observational:
        return extract_observational_datafile(soup.Product_Observational)
    if soup.Product_Collection:
        return extract_collection_datafile(soup.Product_Collection)
    if soup.Product_Document:
        return extract_document_datafile(soup.Product_Document)
    return None

def extract_collection_datafile(product):
    ''' Finds the inventory filename referenced in a collection product '''
    file_area = product.File_Area_Inventory if product else None
    file_element = file_area.File if file_area else None
    file_name = file_element.file_name if file_element else None
    return file_name.string

def extract_observational_datafile(product):
    ''' Finds the data filename referenced in a product '''
    file_area = product.File_Area_Observational if product else None
    file_element = file_area.File if file_area else None
    file_name = file_element.file_name if file_element else None
    return file_name.string

def extract_document_datafile(product):
    ''' Finds the document filename referenced in a document product. '''
    document = product.Document if product else None
    document_edition = document.Document_Edition if document else None
    document_file = document_edition.Document_File if document_edition else None
    file_name = document_file.document_file if document_file else None
    return file_name.string

def increment_labelfile(labelfile):
    ''' Creates the filename for a label file with a new version number '''

    (filebase, major, _) = parse_labelfile_name(labelfile)
    newmajor, newminor = major + 1, 0
    return "{}_{}_{}.xml".format(filebase, newmajor, newminor)

def increment_datafile(datafile):
    ''' Creates the filename for a data file with the new version number '''
    (filebase, major, extension) = parse_datafile_name(datafile)
    newmajor = major + 1
    return "{}_{}.{}".format(filebase, newmajor, extension)

def inject_datafile(label, datafile, new_datafile):
    ''' Replaces the filename reference in a label with the specified file '''
    return label.replace(datafile, new_datafile)

def rename(dirname, filename, newfilename):
    ''' Renames a file '''
    src = os.path.join(dirname, filename)
    dst = os.path.join(dirname, newfilename)

    if os.path.exists(newfilename):
        print("File already exists: " + newfilename)
    else:
        os.rename(src, dst)

def parse_datafile_name(name):
    ''' Extract the version number from a data file, if available '''
    versioned_match = re.match(DATAFILE_PARSE_VERSIONED_REGEX, name)
    if versioned_match:
        (filebase, major, extension) = versioned_match.groups()
        return (filebase, int(major), extension)

    unversioned_match = re.match(DATAFILE_PARSE_UNVERSIONED_REGEX, name)
    (filebase, extension) = unversioned_match.groups()
    return (filebase, 1, extension)

def parse_labelfile_name(name):
    ''' Extract the version number from a label file, if available '''
    versioned_match = re.match(LABELFILE_PARSE_VERSIONED_REGEX, name)
    if versioned_match:
        (filebase, major, minor) = versioned_match.groups()
        return (filebase, int(major), int(minor))

    unversioned_match = re.match(LABELFILE_PARSE_UNVERSIONED_REGEX, name)
    filebase = unversioned_match.groups()[0]
    return (filebase, 1, 0)

def increment_major(major, _):
    '''
    Returns the version number with the major version incremented,
    and the minor version reset to 1
    '''
    return (major + 1, 0)

def increment_minor(major, minor):
    ''' Returns the version number with the minor version incremented '''
    return (major, minor + 1)

def attach_version_to_datafile(filebase, extension, major):
    ''' Creates a version of a filename that includes the version number '''
    return '{filebase}_{major}.{extension}'.format(
        major=major,
        filebase=filebase,
        extension=extension
    )

def attach_version_to_labelfile(filebase, major, minor):
    ''' Creates a version of a label filename that includes the version number '''
    return '{filebase}_{major}_{minor}.xml'.format(
        filebase=filebase,
        major=major,
        minor=minor
    )

if __name__ == '__main__':
    sys.exit(main())
