#! /usr/bin/env python3

import argparse
import pds3parse
import csv
import itertools
import sys


def to_dict(parsed, context=""):
    result = {}
    print (parsed)
    names = [e['value']['scalar'] for e in parsed if e['name'] == 'NAME']
    objname = names[0] if names else None
    prefix = context + objname + '.' if objname else context

    for entry in parsed:
        key = prefix + entry['name']
        if entry['type'] in ('attribute', 'pointer'):
            values = entry['value']
            if isinstance(values, dict) and 'scalar' in values:
                result[key] = values['scalar'].strip()
            elif isinstance(values, dict) and 'set' in values:
                result[key] = ';'.join(
                    sub["scalar"].strip() for sub in values['set'] if "scalar" in sub)
            elif isinstance(values, list):
                result[key] = ';'.join([x['scalar'].strip() for x in values])
            else:
                print(entry)
        elif entry['type'] == 'object':
            subresult = to_dict(entry['value'], key + ".")
            result.update(subresult)
        else:
            print(entry)

    return result


def file_to_dict(parser, filepath):
    with open(filepath) as f:
        data = f.read()
        parsed = parser.parse(data)
        parsed_dict = to_dict(parsed)
        parsed_dict['meta.filepath'] = filepath
        return parsed_dict


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--output-file",
                           default="out.csv",
                           help='The name of the csv file to write to. Defaults to out.csv')
    argparser.add_argument("labels", nargs="*")
    args = argparser.parse_args()

    parser = pds3parse.parser

    result = [file_to_dict(parser, filepath) for filepath in args.labels]

    # print(result)
    headers = set(itertools.chain.from_iterable([x.keys() for x in result]))
    with (open(args.output_file, 'w')) as outfile:
        csvout = csv.DictWriter(outfile, headers)
        csvout.writeheader()
        csvout.writerows(result)


if __name__ == '__main__':
    sys.exit(main())
