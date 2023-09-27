from hanetoolpy.jobs.vaspjob import BaseVaspJob
from hanetoolpy.print.table import print_args
from hanetoolpy.utils.config import get_config

config = get_config()

def vasp_run(command: str = config["vasp"]["default_vasp_command"],
             ppn: int = config["mpi"]["default_ppn"],
             mpi: str = config["mpi"]["default_mpi_command"],
             logfile: str = config["vasp"]["default_vasp_logfile"]):
    """
    运行一个 vasp 程序
    """
    print_args(locals())
    job = BaseVaspJob()
    job.vasp_command =command
    job.ppn = ppn
    job.submit()
    job.track()
