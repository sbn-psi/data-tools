from string import Formatter
import level0
import level1
import poly
import sys

KEYS=[x for x in poly.COEFFICIENTS.keys()]



def main(argv):
    if argv is None:
        argv = sys.argv

    l0filename = argv[1]
    l1filename = argv[2]

    records = {}

    for record in extract_records(l0filename, level0.RECORD_LENGTH):
        extracted = level0.extract_record(record)
        records[timestamp(extracted)] = extracted

    for record in extract_records(l1filename, level1.RECORD_LENGTH):
        extracted = level1.extract_record(record)
        records[timestamp(extracted)].update(extracted)

    for record in records.values():
        calc_keyed(record, KEYS, poly.apply)
        calc_n12(record)

    for name in KEYS:
        export(records, name, "14.5f")

    export(records, "fpe_n12v_v", "14.5f")

    return 0

def extract_records(file, record_length):
    with open(file, "rb") as f:
        data = f.read()
        return (data[x:x+record_length] for x in range(0, len(data), record_length))

def timestamp(extracted):
    return extracted["idp_ccsds_timestamp"]


def calc_keyed(extracted, keys, f):
    for k in keys:
        dn = extracted[k]
        c = f(k, dn)

        store_values(extracted, k, c)

def calc_n12(extracted):
    p12 = extracted["fpe_p12v_v"]
    n12 = extracted["fpe_n12v_v"]
    c = (0.00371803*n12) - (0.00743605*p12)
    store_values(extracted, "fpe_n12v_v", c)

def store_values(record, k, c):
    kc = k + "_cal"

    record[kc] = c

def build_format_string(basename, extension_format_spec):
    extensions = ["_x", "_cal"]
    base_format = "{%s}" % basename
    extension_formats = ",".join(["{%s:%s}" % (basename + e, extension_format_spec) for e in extensions])
    return base_format + "," + extension_formats

def field_list(basename):
    extensions = ["", "_x", "_cal"]
    return ["idp_ccsds_timestamp"] + [basename + x for x in extensions]

def export(records, basename, format_spec):
    do_export(records, basename + ".csv", field_list(basename), build_format_string(basename, format_spec))

def do_export(records, filename, fields, format_str):
    with open(filename, "w") as f:
        f.write(", ".join([k for k in fields]) + "\r\n")
        for r in records.values():
            f.write(Formatter().format(format_str, **r) + "\r\n")


if __name__ == "__main__":
    sys.exit(main(None))