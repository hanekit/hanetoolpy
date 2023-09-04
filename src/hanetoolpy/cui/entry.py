import textwrap
try:
    import readline
except:
    pass

from hanetoolpy.about import full_version
from hanetoolpy.cui.text import header, divider

width = 80


def print_header():
    print(divider())
    print(header)
    print(full_version.rjust(width))
    print(divider())


def print_options():
    print(" (q) Quit")
    print(" (t) Test")
    print(" (1) BoltzTraP")
    option = input(" ------------>>\n")
    try:
        option_dic[option]()
    except KeyError:
        print("Error: 非法参数，请重新输入。")
        print_options()


def start_cui():
    print_header()
    print_options()


def boltztrap():
    print("BoltzTraP")


def test_tool():
    from subprocess import run
    command = test_str()
    completed_process = run(command, shell=True)


option_dic = {
    "q": quit,
    "t": test_tool,
    "1": boltztrap
}
