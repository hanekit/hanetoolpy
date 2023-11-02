from copy import deepcopy

from pymatgen.io.vasp import Kpoints


def add_kpoints(kpoints1: Kpoints, kpoints2: Kpoints):
    result = deepcopy(kpoints1)
    result.num_kpts += kpoints2.num_kpts
    result.kpts.extend(kpoints2.kpts)
    result.kpts_weights.extend(kpoints2.kpts_weights)
    result.labels.extend(kpoints2.labels)
    return result


def get_str(self):
    lines = self.__repr__().split("\n")
    header = lines[:3]
    kpoints = lines[3:-1]
    kpoint_lines = []
    for kpoint in kpoints:
        kpoint_list = kpoint.split()
        for intkey, value in enumerate(kpoint_list[:3]):
            kpoint_list[intkey] = f"{float(value):.14f}"
        kpoint_lines.append("    " + "    ".join(kpoint_list))
    result = "\n".join(header + kpoint_lines)
    return result


def write_file(self, filename: str):
    with open(filename, "wt") as f:
        f.write(self.get_str())


@staticmethod
def kpoints_from_kpts(kpts: list, kpts_weights, labels=None):
    num_kpts = len(kpts)
    if kpts_weights == 0:
        kpts_weights = [0] * num_kpts
    if labels is None:
        labels = [""] * num_kpts
    return Kpoints(style="Reciprocal",
                   num_kpts=num_kpts,
                   kpts=kpts,
                   kpts_weights=kpts_weights,
                   labels=labels)


Kpoints.__add__ = add_kpoints
Kpoints.get_str = get_str
Kpoints.write_file = write_file
Kpoints.from_kpts = kpoints_from_kpts


if __name__ == '__main__':
    k1 = Kpoints.from_file("IBZKPT")
    k2 = Kpoints.from_kpts(kpts=[(0.2, 0.1, 0.05), (0.03, 0.02, 0.01), (0, 0, 1)], kpts_weights=0)
    k3 = k1 + k2
    k3.write_file("test.txt")
