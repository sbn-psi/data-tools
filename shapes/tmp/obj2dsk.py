#!/usr/bin/env python3 

import sys
import subprocess
import os
import re
import getopt
import itertools

def find_files(dirname):
    '''
    Gets all of the files in a directory
    '''
    filelists = [[os.path.join(subdir, f) for f in files] for subdir, _, files in os.walk(dirname)]
    return itertools.chain.from_iterable(filelists)

def process(dirname,function,filter=None):
    return [function(x) for x in find_files(dirname) if filter is None or filter(x)]

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def rotateMesh(STL_FILE_PATH, ROTATED_STL_FILE_NAME):
    infile = 'infile="' + STL_FILE_PATH + '"'
    SCAD_PATH = os.path.abspath('scad/rotate_stl.scad')

    subprocess.run([
        'openscad',
        '-o', ROTATED_STL_FILE_NAME,
        '-D', infile,
        SCAD_PATH
    ])

def convertToUsdz(ORIGINAL_FILE_NAME):
    STL_FILE_NAME  = re.sub( '.obj', '.obj.stl', ORIGINAL_FILE_NAME )
    STL_FILE_PATH = os.path.abspath(STL_FILE_NAME)
    ROTATED_STL_FILE_NAME  = re.sub( '.obj.stl', '.rotated.stl', STL_FILE_NAME )
    ROTATED_STL_FILE_PATH  = os.path.abspath(re.sub( '.obj.stl', '.rotated.stl', ROTATED_STL_FILE_NAME ))

    # convert to STL
    subprocess.run([
        'meshconv',
        ORIGINAL_FILE_NAME,
        '-c', 'stl',
        '-o', re.sub('.stl', '', STL_FILE_NAME)
    ])

    # rotate mesh
    rotateMesh(STL_FILE_PATH,ROTATED_STL_FILE_NAME)

    # convert back to OBJ
    subprocess.run([
        'meshconv',
        ROTATED_STL_FILE_NAME,
        '-c', 'obj',
        '-o', re.sub('.stl', '', ROTATED_STL_FILE_NAME)
    ])

    ROTATED_OBJ_FILE_NAME = re.sub('.stl', '.obj', ROTATED_STL_FILE_NAME)
    USDZ_FILE_NAME = re.sub('.rotated.obj', '.usdz', ROTATED_OBJ_FILE_NAME)

    # convert to USDZ
    subprocess.run([
        'xcrun', 'usdz_converter',
        ROTATED_OBJ_FILE_NAME,
        USDZ_FILE_NAME
    ])

    # Remove any leftover artifacts
    os.remove(os.path.abspath(STL_FILE_NAME))
    os.remove(os.path.abspath(ROTATED_STL_FILE_NAME))
    os.remove(os.path.abspath(ROTATED_OBJ_FILE_NAME))

    print('Done.')

def main(argv=None):
    if argv is None:
        argv = sys.argv
        try:
            try:
                opts, args = getopt.getopt(argv[1:], "h", ["help"])
            except (getopt.error, msg):
                raise Usage(msg)

            # begin main script process
            print(opts, args)
            dirname = argv[1] if len(argv) > 1 else '.'

            process(dirname,convertToUsdz,lambda x: x.endswith('.obj'))

        except (Usage, err):
            print >>sys.stderr, err.msg
            print >>sys.stderr, "for help use --help"
            return 2

if __name__ == "__main__":
    sys.exit(main())