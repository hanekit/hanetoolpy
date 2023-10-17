import logging
import time
from pathlib import Path

import typer
from hanetoolpy.about import __version__
from hanetoolpy.typer.add_commands import add_commands
from rich.logging import RichHandler
from typing_extensions import Annotated

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]},  # 给帮助增加 -h 选项
                  add_completion=False,  # 去除默认参数选项
                  invoke_without_command=True  # 无子命令时运行 callback
                  )
add_commands(app)

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)-s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[RichHandler(omit_repeated_times=False,
                                          show_time=False,
                                          show_level=False,
                                          show_path=False)])
# logging.info("hanetoolpy start...")

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


if __name__ == "__main__":
    app()
