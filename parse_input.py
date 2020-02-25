#!/usr/bin/env python3

import re
import argparse

parser = argparse.ArgumentParser(description="parse restart")
parser.add_argument("-f", dest='filename', help="restart file")
parser.add_argument("--charge", dest='charge', help="parse charge",
                    type=bool, default=False)
args = parser.parse_args()

with open(args.filename, 'r') as f:
    lines = f.read()


def find_charge(lines):
    P_CHARGE = r'CHARGE\s+(-?\d+)'
    a = re.search(P_CHARGE, lines, re.DOTALL)
    charge = a.group(1).strip()

    print(charge)


if args.charge:
    find_charge(lines)
