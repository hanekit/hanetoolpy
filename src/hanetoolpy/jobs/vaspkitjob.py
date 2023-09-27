#!/usr/bin/env python
# Standard library imports
import logging
from pathlib import Path
from subprocess import run
from logging import info, error

# Third-party imports


# Application-specific imports

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)-s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def check_files(file_list):
    info(f"Checking input files: {file_list}")
    for file_name in file_list:
        file_path = Path(file_name)
        if file_path.exists():
            info(f"Input file {file_path} found.")
        else:
            error(f"Input file {file_path} not found, program exits.")
            exit()


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
