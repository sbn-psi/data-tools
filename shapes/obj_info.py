#!/usr/bin/python

import sys
import re

v_manifest = {}

def lines(file):
	return file.split("\n")

def get_count(file,token):
	return str(len(re.findall(token,file)))

def missing( idx ):
	print('missing vertex reference: ',idx)

def countVertices( line ):
	for v in line.split():
		if v in v_manifest:
			v_manifest[v] = v_manifest[v] + 1
		else:
			v_manifest[v] = 1

def print_details(file):
	print('Filename: ' + filename)
	print('Vertices: ' + get_count(file,"v "))
	print('Faces: ' + get_count(file,"f "))
	check_manifest(v_manifest,int(get_count(file,"v ")))

def check_manifest( m, max ):
	for idx in range(max):
		key = str(idx)
		if key not in m and key != "0": # wavefront format index begins at 1
			missing(idx)

def main( file ):
	v_count = get_count(file,"v ")
	for i, line in enumerate(lines(file)):
		if (int(i) > int(v_count)) and len(line) > 0:
			countVertices(line)
	print_details(file)

if __name__ == "__main__":
	filename = sys.argv[1]
	with open(filename) as f:
		main( file=f.read() )
	print("Done.")