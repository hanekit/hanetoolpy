#!/usr/bin/env python
# Standard library imports
from pathlib import Path
from subprocess import run
# Third-party imports
# Application-specific imports
from hanetoolpy.utils.pbs import BasePbsJob


class BaseVaspJob:
    def __init__(self, vasp_command="vasp641.x_std"):
        self.vasp_command = vasp_command
        self.ppn = 8
        self.logfile = "vasp.log"

    def submit(self):
        job = BasePbsJob()
        job.name = "VASP"
        job.ppn = self.ppn
        job.workdir = Path.cwd()
        submit_command = f"time mpirun -n {self.ppn} {self.vasp_command} > {self.logfile}"
        job.commands.append(submit_command)
        job.submit()

    def track(self):
        run(f"tail -f {self.logfile}", shell=True)


if __name__ == '__main__':
    print("Finish!")
