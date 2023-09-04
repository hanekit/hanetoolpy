import textwrap
try:
    import readline
except:
    pass

from hanetoolpy.about import full_version
from hanetoolpy.cui.text import header, divider
from hanetoolpy.cui.options import print_options
from hanetoolpy.functions.vasp import vasp


width = 80


def print_header():
    print(divider())
    print(header)
    print(full_version.rjust(width))
    print(divider())




def test_tool():
    from subprocess import run
    command = test_str()
    completed_process = run(command, shell=True)


def boltztrap():
    print("BoltzTraP")


main_option_dic = {
    "q": {"name": "Quit", "function": quit},
    "t": {"name": "Test", "function": test_tool},
    "1": {"name": "VASP", "function": vasp},
    "2": {"name": "BoltzTraP", "function": boltztrap},
}


def start_cui():
    print_header()
    print_options(main_option_dic)
