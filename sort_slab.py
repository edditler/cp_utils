import ase
import ase.io

@click.command()
@click.option('--structure', default='last_geometry.xyz', help='Input')
@click.option('--output', default='output.xyz', help='Output')
def sort_it(structure, output):
    """
    Sorts the atoms in the slab according to their z-coordinate.
    Lowest z-coordinate => lowest index
    """
    s = ase.io.read(structure)
    new_slab = ase.Atoms()
    for index in np.argsort(slab.positions[:, 2]):
        new_slab.append(slab[index])
    ase.io.write(output, new_slab)

if __name__ == '__main__':
    sort_it()
