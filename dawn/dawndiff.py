#! /usr/bin/env python
'''
A script that will compare two Dawn IMG files.
'''
import sys
import dawn

def main(argv=None):
    '''
    Receives two dawn image filenames from the command line and compares the
    data areas.
    '''
    if argv is None:
        argv = sys.argv

    file_name1 = argv[1]
    file_name2 = argv[2]

    dawn.compare_files(file_name1, file_name2)

if __name__ == '__main__':
    sys.exit(main())
