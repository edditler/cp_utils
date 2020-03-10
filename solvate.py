#!/usr/bin/env python
import numpy as np
from tqdm import tqdm
import argparse
import copy


def distance(atom1, atom2):
    d = np.subtract(atom1, atom2)
    return np.linalg.norm(d)


def list_to_xyz(atoms, file):
    print(f'Writing to {file}')
    with open(file, 'w') as f:
        f.write(f"{len(atoms)}\n")
        f.write("\n")
        for atom in tqdm(atoms):
            element = atom[0]
            x = atom[1][0]
            y = atom[1][1]
            z = atom[1][2]
            line = f"{element} {x} {y} {z}\n"
            f.write(line)


def box_dimensions(box):
    x = y = z = 0
    for water in box:
        if water[0] > x:
            x = water[0]
        if water[1] > y:
            y = water[1]
        if water[2] > z:
            z = water[2]

    return (x, y, z)


def center_molecule(mol, point):
    coord = np.zeros((len(mol), 3))
    for i, at in enumerate(mol):
        coord[i] = np.array(at[1])
    mol_com = np.average(coord, axis=0)
    disp = np.subtract(mol_com, np.array(point)/2)

    mol_shifted = copy.deepcopy(mol)
    for i, at in enumerate(mol):
        mol_shifted[i][1][0] -= disp[0]
        mol_shifted[i][1][1] -= disp[1]
        mol_shifted[i][1][2] -= disp[2]
    return mol_shifted


# Comand line parser
parser = argparse.ArgumentParser(description="solvate molecule")
parser.add_argument("-w", dest='file_water', help="xyz-file of the water box")
parser.add_argument("-m", dest='file_molecule', help="xyz-file of the molecule")
parser.add_argument("-R", dest='radius', help="Approximate radius inside which the water molecules will be removed around the molecule", type = float)
parser.add_argument("-o", dest='fname_out', help="Name of output file name", type = str, default = 'solvated.xyz')
parser.add_argument("-check", dest='check_box', help="Check if water box consists of water molecules", type = bool, default = False)
args = parser.parse_args()


def solvate(waterbox_file, molecule_file, radius):
    # read molecule files
    with open (molecule_file, 'r') as f:
        lines = f.readlines()[2:]
        molecule = [[line.split()[0],
                     list(float(i) for i in line.split()[1:4])] for line in lines ]

    print(f'Found {len(molecule)} atoms in the molecule.')

    # read water box file
    hydrogen = []
    oxygen = []

    with open(waterbox_file, 'r') as f:
        lines = f.readlines()[2:]
        no = 0
        nh = 0
        for line in lines:
            # print(line.split()[0])
            if line.split()[0] == 'O':
                oxygen.append(list(float(i) for i in line.split()[1:4]))
                no += 1
            elif line.split()[0] == 'H':
                hydrogen.append(list(float(i) for i in line.split()[1:4]))
                nh += 1

    print(f'Found {no} oxygen and {nh} hydrogen')

    # Create the list of water molecules
    water_molecules = []
    for o in tqdm(oxygen):
        tmp_water = []
        tmp_water.append(['O', o])
        found_h = []
        for i, h in enumerate(hydrogen):
            if distance(o, h) < 1.4:
                found_h.append(i)
                tmp_water.append(['H', h])

        # make sure we found a whole H2O
        try:
            assert len(found_h) == 2
        except AssertionError:
            print('The water box is broken!')

        water_molecules.append(tmp_water)

        # make sure we don't find the same H again
        for fh in sorted(found_h, reverse=True):
            del hydrogen[fh]
    print('Done doing the list of water.')
    box_x, box_y, box_z = box_dimensions(oxygen+hydrogen)

    # Constrain the thing to the slab
    # slab_min = [1000, 1000, 1000]
    # slab_max = [-1000, -1000, -1000]
    # for m in molecule:
    #     if m[1][0] < slab_min[0]:
    #         slab_min[0] = m[1][0]
    #     if m[1][1] < slab_min[1]:
    #         slab_min[1] = m[1][1]
    #     if m[1][2] < slab_min[2]:
    #         slab_min[2] = m[1][2]

    #     if m[1][0] > slab_max[0]:
    #         slab_max[0] = m[1][0]
    #     if m[1][1] > slab_max[1]:
    #         slab_max[1] = m[1][1]
    #     if m[1][2] > slab_max[2]:
    #         mol_top = m[1][2]
    #         if m[0] == 'Ti':
    #             slab_max[2] = m[1][2]

    # print(slab_min, slab_max)
    # Add the water to the box
    mol_centered = center_molecule(molecule, point=(box_x, box_y, box_z))
    solvated_molecule = []
    solvated_molecule += mol_centered
    print(f'Originally there are {len(solvated_molecule)} atoms.')
    for water in tqdm(water_molecules):
        o = water[0][1:3]
        h1 = water[1][1:3]
        h2 = water[2][1:3]

        center = np.add(o, h1)
        center = np.add(center, h2)
        center /= 3
        center = center[0]

        # # should be above the slab
        # is_okay = center[2] >= slab_max[2]
        # # but not too far
        # is_okay &= center[2] <= (mol_top+10)

        # # should also be above in x and y
        # is_okay &= center[0] >= slab_min[0]-1 and center[0] <= slab_max[0]+1
        # is_okay &= center[1] >= slab_min[1]-1 and center[1] <= slab_max[1]+1

        is_okay = True
        for m in mol_centered:
            if distance(m[1], center) < radius:
                is_okay = False

        if is_okay:
            solvated_molecule += water

    print(f'With water there are {len(solvated_molecule)} atoms.')
    list_to_xyz(solvated_molecule, args.fname_out)


solvate(args.file_water, args.file_molecule, args.radius)
