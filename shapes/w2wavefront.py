#! /usr/bin/python
import sys

def convert_tokens(tokens, type):
    out_tokens = [type] + tokens[0:3]
    return " ".join(out_tokens)
    
def convert_face_tokens(tokens, type):
    out_tokens = [type] + [str(int(x) + 1) for x in tokens[0:3]]
    return " ".join(out_tokens)


def to_vertex(line):
    return convert_tokens(line.strip().split(), "v")
    
def to_face(line):
    return convert_face_tokens(line.strip().split(), "f")
    
def convert_file(infilename, outfilename):
    lines = open(infilename).read().split('\n')
    metaline = lines[0]
    vertices, faces = (int(x) for x in metaline.strip().split())
    
    outfile = open(outfilename, "w")
    
    outfile.writelines( (to_vertex(line) + "\n" for line in lines[1:vertices+1]) )
    outfile.writelines( (to_face(line) + "\n" for line in lines[vertices+1:vertices+faces+1]) )
    outfile.close()

#def convert_model(filebase):
#    infilename = filebase + ".tab"
#    outfilename = filebase + ".obj"
#    convert_file(infilename, outfilename)
    
if __name__ == "__main__":
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
    convert_file(infilename, outfilename)
#    convert_model("phobos_ver64q")
#    convert_model("phobos_ver128q")
#    convert_model("phobos_ver256q")
#    convert_model("phobos_ver512q")


