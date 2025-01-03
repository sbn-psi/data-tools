#! /usr/bin/env python3
import struct
import argparse
import itertools


FORMAT_SPECS = {
    "IEEE_REAL": "f",
    "MSB_INTEGER": "i",
    "CHARACTER": "s"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--declared", action="store_true")
    parser.add_argument("fmtfilepath", type=str)
    parser.add_argument("datapath", type=str)
    args = parser.parse_args()

    columns = read_fmt_file(args.fmtfilepath)

    header = ",".join(make_header(column) for column in columns)

    print(header)
    print_data_file(args.datapath, columns, args.declared)


def print_data_file(datapath, columns, declared):
    with open(datapath, "rb") as infile:
        if declared:
            print_declared_columns(infile, columns)
        else:
            print_calculated_columns(infile, columns)


def iter_read(infile, size):
    """
    Reads a file in chunks of the specified size. The file must be a multiple of the chunk size
    """
    while True:
        buf = infile.read(size)
        if len(buf) == size:
            yield buf
        elif len(buf) == 0:
            break
        else:
            raise Exception(f"Number of bytes read ({len(buf)}) did not match expected length ({size})")


def print_declared_columns(infile, columns):
    """
    Prints column information using the declared start bytes
    """
    lastcolumn = columns[-1]
    linelength = int(lastcolumn["BYTES"]) + int(lastcolumn["START_BYTE"]) - 1
    lines = iter_read(infile, linelength)
    for line in lines:
        vals = itertools.chain.from_iterable(read_declared_column(line, column) for column in columns)
        print(",".join(format_val(x) for x in vals))


def print_calculated_columns(infile, columns):
    """
    Prints column information using the calculated start bytes
    """
    format_string = ">" + "".join(make_format_string(column) for column in columns)
    lines = iter_read(infile, struct.calcsize(format_string))
    for line in lines:
        vals = struct.unpack(format_string, line)
        print(",".join(format_val(x) for x in vals))

def read_declared_column(line, column):
    """
    Reads a column from the record using the declared start bytes
    """
    start_byte = int(column["START_BYTE"]) - 1
    bytes = int(column["BYTES"])
    column_bytes = line[start_byte:start_byte+bytes]

    return struct.unpack(">" + make_format_string(column), column_bytes)    

def read_fmt_file(filepath):
    columns = []
    active = {}

    for line in open(filepath):
        trimmed = line.strip()
        if "=" in trimmed:
            key, val = [x.strip() for x in trimmed.split("=")]
            if key == "END_OBJECT":
                columns.append(active)
                active = {}
            else:
                active[key] = val

    return columns

def make_format_string(column):
    if "ITEMS" in column:
        return f"{column["ITEMS"]}{FORMAT_SPECS[column["DATA_TYPE"]]}"
        #return "".join(int(column["ITEMS"]) * [f'{FORMAT_SPECS[column["DATA_TYPE"]]}'])
    elif column["DATA_TYPE"] == "CHARACTER":
        return(f'{column["BYTES"]}{FORMAT_SPECS[column["DATA_TYPE"]]}')
    else:
        return(f'{FORMAT_SPECS[column["DATA_TYPE"]]}')
    
def make_header(column):
    if "ITEMS" in column:
        return ",".join(f"{column['NAME']}_{i+1}" for i in range(0, int(column["ITEMS"])))
    return column["NAME"]

def format_val(x):
    if type(x) is bytes:
        try:
            return x.decode('utf-8')
        except Exception:
            return "(CANNOT DECODE STRING)"

    return str(x)


if __name__ == "__main__":
    main()