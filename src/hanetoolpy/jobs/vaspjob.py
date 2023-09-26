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
                 ppn=config["mpi"]["default_ppn"]):
        self.vasp_command = vasp_command
        self.ppn = ppn
        self.logfile = "vasp.log"

    def submit(self):
        job = BasePbsJob()
        job.name = "VASP"
        job.ppn = self.ppn
        job.workdir = Path.cwd()
        mpi_command = config["mpi"]["default_mpi_command"]
        mpi_perfix = f"{mpi_command} -n {self.ppn}"
        submit_command = f"time {mpi_perfix} {self.vasp_command} > {self.logfile}"
        job.commands.append(submit_command)
        job.submit()

    def track(self):
        # run(f"tail -f {self.logfile}", shell=True)
        pass


if __name__ == '__main__':
    print("Finish!")
