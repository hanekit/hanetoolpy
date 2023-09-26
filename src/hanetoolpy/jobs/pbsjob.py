#!/usr/bin/env python
# Standard library imports
from subprocess import run
from dataclasses import dataclass, field
from typing import Any

# Third-party imports
from logging import info, warning, error
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Application-specific imports
from hanetoolpy.utils.config import get_config

config = get_config()
pbs_config = config["pbs"]

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
    nodes: Any = pbs_config.get("nodes")  # -l nodes
    ppn: Any = pbs_config.get("ppn")  # -l ppn
    walltime: Any = pbs_config.get("walltime")  # -l walltime
    mail_options: str = pbs_config.get("mail_options")  # -m [b][a][e]
    mail_address: str = pbs_config.get("mail_address")  # -M
    name: str = pbs_config.get("name")  # -N
    stdout: Any = None  # -o
    stderr: Any = None  # -e
    # job args
    # field(default_factory=list) = []
    pre_commands: list = field(default_factory=lambda: pbs_config.get("pre_commands", []))
    commands: list = field(default_factory=list)
    post_commands: list = field(default_factory=lambda: pbs_config.get("post_commands", []))
    file: Any = None
    jobid: Any = None

    def submit(self):
        cmd = ["qsub"]
        console = Console()
        table = Table(title="PBS running arguments")
        table.add_column("Arg")
        table.add_column("Value")
        if self.workdir:
            table.add_row("workdir", str(self.workdir))
            cmd.extend(["-d", str(self.workdir)])
        if self.name:
            table.add_row("name", str(self.name))
            cmd.extend(["-N", self.name])
        if self.nodes is not None and self.ppn is None:
            nodes = str(self.nodes)
            table.add_row("nodes", nodes)
            cmd.extend(["-l", f"node={nodes}"])
        elif self.ppn is not None:
            ppn = str(self.ppn)
            nodes = self.nodes or 1
            nodes = str(nodes)
            table.add_row("nodes", nodes)
            table.add_row("ppn", ppn)
            cmd.extend(["-l", f"nodes={nodes}:ppn={ppn}"])
        if self.walltime:
            table.add_row("walltime", self.walltime)
            cmd.extend(["-l", f"walltime={self.walltime}"])
        if self.join:
            cmd.extend(["-j", self.join])
        if self.stdout:
            cmd.extend(["-o", self.stdout])
        if self.stderr:
            cmd.extend(["-e", self.stderr])
        if self.mail_options:
            table.add_row("mail options", str(self.mail_options))
            cmd.extend(["-m", self.mail_options])
        if self.mail_address:
            table.add_row("mail address", str(self.mail_address))
            cmd.extend(["-M", self.mail_address])
        temp_path = "temp.pbs"
        table.add_row("file", temp_path)
        file_commands = self.pre_commands + self.commands + self.post_commands
        file_content = "\n".join(file_commands)
        from rich.syntax import Syntax
        if len(self.commands) >= 2:
            syntax = Syntax(file_content, "bash", line_numbers=True)
        else:
            syntax = Syntax(file_content, "bash")
        with open(temp_path, "w") as file:
            file.write(file_content)
        self.file = "temp.pbs"
        cmd.append(self.file)
        console.print(table)  # PBS running arguments
        console.print(f"The content of {temp_path} is:")
        console.print(Panel(syntax,
                            title=temp_path))
        console.print("The following command will be executed:")
        command = " ".join(cmd)
        console.print(Panel(command))
        try:
            result = run(command, shell=True, capture_output=True, text=True)
        except FileNotFoundError as e:
            print(e)
            error("qsub 命令执行失败")
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


if __name__ == "__main__":
    job = BasePbsJob()
    job.jobname = "myjob"
    job.stdout = "myjob.out"
    job.stderr = "myjob.err"
    job.commands = ["command1",
                    "command2",
                    "command3"]
    job.submit()
