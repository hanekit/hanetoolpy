from hanetoolpy.utils.jobs import BaseVaspJob

def vasp_run(command: str = "vasp.x_std",
             ppn: int = 8,
             mpi: str = "mpirun",
             logfile: str = "vasp.log"):
    """
    运行一个 vasp 程序
    """
    print("test funtion:")
    print(f"{mpi} -np {ppn} {command} > \"{logfile}\"")
    # job = BaseVaspJob()
    # job.submit()
    # job.track()
