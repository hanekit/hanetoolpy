from hanetoolpy.cui.argparse import get_parser
from hanetoolpy.cui.argprocess import argprocess


def main():
    parser = get_parser()
    args = parser.parse_args()
    argprocess(args)


if __name__ == "__main__":
    main()
