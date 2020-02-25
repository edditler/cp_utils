#!/usr/bin/env python3
import argparse
import numpy as np
import ase
import ase.io

parser = argparse.ArgumentParser(description="adsorb molecule")
parser.add_argument("-m", dest="molecule", help="molecule")
parser.add_argument("-s", dest="slab", help="slab")
parser.add_argument("-d", dest="distance", help="distance", type=float, default=2.0)
parser.add_argument(
    "-o", dest="output", help="output file", type=str, default="out.xyz"
)
parser.add_argument(
    "-r", dest="rotate", help="rotate the molecule", type=str, default="0 0 0"
)
args = parser.parse_args()


def find_xy_center(mol):
    xmin = np.min(mol.positions, axis=0)[0]
    xmax = np.max(mol.positions, axis=0)[0]

    ymin = np.min(mol.positions, axis=0)[1]
    ymax = np.max(mol.positions, axis=0)[1]

    return [(xmax + xmin) / 2, (ymax + ymin) / 2]


molecule = ase.io.read(args.molecule)
slab = ase.io.read(args.slab)
heigth = args.distance
center_xy_slab = find_xy_center(slab)
center_xy_molecule = find_xy_center(molecule)

max_slab = np.max(slab.positions, axis=0)[2]
min_mol = np.min(molecule.positions, axis=0)[2]

difference = abs(max_slab - min_mol)

molecule.translate(
    (
        (center_xy_slab[0] - center_xy_molecule[0]),
        center_xy_slab[1] - center_xy_molecule[1],
        difference + heigth,
    )
)

angles = [float(x) for x in args.rotate.split()]
molecule.euler_rotate(*angles, center="COM")
atoms = slab + molecule

ase.io.write(args.output, atoms)
