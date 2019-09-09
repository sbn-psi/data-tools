import sys
import json

from string import Formatter
import os.path

from extractor import Extractor
from keymap import Keymap
from poly import Polynomials

def main(argv=None):
    if argv is None:
        argv = sys.argv

    l0filename = argv[1]
    l1filename = argv[2]

    level0 = Extractor("l0label.xml")
    level1 = Extractor("l1label.xml")

    fields = Keymap("fields.csv")

    polys = Polynomials("coefficients.csv", fields)

    records = []
    l0_record_length = level0.record_length
    l1_record_length = level1.record_length

    l0records = extract_records(l0filename, l0_record_length)
    l1records = extract_records(l1filename, l1_record_length)

    for l0rec, l1rec in zip(l0records, l1records):
        extracted = {}
        extracted.update(level0.extract_record(l0rec))
        extracted.update(level1.extract_record(l1rec))
        records.append(extracted)

    for record in records:
        calc_keyed(record, fields.raw.keys(), polys.apply)

    outputdir = os.path.join("outputdir", os.path.basename(l0filename).replace(".dat", ""))
    os.makedirs(outputdir)

    for name in fields.raw.keys():
        export(records, outputdir, name, "14.5f")

    return 0


def extract_records(file, record_length):
    with open(file, 'rb') as f:
        data = f.read()
        return (data[x:x+record_length] for x in range(0, len(data), record_length))


def calc_keyed(extracted, keys, funcs):
    for k in keys:
        dn = extracted[k]
        c = funcs(k, dn)

        store_values(extracted, k, c)

def store_values(record, k, c):
    kc = k + "_cal"
    record[kc] = c

def export(records, outputdir, basename, format_spec):
    do_export(records, os.path.join(outputdir, basename + ".csv"), field_list(basename), build_format_string(basename, format_spec))

def do_export(records, filename, fields, format_str):
    with open(filename, "w") as f:
        f.write(", ".join([k for k in fields]) + "\r\n")
        for r in records:
            f.write(Formatter().format(format_str, **r) + "\r\n")

def build_format_string(basename, extension_format_spec):
    extensions = ["_x", "_cal"]
    base_format = "{%s}" % basename
    extension_formats = ",".join(["{%s:%s}" % (basename + e, extension_format_spec) for e in extensions])
    return base_format + "," + extension_formats

def field_list(basename):
    extensions = ["", "_x", "_cal"]
    return [basename + x for x in extensions]            

if __name__ == '__main__':
    sys.exit(main())