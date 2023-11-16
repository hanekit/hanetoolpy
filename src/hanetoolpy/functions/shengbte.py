import logging
from typing import Annotated, Tuple, Union

import typer
from hanetoolpy.io.shengbte import Control
from rich import print
from rich.panel import Panel


def shengbte_run():
    """
    TODO
    """
    pass


def poscar_to_control(
        poscar: Annotated[
            str,
            typer.Option("--poscar", "-p",
                         metavar="PATH",
                         help="Path of POSCAR file")]
    = "./POSCAR",
        temperature: Annotated[
            int,
            typer.Option("--temperature", "-t",
                         metavar="INT",
                         help="Single value of temperature (priority)")]
    = None,
        temperatures: Annotated[
            Tuple[int, int, int],
            typer.Option("--temperatures", "--ts",
                         metavar="[INT INT INT]",
                         help="(T_min, T_max, T_step)")]
    = (None, None, None),
        ngrid: Annotated[
            Tuple[int, int, int],
            typer.Option("--ngird", "-n",
                         metavar="[INT INT INT]",
                         help="Value of ngrid")]
    = (1, 1, 1),
        supercell: Annotated[
            Tuple[int, int, int],
            typer.Option("--supercell", "--sc",
                         metavar="[INT INT INT]",
                         help="Supercell of FORCE_CONSTANTS_2ND")]
    = (1, 1, 1),
    path: Annotated[
            str,
            typer.Option("--path", "-s",
                         metavar="PATH",
                         help="Save path of CONTROL file")]
    = "./CONTROL",
):
    """
    generate the CONTROL file from POSCAR file.
    """
    control = Control.from_poscar(poscar)
    if temperature is not None:
        control.temperature = temperature
    elif temperatures != (None, None, None):
        control.temperature = temperatures
    else:
        control.temperature = 300
    control.ngrid = ngrid
    control.scell = supercell
    logging.info("The CONTROL file is generated as below:")
    print(Panel(str(control), title = path))
    control.write(path=path)
    logging.info(f"The CONTROL file is saved to {path}.")


