import numpy as np


class Poscar:
    """the class of POSCAR file for VASP"""

    def __init__(self, path):
        self.header = "POSCAR"
        self.lattice = np.empty((3, 3))
        self.lattice_unit = "Ang"
        self.elements = None
        self.element_numbers = None
        self.positions = None
        self.path = path
        self.read()

    @staticmethod
    def from_file(path):
        return Poscar(path)

    def read(self):
        with open(self.path, "r") as f:
            lines = f.readlines()

        # header
        self.header = lines[0]

        # lattice
        factor = float(lines[1].strip())
        for i in range(3):
            self.lattice[i] = [float(j) for j in lines[2 + i].split()]
        self.lattice *= factor

        # elements
        self.elements = lines[5].split()
        self.element_numbers = np.array(lines[6].split()).astype(int)

        # type
        typeline = lines[7]
        natoms = self.element_numbers.sum()

        # positions
        self.positions = np.empty((natoms, 3))
        for i in range(natoms):
            self.positions[i] = [float(j) for j in lines[8 + i].split()]

        # type
        if typeline[0].lower() in ["c", "k"]:
            import scipy
            self.positions = scipy.linalg.solve(self.lattice, self.positions * factor)

    def atom_types(self, start=0):
        types = [i for i, num in enumerate(self.element_numbers) for _ in range(num)]
        return np.array(types) + start
