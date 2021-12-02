#!/usr/bin/env python3
'''
Convert a stooke model to an obj model
'''

import argparse
import sys
import math

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the name of the file to convert")
    args = parser.parse_args()
    
    with (open(args.filename) as infile):
        coords = ([float(x) for x in line.split()] for line in infile)
        spheres = ((rho, lon, 90-lat) for (lon, lat, rho) in coords)
        carts = (to_cart(rho, theta, phi) for (rho, theta, phi) in spheres)
        #list(carts)
        for (x,y,z) in carts:
            print("v", x, y, z)

    for a in range(0,73):
        for b in range(0,37):
            v1 = pos(a, b)
            v2 = pos(a, b+1)
            v3 = pos(a+1, b)
            print ("f", v1, v2, v3)
    for a in range(1,73):
        for b in range(1,37):
            v1 = pos(a, b)
            v2 = pos(a, b-1)
            v3 = pos(a-1, b)
            print ("f", v1, v2, v3)


def pos(a, b):
    return a * 37 + b + 1

def to_cart(rho, theta, phi):
    x = rho * math.sin(math.radians(phi)) * math.cos(math.radians(theta))
    y = rho * math.sin(math.radians(phi)) * math.sin(math.radians(theta))
    z = rho * math.cos(math.radians(phi))
    return (x, y, z)


if __name__ == '__main__':
    sys.exit(main())