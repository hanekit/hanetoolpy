
import typer
from typing_extensions import Annotated
from hanetoolpy.jobs.vaspkitjob import Vaspkit281Job


help_dict = {
    "scheme": """\b
    K-Mesh Scheme.
    | G: Gamma Scheme
    | M: Monkhorst-Pack Scheme
    """,
    "kscf": """\b
    Resolution for SCF Calculation.
    | Typical Value: 0.02-0.04
    """,
    "kpath": """\b
    Resolution along K-Path.
    | Typical Value: 0.03-0.05 for DFT
    |                0.04-0.06 for hybrid DFT
    """
}


def vaspkit_281(scheme: Annotated[str, typer.Option(help=help_dict["scheme"])] = "G",
                kscf: Annotated[float, typer.Option(help=help_dict["kscf"])] = 0.03,
                kpath: Annotated[float, typer.Option(help=help_dict["kpath"])] = 0.04,
                ):
    """
    Generate KPOINTS file for Band-Unfolding Calculation.

    \b
    Required files:
    | POSCAR
    | TRANSMAT.in
    | KPATH.in
    \b
    Output files:
    | KPOINTS
    """
    job = Vaspkit281Job()
    job.run()
