from hanetoolpy.jobs.vaspjob import BaseVaspJob
from hanetoolpy.print.table import print_args


def vasp_run(command: str = "vasp.x_std",
             ppn: int = 8,
             mpi: str = "mpirun",
             logfile: str = "vasp.log"):
    """
    运行一个 vasp 程序
    """
    print_args(locals())
    job = BaseVaspJob()
    job.vasp_command =command
    job.ppn = ppn
    job.submit()
    job.track()
