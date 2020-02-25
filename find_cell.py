#!/usr/bin/env python3

import re
import argparse

parser = argparse.ArgumentParser(description="parse restart")
parser.add_argument("-f", dest='filename', help="restart file")
parser.add_argument("--coord", dest='coord', help="parse coordinates", type=bool, default=False)
parser.add_argument("--cell", dest='cell', help="parse cell", type=bool, default=False)
args = parser.parse_args()

with open(args.filename, 'r') as f:
    lines = f.read()

def find_cell(lines):
    P_cell_group = r'&CELL[^_](.+)&END CELL'
    a = re.search(P_cell_group, lines, re.DOTALL)
    cell_group = a.group(1)

    P_abc = r'A\s+(.+)B(.+?)C(.+?)\n'
    a = re.search(P_abc, cell_group, re.DOTALL)

    letters = ['A', 'B', 'C']
    print("&CELL")
    for i in range(1, 4):
        print(' '*4+letters[i-1]+'    '+a.group(i).strip())
    print("&END CELL")


def find_coord(lines):
    P_coord_group = r'&COORD(.+)&END COORD'
    a = re.search(P_coord_group, lines, re.DOTALL)
    coord_group = a.group(1).strip()
    
    natoms = len(coord_group.splitlines())

    print(natoms)
    print('')
    print(coord_group)


if args.coord:
    find_coord(lines)

if args.cell:
    find_cell(lines)

