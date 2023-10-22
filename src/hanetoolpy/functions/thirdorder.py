import glob
import logging
import shutil
from pathlib import Path

import typer
from typing_extensions import Annotated


def check_thirdorder_jobs(path: str = "./",
                          gap: int = 50,
                          skipfile: str = "SKIP.log"):
    """
    check_thirdorder_jobs
    """
    from hanetoolpy.functions.vasp import is_vasp_end
    path = Path(path).resolve()
    job_paths = sorted(path.glob("job-*"))
    if len(job_paths) == 0:
        logging.warning("No job-* found, program exit.")
        exit()
    status = []
    for job_path in job_paths:
        state = is_vasp_end(job_path)
        if state == True:
            status.append("#")
        elif (job_path / skipfile).exists():
            status.append("S")
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
    """
    sort the 3RD.POSCAR.* and INCAR KPOINTS POTCAR to job-* folders.
    """
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
                logging.info(str(file_source)+"\tlink to\t" + str(file_destination))
            elif method[0].lower() == 'c':  # for copy
                shutil.copy(file_source, file_destination)
                logging.info(str(file_source)+"\tcopy to\t" + str(file_destination))
            else:
                logging.error(f'Unsupported method: {method}')
            # info(f'Created {method} file for {config_file} in {job_dir}')


def read_header(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()


def check_duplicates(path="./", link: bool = True, skipfile="SKIP.log"):
    """
    check duplicate jobs and write SKIP.log
    """
    work_path = Path(path).resolve()
    jobs = sorted([job for job in list(work_path.glob('job-*')) if job.is_dir()])
    headers = [read_header(job / "POSCAR") for job in jobs]

    for job, header in zip(jobs, headers):
        first_job = jobs[headers.index(header)]
        if job != first_job:
            logging.info(f"{job.name} = {first_job.name}")
            xml_path = job / "vasprun.xml"
            if link:
                if xml_path.is_symlink():
                    xml_path.unlink()
                    logging.info(f"link {xml_path} found, unlinked")
                elif xml_path.is_file():
                    xml_path.rename(xml_path.parent / "vasprun.xml.bak")
                    logging.info(f"file {xml_path} found, renamed it to vasprun.xml.bak")
                xml_path.symlink_to(first_job / "vasprun.xml")
                logging.info(f"link {xml_path} created")
            with open(job / skipfile, 'w') as file:
                file.write(f"{job.name} = {first_job.name}")


def recutoff(old_work_path, new_work_path):
    old_work_path = Path(old_work_path).resolve()
    new_work_path = Path(new_work_path).resolve()
    old_jobs = sorted([job for job in list(old_work_path.glob('job-*')) if job.is_dir()])
    new_jobs = sorted([job for job in list(new_work_path.glob('job-*')) if job.is_dir()])
    old_headers = [read_header(job / "POSCAR") for job in old_jobs]
    new_headers = [read_header(job / "POSCAR") for job in new_jobs]

    for new_job, new_header in zip(new_jobs, new_headers):
        if new_header in old_headers:
            old_job = old_jobs[old_headers.index(new_header)]
            print(f"new-{new_job.name} = old-{old_job.name}")


if __name__ == '__main__':
    check_duplicates("./jobs")
