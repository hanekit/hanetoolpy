import argparse

from hanetoolpy.about import full_version


def get_parser():
    parser = argparse.ArgumentParser(
        description=full_version,  # What the program does
        epilog="",  # Text at the bottom of help
        add_help=False
    )

    parser.add_argument('-h', '--help',
                        action='help',
                        help='# Show this help message and exit.')
    parser.add_argument("-v", "--version",
                        action="store_true",
                        dest="version",
                        help="# Displays the currently installed version of hanetoolpy.",
                        )
    parser.add_argument("-t", "--task",
                        type=int,
                        help="# TODO",
                        metavar="function_number",
                        dest="task")
    parser.add_argument("--pbs",
                        dest="pbs",
                        action="store_true",
                        help="# TODO",
                        )
    parser.add_argument("--file",
                        dest="file",
                        type=str,
                        help="# TODO"
                        )
    parser.add_argument("--command",
                        dest="command",
                        type=str,
                        help="# TODO"
                        )
    parser.add_argument("--vasp-run",
                        dest="vasp_run",
                        action="store_true",
                        help="# TODO",
                        )
    parser.add_argument("--btp2-doseffmass",
                        dest="btp2_doseffmass",
                        type=str,
                        default=None,
                        help="# TODO",
                        metavar="scf_dir",
                        )
    return parser


if __name__ == "__main__":
    pass
