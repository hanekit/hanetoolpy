#!/usr/bin/env python
# Standard library imports
from pathlib import Path
from subprocess import run

# Third-party imports

# Application-specific imports
from hanetoolpy.jobs.pbsjob import BasePbsJob
from hanetoolpy.utils.config import get_config

config = get_config()


class BaseVaspJob:
    def __init__(self,
                 vasp_command=config["vasp"]["default_vasp_command"],
                 mpi_command=config["mpi"]["default_mpi_command"],
                 ppn=config["mpi"]["default_ppn"]):
        self.vasp_command = vasp_command
        self.mpi_command = mpi_command
        self.ppn = ppn
        self.logfile = "vasp.log"

    def get_command(self):
        mpi_perfix = f"{self.mpi_command} -n {self.ppn}"
        return f"time {mpi_perfix} {self.vasp_command} > {self.logfile}"

    def submit(self):
        job = BasePbsJob()
        job.name = "VASP"
        job.ppn = self.ppn
        job.workdir = Path.cwd()
        submit_command = self.get_command()
        job.commands.append(submit_command)
        job.submit()

    def track(self):
        run(f"tail -f {self.logfile}", shell=True)

    def run(self):
        command = self.get_command()
        run(command, shell=True)


if __name__ == '__main__':
    print("Finish!")
