from pathlib import Path
import logging

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
    try:
        with open(outcar_path, 'r') as f:
            content = f.read()
            if "Total CPU time used" in content:
                return True
            else:
                return False
    except FileNotFoundError:
        return False
