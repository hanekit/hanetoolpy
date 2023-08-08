from hanetoolpy.cui.argparse import get_parser
from hanetoolpy.cui.entry import start_cui
from hanetoolpy.about import full_version


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.version:
        print(full_version)
    elif args.pbs_file:
        pbs_command(args.pbs_file)
    else:
        start_cui()


if __name__ == "__main__":
    main()
