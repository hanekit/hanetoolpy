#!/usr/bin/env python
# Standard library imports
import logging
from pathlib import Path
from logging import info, error

# Third-party imports


# Application-specific imports

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)-s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def check_files(file_list):
    info(f"Checking input files: {file_list}")
    for file_name in file_list:
        file_path = Path(file_name)
        if file_path.exists():
            info(f"Input file {file_path} found.")
        else:
            error(f"Input file {file_path} not found, program exits.")
            exit()