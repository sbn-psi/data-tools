#! /usr/bin/env python
'''
A script that will compare two Dawn IMG files.
'''
import sys
import os
import os.path
import dawn

def main(argv=None):
    '''
    Receives two dawn image filenames from the command line and compares the
    data areas.
    '''
    if argv is None:
        argv = sys.argv

    direcory_name1 = argv[1]
    direcory_name2 = argv[2]

    compare_directories(direcory_name1, direcory_name2)



def compare_directories(directory1, directory2):
    '''
    Compares two directories of dawn image files.
    Both directories must have the same structure.
    '''
    dirlist1 = get_dir_list(directory1)
    dirlist2 = get_dir_list(directory2)

    compare_contents(directory1, directory2, dirlist1)

def compare_contents(directory1, directory2, dirlist):
    for (dirname, filenames) in dirlist:
        for filename in filenames:
            file1 = os.path.join(directory1, dirname, filename)
            file2 = os.path.join(directory2, dirname, filename)

            if os.path.exists(file1) and os.path.exists(file2):
                dawn.compare_files(file1, file2)
            elif os.path.exists(file1):
                print(file1 + " <- " + file2)
            elif os.path.exists(file2):
                print(file1 + " -> " + file2)
            else:
                print("No files exist")


def is_dawn(filename):
    return filename.lower().endswith('.img')

def get_dir_list(directory):
    walkresult = [(dirpath, [x for x in filenames if is_dawn(x)]) for dirpath, _, filenames in os.walk(directory)]
    return [(dirpath.replace(directory, '') , filenames) for dirpath, filenames in walkresult if filenames]

if __name__ == '__main__':
    sys.exit(main())
