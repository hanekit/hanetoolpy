import typer
from typing_extensions import Annotated

from hanetoolpy.about import __version__
from hanetoolpy.functions.global_band_plotter import plot


app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]},  # 给帮助增加 -h 选项
                  add_completion=False,  # 去除默认参数选项
                  invoke_without_command=True  # 无子命令时运行 callback
                  )


@app.callback()
def main(context: typer.Context,
         version: Annotated[bool, typer.Option("--version", "-v", help="show version")] = False):
    """
    直接运行时执行的函数。
    """
    if version:  # -version -v 显示程序版本
        print(__version__)
    elif context.invoked_subcommand is None:  # 无子命令时显示帮助
        print("use -h for help.")


# 添加 vasp 子命令
vasp = typer.Typer(no_args_is_help=True,
                   invoke_without_command=True)
app.add_typer(vasp, name="vasp", help="VASP tools")

# 添加 vasp-f101 子命令
vasp.command("f101", no_args_is_help=True)(plot)

if __name__ == "__main__":
    app()
