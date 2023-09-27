# Standard library imports
from hanetoolpy.functions.ebs_unfold_plotter import main as f102
from hanetoolpy.functions.global_band_plotter import plot as f101
from pathlib import Path

import typer
from typing_extensions import Annotated
import logging
from rich.logging import RichHandler

from hanetoolpy.about import __version__
from hanetoolpy.functions.vasp_run import vasp_run
from hanetoolpy.functions.vasp_stop import vasp_stop


app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]},  # 给帮助增加 -h 选项
                  add_completion=False,  # 去除默认参数选项
                  invoke_without_command=True  # 无子命令时运行 callback
                  )

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)-s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[RichHandler(omit_repeated_times=False,
                                          show_time=False,
                                          show_level=False,
                                          show_path=False)])

current_file_path = Path(__file__).resolve()
package_root = current_file_path.parent.parent


@app.callback(no_args_is_help=True)
def main(context: typer.Context,
         version: Annotated[bool, typer.Option("--version", "-v", help="show version")] = False,
         whereis: Annotated[bool, typer.Option("--where", "-w", help="show package path")] = False):
    """
    TODO: Introduction text.
    """
    if version:  # -version -v 显示程序版本
        print(__version__)
    elif whereis:
        print(package_root)
    elif context.invoked_subcommand is None:
        # no_args_is_help=False 才会执行
        print("use -h for help.")


# 添加 vasp 命令
vasp = typer.Typer(no_args_is_help=True,
                   invoke_without_command=True)
app.add_typer(vasp, name="vasp", help="VASP tools")

# 添加 vasp 子命令
vasp.command("run")(vasp_run)
vasp.command("stop", no_args_is_help=True)(vasp_stop)

vasp.command("f101")(f101)

vasp.command("f102")(f102)

# 添加 vaspkit 命令
vaspkit = typer.Typer(no_args_is_help=True,
                      invoke_without_command=True)
app.add_typer(vaspkit, name="vaspkit", help="VASPKIT tools")

# 添加 vaspkit 子命令
from hanetoolpy.functions.vaspkit import vaspkit_281
vaspkit.command("f281")(vaspkit_281)


if __name__ == "__main__":
    app()
