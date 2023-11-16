from collections import OrderedDict

import numpy as np
from hanetoolpy.io.vasp import Poscar


class Control:
    """the class of CONTROL file for ShengBTE"""

    def __init__(self):
        self.data = OrderedDict({
            "allocations": OrderedDict(),
            "crystal": OrderedDict(),
            "parameters": OrderedDict(),
            "flags": OrderedDict(),
        })
        self.data["parameters"]["scalebroad"] = 1.0
        self.scell = np.array((1, 1, 1))
        self.ngrid = np.array((1, 1, 1))
        self.temperature = 300

    @staticmethod
    def from_poscar(path):
        control = Control()
        poscar = Poscar.from_file(path)
        # allocations
        control.data["allocations"]["nelements"] = len(poscar.elements)
        control.data["allocations"]["natoms"] = len(poscar.positions)
        # crystal
        control.data["crystal"]["lfactor"] = 0.1  # Angstrom (in VASP) to nm (in ShengBTE)
        control.data["crystal"]["lattvec"] = poscar.lattice
        control.data["crystal"]["elements"] = poscar.elements
        control.data["crystal"]["types"] = poscar.atom_types(start=1)
        control.data["crystal"]["positions"] = poscar.positions
        return control

    @property
    def namelist(self):
        import f90nml
        namelist = f90nml.Namelist(self.data)
        namelist.float_format = " .16f"
        return namelist

    def __str__(self):
        return str(self.namelist)

    def write(self, path="./CONTROL.nml", force=True):
        self.namelist.write(path, force=force)

    @property
    def ngrid(self):
        return self.data["allocations"]["ngrid"]

    @ngrid.setter
    def ngrid(self, value):
        self.data["allocations"]["ngrid"] = np.array(value)

    @property
    def scell(self):
        return self.data["crystal"]["scell"]

    @scell.setter
    def scell(self, value):
        self.data["crystal"]["scell"] = np.array(value)

    @property
    def temperature(self):
        pass

    @temperature.setter
    def temperature(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self.data["parameters"]["T"] = value
        elif isinstance(value, tuple) and len(list(value)) == 3:
            self.data["parameters"].pop("T")
            self.data["parameters"]["T_min"] = value[0]
            self.data["parameters"]["T_max"] = value[1]
            self.data["parameters"]["T_step"] = value[2]
        else:
            print(value)
            raise ValueError
