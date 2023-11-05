from logging import info
from rich import print
from rich.panel import Panel

def get_fermi_energy(outcar="./OUTCAR"):
    key_text = "E-fermi"
    with open(outcar, 'r') as file:
        info(f"Reading OUTCAR file \"{outcar}\" ...")
        lines = file.readlines()
    for line_number, line in enumerate(lines, start=1):
        if key_text in line:
            info("Find \"E-fermi\" line:")
            text = f"{line_number} |" + line.replace("\n", "")
            print(Panel(text))
            e_fermi = float(line.split()[2])
    info(f"Get Fermi energy: E_F = {e_fermi} eV")
    return e_fermi

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)-s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    get_fermi_energy("./test_files/OUTCAR")