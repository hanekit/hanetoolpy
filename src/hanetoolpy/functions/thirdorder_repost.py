import logging
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
        path: Annotated[str, typer.Argument()] = thirdorder_vasp_path):
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
    python_command = "python"
    thirdorder_vasp_path = path
    supercell = " ".join(map(str, supercell))
    command = f"{python_command} {thirdorder_vasp_path} {action} {supercell} {cutoff}"
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