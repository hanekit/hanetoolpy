import logging
from pathlib import Path
from subprocess import run
from typing import Tuple

import typer
from hanetoolpy.about import external_packages_path
from typing_extensions import Annotated

thirdorder_package_path = external_packages_path / "thirdorder"
thirdorder_vasp_path = thirdorder_package_path / "thirdorder_vasp.py"

def sow(
        supercell: Annotated[Tuple[int, int, int], typer.Argument(metavar="[INT * 3]",
                                                                  help="size of supercell")],
        cutoff: Annotated[str, typer.Argument(metavar="-INT|+FLOAT",
                                              help="negative integer (n-th) or positive float (Ang)")],
        thirdorder_vasp_path: Annotated[str, typer.Argument(metavar="PATH",)] = thirdorder_vasp_path):
    """
    run the thirdorder_vasp.py sow

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
    thirdorder_vasp_path = Path(thirdorder_vasp_path)
    if not thirdorder_vasp_path.exists():
        logging.error(f"Can not find the thirdorder_vasp.py at: \n {thirdorder_vasp_path}")
        logging.error(f"Please put this file into the above path, or specify the file path by argument.")
        raise typer.Abort()
    python_command = "python"
    supercell = " ".join(map(str, supercell))
    command = f"{python_command} {thirdorder_vasp_path} sow {supercell} {cutoff}"
    run(command, shell=True)


def reap(
    supercell: Annotated[Tuple[int, int, int], typer.Argument(metavar="[INT * 3]",
                                                              help="size of supercell")],
    cutoff: Annotated[str, typer.Argument(metavar="-INT|+FLOAT",
                                          help="negative integer (n-th) or positive float (Ang)")],
    path: Annotated[str, typer.Argument()] = thirdorder_vasp_path,
):
    """
    run the thirdorder_vasp.py reap

    \b
    Required files:
    | POSCAR
    | vasprun.xml
    \b
    Output files:
    | FORCE_CONSTANTS_3RD
    """
    raise NotImplementedError