from hanetoolpy.jobs.pbsjob import BasePbsJob
from hanetoolpy.print.table import print_args
from hanetoolpy.utils.config import get_config

from pathlib import Path

config = get_config()


def run_sh_with_pbs(
        file: str,
        command: str = None,
):
    """
    Run a Script file with pbs.
    """
    print_args(locals())
    job = BasePbsJob()
    if command is None:
        with open(file, "r") as f:
            file_content = f.read()
        job.commands.append(file_content)
    else:
        job.commands.append(f"{command} {file}")
    job.submit()


def run_py_with_pbs(
        file: str,
        python: str = "python",
        env:str = None,
):
    """
    Run a python file with pbs.
    """
    print_args(locals())
    job = BasePbsJob()
    if env is None:
        job.commands.append(f"{python} {file}")
    else:
        job.commands.append(f"conda run -n {env} {python} {file}")
    job.submit()


if __name__ == '__main__':
    run_sh_with_pbs(file="test.py", command="source")
