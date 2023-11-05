import logging
from pathlib import Path

from rich import print
from typing_extensions import Annotated


def check_vasp_end(path="./"):
    path = Path(path).resolve()
    result = is_vasp_end(path)
    if result:
        logging.info(f"[v] {path} finished.")
    else:
        logging.info(f"[x] {path} unfinished.")


def is_vasp_end(path="./"):
    """
    Check if the VASP job is finished.
    """
    path = Path(path).resolve()
    outcar_path = path / "OUTCAR"
    if outcar_path.exists():
        with outcar_path.open('r') as f:
            content = f.read()
            if "Total CPU time used" in content:
                return True
            else:
                return "Running"
    else:
        return False


def get_band_info(
    path: Annotated[
        str, typer.Option(help="The path of vasp workdir")] = "./",
    save: Annotated[
        bool, typer.Option(help="Whether to save information to save_path")] = True,
    save_path: Annotated[
        str, typer.Option(help="The file path to save information")] = "./hanetoolpy-band_info.toml",
):
    """
    Get information about the electron energy band edge and band gap.
    """
    job_dir = Path(path).resolve()
    info_dict = dict()

    from hanetoolpy.utils.vasp.eigenval import Eigenval
    eigenval = Eigenval(job_dir / "EIGENVAL")
    info_dict.update(eigenval.get_info())

    from hanetoolpy.utils.vasp.outcar import get_fermi_energy
    fermi_energy = get_fermi_energy(job_dir / "OUTCAR")
    data = {
        "fermi_energy": fermi_energy,
        "VBM_fermi": round(info_dict["VBM_energy"] - fermi_energy, 10),
        "CBM_fermi": round(info_dict["CBM_energy"] - fermi_energy, 10),
    }
    info_dict.update(data)

    from rich.table import Table
    table = Table(title="Band Information")
    table.add_column("quantity")
    table.add_column("value")
    for key, value in info_dict.items():
        table.add_row(str(key), str(value))
    print(table)

    if save:
        logging.info(f"Saving band information to \"{save_path}\".")
        import toml
        with open(save_path, "w") as file:
            toml.dump(info_dict, file)

    logging.info(f"Finish!")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s][%(levelname)-s]: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    get_band_info("../utils/vasp/test_files", save="../utils/vasp/test_files/1.toml")
