import typer
from typing_extensions import Annotated
import logging
from rich.logging import RichHandler

from hanetoolpy.about import __version__
from hanetoolpy.functions.vasp_run import vasp_run


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


@app.callback()
def main(context: typer.Context,
         version: Annotated[bool, typer.Option("--version", "-v", help="show version")] = False):
    """
    TODO: Introduction text.
    """
    if version:  # -version -v 显示程序版本
        print(__version__)
    elif context.invoked_subcommand is None:  # 无子命令时显示帮助
        print("use -h for help.")


# 添加 vasp 命令
vasp = typer.Typer(no_args_is_help=True,
                   invoke_without_command=True)
app.add_typer(vasp, name="vasp", help="VASP tools")

# 添加 vasp 子命令
vasp.command("run")(vasp_run)

from hanetoolpy.functions.global_band_plotter import plot as f101
vasp.command("f101")(f101)

from hanetoolpy.functions.ebs_unfold_plotter import main as f102
vasp.command("f102")(f102)

if __name__ == "__main__":
    app()
