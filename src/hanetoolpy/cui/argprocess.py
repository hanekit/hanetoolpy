#!/usr/bin/env python
# Standard library imports
# Third-party imports
# Application-specific imports
from hanetoolpy.cui.entry import start_cui
from hanetoolpy.about import full_version
from hanetoolpy.utils.pbs import BasePbsJob
from hanetoolpy.utils.jobs import BaseVaspJob


def argprocess(args):
    if args.pbs:
        if args.file:
            job = BasePbsJob()
            job.file = args.file
            job.submit()
        elif args.command:
            job = BasePbsJob()
            job.commands.append(args.command)
            job.submit()
        else:
            print("请指定文件（-f）或命令（--command）")
    elif args.vasp_run:
        job = BaseVaspJob()
        if args.command:
            job.vasp_command = args.command
        job.submit()
        job.track()
    elif args.version:
        print(full_version)
    else:
        start_cui()


if __name__ == '__main__':
    print("Finish!")
