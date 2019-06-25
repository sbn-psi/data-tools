import re

LABELFILE_PARSE_VERSIONED_REGEX=r'(.+)_(\d+)_(\d+)\.xml'
LABELFILE_PARSE_UNVERSIONED_REGEX=r'(.+)\.xml'

DATAFILE_PARSE_VERSIONED_REGEX=r'(.+)_(\d+)\.([a-z0-9]+)'
DATAFILE_PARSE_UNVERSIONED_REGEX=r'(.+)\.([a-z0-9]+)'


def increment_product(labelfile):
    datafile = extract_datafile(labelfile)

    new_labelfile = increment_labelfile(labelfile)
    new_datafile = increment_datafile(datafile)

    inject_datafile(labelfile, datafile)

    rename(labelfile, new_labelfile)
    rename(datafile, new_datafile)

def extract_datafile(labelfile):
    return ''

def increment_labelfile(labelfile):
    (filebase, major, minor) = parse_labelfile_name(labelfile)
    newmajor, newminor = major, minor + 1
    return filebase, newmajor, newminor

def increment_datafile(datafile):
    (filebase, major, extension) = parse_datafile_name(datafile)
    newmajor = major + 1
    return (filebase, newmajor, extension)

def inject_datafile(labelfile, datafile):
    pass

def rename(filename, newfilename):
    pass

def parse_datafile_name(name):
    versioned_match = re.match(DATAFILE_PARSE_VERSIONED_REGEX, name)
    if (versioned_match):
        (filebase, major, extension) = versioned_match.groups()
        return (filebase, major, extension)
    else:
        unversioned_match = re.match(DATAFILE_PARSE_UNVERSIONED_REGEX, name)
        (filebase, extension) = unversioned_match.groups()
        return (filebase, 1, extension)


def parse_labelfile_name(name):
    versioned_match = re.match(LABELFILE_PARSE_VERSIONED_REGEX, name)
    if (versioned_match):
        (filebase, major, minor) = versioned_match.groups()
        return (filebase, major, minor)
    else:
        unversioned_match = re.match(LABELFILE_PARSE_UNVERSIONED_REGEX, name)
        (filebase) = unversioned_match.groups()
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