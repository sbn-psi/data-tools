#! /usr/bin/env python3

import sys
import os

ORIGINAL_STRING= '''
        <Target_Identification>
            <name>(101955) Bennu</name>
            <alternate_designation>1999 RQ36</alternate_designation>
            <type>Asteroid</type>
            <Internal_Reference>
                <lid_reference>urn:nasa:pds:context:target:asteroid.101955_bennu</lid_reference>
                <reference_type>data_to_target</reference_type>
            </Internal_Reference>
        </Target_Identification>'''

REPLACEMENT_STRING = '''
        <Target_Identification>
            <name>(101955) Bennu</name>
            <alternate_designation>1999 RQ36</alternate_designation>
            <type>Asteroid</type>
            <Internal_Reference>
                <lid_reference>urn:nasa:pds:context:target:asteroid.101955_bennu</lid_reference>
                <reference_type>collection_to_target</reference_type>
            </Internal_Reference>
        </Target_Identification>'''

filenames = sys.argv[1:]
for filename in filenames:
    with open(filename) as f:
        contents = f.read()
    
    if ORIGINAL_STRING in contents:
        updated = contents.replace(ORIGINAL_STRING, REPLACEMENT_STRING)

        os.rename(filename, filename + '.bak')

        with open(filename, 'w') as f2:
            f2.write(updated)
        print('updated ' + filename )
    else:
        print(filename + ' does not contain string')