#!/usr/bin/env python
# Standard library imports
from subprocess import run
from dataclasses import dataclass, field
from typing import Any

# Third-party imports
from rich.console import Console

# Application-specific imports


@dataclass
class BasePbsJob:
    # qsub options
    date_time: Any = None  # -a
    account_string: Any = None  # -A
    secs: Any = None  # -b
    checkpoint_options: Any = None  # -c
    directive_prefix: Any = None  # -C
    workdir: Any = None  # -d
    join: Any = None  # -j
    keep: Any = None  # -k
    kill_delay: Any = None  # -K
    resource_list: list = None  # -l
    nodes: Any = None  # -l nodes
    ppn: Any = None  # -l ppn
    walltime: Any = None  # -l walltime
    mail_options: str = None  # -m [b][a][e]
    mail_address: str = None  # -M
    name: str = None  # -N
    stdout: Any = None  # -o
    stderr: Any = None  # -e
    # job args
    commands: list = field(default_factory=list)  # = []
    file: Any = None
    jobid: Any = None

    def submit(self):
        cmd = ["qsub"]
        if self.workdir:
            cmd.extend(["-d", str(self.workdir)])
        if self.name:
            cmd.extend(["-N", self.name])
        if self.nodes and self.ppn:
            nodes = str(self.nodes)
            ppn = str(self.ppn)
            cmd.extend(["-l", f"node={nodes}:ppn={ppn}"])
        if self.walltime:
            cmd.extend(["-l", f"walltime={self.walltime}"])
        if self.join:
            cmd.extend(["-j", self.join])
        if self.stdout:
            cmd.extend(["-o", self.stdout])
        if self.stderr:
            cmd.extend(["-e", self.stderr])
        if self.mail_options:
            cmd.extend(["-m", self.mail_options])
        if self.mail_address:
            cmd.extend(["-M", self.mail_address])
        if self.commands:
            with open("temp.pbs", "w") as file:
                file.write("\n".join(self.commands))
            self.file = "temp.pbs"
        cmd.append(self.file)
        console = Console()
        console.print("your command is:")
        console.print(" ".join(cmd), style="blue")
        result = run(cmd, capture_output=True, text=True)
        console.print(result.stdout)
        # output = result.stdout.strip()
        # if output.startswith("Your job"):
        #     self.jobid = output.split()[2]
        #     print("Job", self.jobid, "submitted.")
        # else:
        #     print("Error submitting job:", output)

    def cancel(self):
        if self.jobid is not None:
            run(["qdel", self.jobid])
            self.jobid = None
        else:
            print("No job ID associated with this job.")

    def get_status(self):
        if self.jobid is not None:
            result = run(
                ["qstat", "-f", self.jobid], capture_output=True, text=True)
            output = result.stdout.strip()
            if output.startswith("Job Id:"):
                status = output.split("job_state = ")[1].split()[0]
                return status
        return None


class CustomPbsJob(BasePbsJob):
    def __init__(self):
        super().__init__()
        self.ppn = 8
        self.walltime = "10000:00:00"


if __name__ == "__main__":
    job = CustomPbsJob()
    job.jobname = "myjob"
    job.stdout = "myjob.out"
    job.stderr = "myjob.err"
    job.commands = ["command1",
                    "command2",
                    "command3"]
    job.submit()
