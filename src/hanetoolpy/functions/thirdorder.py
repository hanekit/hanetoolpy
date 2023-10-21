import glob
import logging
import shutil
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


def check_thirdorder_jobs(path="./", gap: int = 50):
    """
    check_thirdorder_jobs
    """
    from hanetoolpy.functions.vasp import is_vasp_end
    path = Path(path).resolve()
    job_paths_pattern = str(path / "job-*")
    job_paths = sorted(glob.glob(job_paths_pattern))
    if len(job_paths) == 0:
        logging.warning("No job-* found, program exit.")
        exit()
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
            line = f"{start_index+1:03} {text[start_index:end_index]} {end_index:03}"
            result.append(line)
        return '\n'.join(result)

    print(path)
    print("Total Progress")
    print(progress_bar(status_count["finished"], len(status_text)))
    print("Detailed Progresses")
    print(format(status_text))


def organize_files(
    poscar_dir: Annotated[str, typer.Argument(help="Directory containing config files")] = './',
    jobs_dir: Annotated[str, typer.Option(help="(hex/rec) Symmetry of the system")] = "./jobs",
    incar_path: Annotated[str, typer.Argument(help="Path to INCAR file")] = 'INCAR',
    kpoints_path: Annotated[str, typer.Argument(help="Path to KPOINTS file")] = 'KPOINTS',
    potcar_path: Annotated[str, typer.Argument(help="Path to POTCAR file")] = 'POTCAR',
    method: Annotated[str, typer.Option(help="Method for organizing files: 'softlink' or 'copy'")] = 'softlink',
):
    poscar_dir = Path(poscar_dir).resolve()
    jobs_dir = Path(jobs_dir).resolve()
    jobs_dir.mkdir(exist_ok=True)
    input_files = {
        "INCAR": incar_path,
        "KPOINTS": kpoints_path,
        "POTCAR": potcar_path,
    }
    for key, path in input_files.items():
        input_files[key] = Path(path).resolve()

    for poscar in glob.glob(str(poscar_dir / '3RD.POSCAR.*')):
        job_number = poscar.split('.')[-1]
        job_dir = jobs_dir / f'job-{job_number}'
        job_dir.mkdir(exist_ok=True)
        shutil.move(poscar, job_dir / 'POSCAR')

        for file_name, file_source in input_files.items():
            file_destination = job_dir / file_name
            if method[0].lower() == 's':  # for softlink
                file_destination.symlink_to(file_source)
                logging.info(str(file_source)+"\tlink to\t"+ str(file_destination))
            elif method[0].lower() == 'c':  # for copy
                shutil.copy(file_source, file_destination)
                logging.info(str(file_source)+"\tcopy to\t"+ str(file_destination))
            else:
                logging.error(f'Unsupported method: {method}')
            # info(f'Created {method} file for {config_file} in {job_dir}')


if __name__ == '__main__':
    organize_files()
