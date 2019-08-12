import re
import os
import sys
from bs4 import BeautifulSoup

LABELFILE_PARSE_VERSIONED_REGEX=r'(.+)_(\d+)_(\d+)\.xml'
LABELFILE_PARSE_UNVERSIONED_REGEX=r'(.+)\.xml'

DATAFILE_PARSE_VERSIONED_REGEX=r'(.+)_(\d+)\.([a-z0-9]+)'
DATAFILE_PARSE_UNVERSIONED_REGEX=r'(.+)\.([a-z0-9]+)'

def main(argv=None):
    if argv is None:
        argv = sys.argv
    filepaths = argv[1:]

    for filepath in filepaths:
        dirname, filename = os.path.split(filepath)
        increment_product(dirname, filename)


def increment_product(path, labelfile):
    print(labelfile)
    label = read_label(path, labelfile)
    datafile = extract_datafile(label)

    new_labelfile = increment_labelfile(labelfile)

    if datafile:
        new_datafile = increment_datafile(datafile)
        contents = inject_datafile(label, datafile, new_datafile)
        with open(new_labelfile, "w") as f:
            f.write(contents)
        rename(path, datafile, new_datafile)
    else:
        rename(path, labelfile, new_labelfile)

def read_label(path, labelfile):
    with open(os.path.join(path, labelfile)) as f:
        return f.read()

def extract_datafile(label):
    soup = BeautifulSoup(label, 'lxml-xml')
    if soup.Product_Observational:
        return extract_observational_datafile(soup.Product_Observational)
    elif soup.Product_Collection:
        return extract_collection_datafile(soup.Product_Collection)
    elif soup.Product_Document:
        return extract_document_datafile(soup.Product_Document)
    else:
        return None

def extract_collection_datafile(product):
    file_area = product.File_Area_Inventory if product else None
    file_element = file_area.File if file_area else None
    file_name = file_element.file_name if file_element else None
    return file_name.string

def extract_observational_datafile(product):
    file_area = product.File_Area_Observational if product else None
    file_element = file_area.File if file_area else None
    file_name = file_element.file_name if file_element else None
    return file_name.string

def extract_document_datafile(product):
    document = product.Document if product else None
    document_edition = document.Document_Edition if document else None
    document_file = document_edition.Document_File if document_edition else None
    file_name = document_file.document_file if document_file else None
    return file_name.string

def increment_labelfile(labelfile):
    (filebase, major, minor) = parse_labelfile_name(labelfile)
    newmajor, newminor = major + 1 , 0
    return "{}_{}_{}.xml".format(filebase, newmajor, newminor)

def increment_datafile(datafile):
    (filebase, major, extension) = parse_datafile_name(datafile)
    newmajor = major + 1
    return "{}_{}.{}".format(filebase, newmajor, extension)

def inject_datafile(label, datafile, new_datafile):
    return label.replace(datafile, new_datafile)

def rename(dir, filename, newfilename):
    src = os.path.join(dir, filename)
    dst = os.path.join(dir, newfilename)

    if (os.path.exists(newfilename)):
        print ("File already exists: " + newfilename)
    else:
        os.rename(src, dst)

def parse_datafile_name(name):
    versioned_match = re.match(DATAFILE_PARSE_VERSIONED_REGEX, name)
    if (versioned_match):
        (filebase, major, extension) = versioned_match.groups()
        return (filebase, int(major), extension)
    else:
        unversioned_match = re.match(DATAFILE_PARSE_UNVERSIONED_REGEX, name)
        (filebase, extension) = unversioned_match.groups()
        return (filebase, 1, extension)

def parse_labelfile_name(name):
    versioned_match = re.match(LABELFILE_PARSE_VERSIONED_REGEX, name)
    if (versioned_match):
        (filebase, major, minor) = versioned_match.groups()
        return (filebase, int(major), int(minor))
    else:
        unversioned_match = re.match(LABELFILE_PARSE_UNVERSIONED_REGEX, name)
        filebase = unversioned_match.groups()[0]
        return (filebase, 1, 0)

def increment_major(major, minor):
    return (major + 1, 0)

def increment_minor(major, minor):
    return (major, minor + 1)

def attach_version_to_datafile(filebase, extension, major):
    return '{filebase}_{major}.{extension}'.format({
        'major': major,
        'filebase': filebase,
        'extension': extension
    })

def attach_version_to_labelfile(filebase, major, minor):
    return '{filebase}_{major}_{minor}.xml'.format({
        'major': major,
        'minor': minor,
        'filebase': filebase
    })

if __name__ == '__main__':
    sys.exit(main())