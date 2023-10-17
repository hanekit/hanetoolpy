import glob
import logging
from pathlib import Path
from subprocess import run
from typing import Tuple

import typer
from hanetoolpy.about import external_packages_path
from typing_extensions import Annotated

thirdorder_package_path = external_packages_path / "thirdorder"
thirdorder_vasp_path = thirdorder_package_path / "thirdorder_vasp.py"


def main(
    action: Annotated[str, typer.Argument(metavar="sow/reap", help="action")],
    supercell: Annotated[Tuple[int, int, int], typer.Argument(metavar="[INT * 3]",
                                                              help="size of supercell")],
    cutoff: Annotated[str, typer.Argument(metavar="-INT|+FLOAT",
                                          help="negative integer (n-th) or positive float (Ang)")],
    path: Annotated[str, typer.Argument()] = thirdorder_vasp_path,
):
    """
    run the thirdorder_vasp.py

    \b
    Required files:
    | POSCAR
    \b
    Output files:
    | 3RD.SPOSCAR
    | 3RD.POSCAR.*
    """
    try:
        import thirdorder_core
    except ModuleNotFoundError as error:
        logging.error(error)
        logging.error("NOTE: Please confirm that you have installed thirdorder correctly.")
        raise typer.Abort()
    python_command = "python"
    thirdorder_vasp_path = path
    supercell = " ".join(map(str, supercell))
    command = f"{python_command} {thirdorder_vasp_path} {action} {supercell} {cutoff}"
    run(command, shell=True)


def check_thirdorder_jobs(path="./", gap:int=10):
    """
    check_thirdorder_jobs
    """
    from hanetoolpy.functions.vasp import is_vasp_end
    path = Path(path).resolve()
    job_paths_pattern = str(path / "job-*")
    job_paths = sorted(glob.glob(job_paths_pattern))
    status = []
    for job_path in job_paths:
        state = is_vasp_end(job_path)
        if state == True:
            status.append("#")
        elif state == "Running":
            status.append("R")
        else:
            status.append("_")
    status_text = "".join(status)
    status_count = {}
    status_count["finished"] = status.count("#")
    status_count["unfinished"] = len(status_text)-status.count("#")
    status_count["running"] = status.count("R")
    status_count["unstarted"] = status.count("_")

    def progress_bar(current, maximum, bar_length=50):
        progress = int((current / maximum) * bar_length)
        precent = str(int(current / maximum * 100))
        bar = '[' + '#' * progress + '_' * (bar_length - progress) + "]"
        return f"{bar} {precent} % ({current} / {maximum})"

    def format(text, gap=gap):
        result = []
        last_job_num = len(text)
        for i in range(0, last_job_num, gap):
            start_index = i
            end_index = min(i + gap, last_job_num)
            line = f"{start_index:03} {text[start_index:end_index]} {end_index:03}"
            result.append(line)
        return '\n'.join(result)

    print(path)
    print("Total Progress")
    print(progress_bar(status_count["finished"],len(status_text)))
    print("Detailed Progresses")
    print(format(status_text))

