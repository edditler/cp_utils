#!/usr/bin/env python3
import ase.io
import click

@click.command()
@click.option('--n-slab', default=460, help='Fixed atoms')
@click.option('--n-adsorbate', default=100, help='Moved atoms')
@click.option('--distance', default=3.0, help='Distance')
@click.option('--structure', default='last_geometry.xyz', help='Input')
@click.option('--output', default='output.xyz', help='Output')
def move_it(n_slab, n_adsorbate, distance, structure, output):
    s = ase.io.read(structure)
    slab = s[:n_slab]
    mol = s[n_slab:n_slab+n_adsorbate]
    mol.translate([0, 0, distance])
    ase.io.write(output, slab + mol)

if __name__ == '__main__':
    move_it()

