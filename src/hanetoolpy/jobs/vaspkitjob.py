#!/usr/bin/env python
# Standard library imports
from subprocess import run

# Third-party imports

# Application-specific imports
from hanetoolpy.utils.check_files import check_files


class BaseVaspkitJob:
    def __init__(self):
        self.task_id = None
        self.description = None
        self.short_name = None
        self.input_files = []

    @property
    def log_file(self):
        return f"vaspkit_{self.task_id}_{self.short_name}.log"

    def run(self):
        check_files(self.input_files)
        inputs = [self.task_id] + self.inputs + [""]
        inputs = [str(_) for _ in inputs]
        inputs = R"\n".join(inputs)
        print(f"echo -e \"{inputs}\" | vaspkit > {self.log_file}")
        run(f"echo -e \"{inputs}\" | vaspkit > {self.log_file}")


class Vaspkit281Job(BaseVaspkitJob):
    def __init__(self):
        self.task_id = 281
        self.description = "Generate KPOINTS File for Band-Unfolding Calculation"
        self.short_name = "generate_unfolding_kpoints"
        self.input_files = ["POSCAR", "TRANSMAT.in", "KPATH.in"]
        self.inputs = [2, 0.02, 0.04]


if __name__ == '__main__':
    print("Finish!")
