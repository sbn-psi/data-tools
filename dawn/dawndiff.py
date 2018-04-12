#! /usr/bin/env python
'''
A script that will compare two Dawn IMG files.
'''
import sys

def main(argv=None):
    '''
    Receives two dawn image filenames from the command line and compares the
    data areas.
    '''
    if argv is None:
        argv = sys.argv

    file_name1 = argv[1]
    file_name2 = argv[2]

    compare_files(file_name1, file_name2)


def compare_files(file_name1, file_name2):
    '''
    Compares two dawn image files.
    '''
    data1 = get_data(file_name1)
    data2 = get_data(file_name2)

    if data1 == data2:
        print file_name1 + ' = ' + file_name2
    else:
        print file_name1 + ' != ' + file_name2


def get_data(file_name):
    '''
    Gets the data area from a dawn image.
    '''
    rawheader = read_headers(file_name)
    header = parse_header(rawheader)
    header_size, data_size = get_file_locations(header)
    data = read_data(file_name, header_size, data_size)
    return data


def read_headers(file_name):
    '''
    Read the entire header from a dawn IMG file.
    '''
    lines = []
    with open(file_name) as infile:
        while True:
            line = infile.readline()
            lines.append(line)
            if line.strip() == 'END':
                return lines


def parse_header(lines):
    '''
    Parse the dawn IMG header into a dictionary.
    The format of a dawn header is a PDS3 attached label.

    This parser supports just enough PDS3 to read in the file sizes.
    It does not support multiline expressions. Specifically, it will
    not correcly read in an expression where there is a newline between
    the equals sign and the value.

    Additionally, it will
    not read in all of a multiline string value, which we don't
    really care about, since we are just trying to get the datasize.
    '''
    activedict = {}
    stack = []
    for line in lines:
        if '=' in line:
            (keyword, value) = [x.strip() for x in line.split('=')]
            if keyword == 'OBJECT':
                newdict = {}
                activedict[value] = newdict
                stack.append(activedict)
                activedict = newdict
            elif keyword == 'END_OBJECT':
                activedict = stack.pop()
            else:
                activedict[keyword] = value
    if stack:
        raise 'Could not parse header'
    return activedict


def get_file_locations(header):
    '''
    Interpret the record sizes, etc in the dawn header and find the
    size of the header and the size of the data area.
    '''
    record_size = int(header['RECORD_BYTES'])
    header_records = int(header['LABEL_RECORDS'])
    header_size = record_size * header_records

    sample_count = int(header['IMAGE']['LINE_SAMPLES'])
    line_count = int(header['IMAGE']['LINES'])
    sample_bits = int(header['IMAGE']['SAMPLE_BITS'])
    data_size = sample_count * line_count * sample_bits / 8

    return header_size, data_size


def read_data(file_name, header_size, data_size):
    '''
    Read (dataSize) bytes after (headerSize).
    If your headerSize and dataSize are correct, this should read
    in the entire data area of a dawn image.
    '''
    with open(file_name, 'rb') as infile:
        contents = infile.read()
        return contents[header_size : header_size + data_size]


if __name__ == '__main__':
    sys.exit(main())
