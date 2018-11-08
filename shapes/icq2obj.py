#! /usr/bin/env python3

# Translated from fortran code at https://sbnarchive.psi.edu/pds3/dawn/fc/DWNCSPC_4_01/DOCUMENT/ICQMODEL.ASC

import sys

def main(argv=None):
    if argv == None:
        argv = sys.argv

    filename = argv[1]
    outfilename = argv[2]
    outfile = open(outfilename, 'w')

    q, v = read_vertices_from_file(filename)
    

    n = [[[0 for x in range(0, 7)] for y in range(0, q+1)] for z in range(0, q+1)]
    

    vindex = 0
    for f in range(1,7):
        for j in range(0, q+1):
            for i in range(0, q+1):
                vindex += 1
                write_vertex(outfile, v[vindex-1])
                n[i][j][f] = vindex

    share_edges(n, q)
    share_corners(n, q)

    for (f1,f2,f3) in get_facets(n,v,q):
        write_facet(outfile, f1, f2, f3)

def get_facets(n,v,q):
    for f in range(1,7):
        for i in range(0,q):
            for j in range(0,q):
                w1 = [0,0,0]
                w1[0] = calc_coordinate(n, v, f, (i, j, 1), (i+1, j+1, 2))
                w1[1] = calc_coordinate(n, v, f, (i, j, 2), (i+1, j+1, 0))
                w1[2] = calc_coordinate(n, v, f, (i, j, 0), (i+1, j+1, 1))
                w2 = [0,0,0]
                w2[0] = calc_coordinate(n, v, f, (i+1, j, 1), (i, j+1, 2))
                w2[1] = calc_coordinate(n, v, f, (i+1, j, 2), (i, j+1, 0))
                w2[2] = calc_coordinate(n, v, f, (i+1, j, 0), (i, j+1, 1))
                z1=w1[0]**2+w1[1]**2+w1[2]**2
                z2=w2[0]**2+w2[1]**2+w2[2]**2
                if (z1 <= z2):
                    yield(n[i][j][f], n[i+1][j+1][f], n[i+1][j][f])
                    yield(n[i][j][f], n[i][j+1][f], n[i+1][j+1][f])
                else:
                    yield(n[i][j][f], n[i][j+1][f], n[i+1][j][f])
                    yield(n[i+1][j][f], n[i][j+1][f], n[i+1][j+1][f])


def share_edges(n, q):
    for i in range(1, q):
        n[i][q][6] = n[q-i][q][4]
        n[i][0][6] = n[i][q][2]
        n[i][0][5] = n[q][q-i][1]
        n[i][0][4] = n[q-i][0][1]
        n[i][0][3] = n[0][i][1]
        n[i][0][2] = n[i][q][1]

    for j in range(1, q):
        n[q][j][6] = n[j][q][5]
        n[q][j][5] = n[0][j][4]
        n[q][j][4] = n[0][j][3]
        n[q][j][3] = n[0][j][2]
        n[0][j][6] = n[q-j][q][3]
        n[0][j][5] = n[q][j][2]        

def share_corners(n, q):
    n[0][0][3] = n[0][0][1]
    n[q][0][4] = n[0][0][1]
    n[0][0][2] = n[0][q][1]
    n[q][0][3] = n[0][q][1]
    n[0][0][4] = n[q][0][1]
    n[q][0][5] = n[q][0][1]
    n[0][0][5] = n[q][q][1]
    n[q][0][2] = n[q][q][1]
    n[0][0][6] = n[0][q][2]
    n[q][q][3] = n[0][q][2]
    n[0][q][5] = n[q][q][2]
    n[q][0][6] = n[q][q][2]
    n[q][q][4] = n[0][q][3]
    n[0][q][6] = n[0][q][3]
    n[q][q][5] = n[0][q][4]
    n[q][q][6] = n[0][q][4]



def calc_coordinate(n, v, f, c1, c2):
    i1,j1,v1 = c1
    i2,j2,v2 = c2
    return v[n[i1][j1][f]][v1] * v[n[i2][j2][f]][v2] - v[n[i1][j1][f]][v2] * v[n[i2][j2][f]][v1]
    
def write_vertex(outfile, c):
    c2 = [str(t) for t in c]
    outfile.write('v ' + ' '.join(c2) + '\r\n')

def write_facet(outfile, f1, f2, f3):
    outfile.write('f ' + ' '.join([str(x) for x in [f1,f2,f3]]) + '\r\n')
 

def read_vertices_from_file(filename):
    lines = open(filename).readlines()
    q = int(lines[0].strip())
    vertices = [[float(f) for f in x.strip().split()] for x in lines[1:] if x.strip()]
    return q, vertices

if __name__ == '__main__':
    sys.exit(main())