#! /usr/bin/env python3
import sys

def convert_tokens(tokens, type):
    out_tokens = [type] + tokens[:]
    return " ".join(out_tokens)

def offset(line):
    tokens = []
    for token in line.strip().split():
        tokens.append(str(int(token) + 1))
    return tokens

def to_vertex(line):
    return convert_tokens(line.strip().split(), "v")
    
def to_face(line):
    return convert_tokens(offset(line), "f")
    
def convert_file(infilename, outfilename):
    lines = open(infilename).read().split('\n')
    metaline = lines[0]
    vertices =  int(metaline.strip().split()[0])
    
    outfile = open(outfilename, "w")
    
    outfile.writelines( (to_vertex(line) + "\n" for line in lines[1:vertices+1] if line.strip()))
    outfile.writelines( (to_face(line) + "\n" for line in lines[vertices+1:] if line.strip()))
    outfile.close()
    
if __name__ == "__main__":
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
    convert_file(infilename, outfilename)
