#! /usr/bin/env python3

import sys
import os
from bs4 import BeautifulSoup

CANDIDATES= ['''
        <Target_Identification>
            <name>(101955) Bennu</name>
            <alternate_designation>1999 RQ36</alternate_designation>
            <type>Asteroid</type>
        </Target_Identification>''','''
        <Target_Identification>
            <name>(101955) BENNU</name>
            <alternate_designation>1999 RQ36</alternate_designation>
            <type>Asteroid</type>
        </Target_Identification>''','''
 	 <Target_Identification>
            <name>(101955) Bennu</name>
            <alternate_designation>1999 RQ36</alternate_designation>
            <type>Asteroid</type>
        </Target_Identification>''']       

REPLACEMENT_STRING = '''
        <Target_Identification>
            <name>(101955) Bennu</name>
            <alternate_designation>1999 RQ36</alternate_designation>
            <type>Asteroid</type>
            <Internal_Reference>
                <lid_reference>urn:nasa:pds:context:target:asteroid.101955_bennu</lid_reference>
                <reference_type>{reference_type}</reference_type>
            </Internal_Reference>
        </Target_Identification>'''

REFERENCE_TYPES = {
    "Product_Observational":"data_to_target",
    "Product_Collection":"collection_to_target",
    "Product_Bundle":"bundle_to_target",
    "Product_Document":"document_to_target",    
}

def main():
    filenames = sys.argv[1:]
    for filename in filenames:
        process_file(filename)

def process_file(filename):
        with open(filename) as f:
            contents = f.read()

        original_strings = [x for x in CANDIDATES if x in contents]

        if original_strings:
            product_type = find_product_type(contents)
            reference_type = REFERENCE_TYPES[product_type]

            for original_string in original_strings:
                updated = contents.replace(original_string, REPLACEMENT_STRING.format(reference_type=reference_type))

                os.rename(filename, filename + '.bak')

                with open(filename, 'w') as f2:
                    f2.write(updated)
                print('updated ' + filename )
        else:
            print(filename + ' does not contain string')

def find_product_type(labelstr):
    soup = BeautifulSoup(labelstr, "lxml-xml")
    return soup.find(REFERENCE_TYPES.keys()).name


if __name__ == '__main__':
    sys.exit(main())