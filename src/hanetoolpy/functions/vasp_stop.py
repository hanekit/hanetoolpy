from typing_extensions import Annotated
import typer


def vasp_stop(ele: Annotated[bool, typer.Option("--ele", "-e", help="VASP will stop at the next electronic step.")] = False,
              ion: Annotated[bool, typer.Option("--ion", "-i", help="VASP will stop at the next ionic step.")] = False):
    """
    Stop current folder's VASP Process by STOPCAR.
    """
    # 使用列表来存储文件的各行内容
    content_lines = [
        "# Stop at the next electronic step",
        "LABORT = .TRUE." if ele else "# LABORT = .TRUE.",
        "",
        "# Stop at the next ionic step",
        "LSTOP  = .TRUE." if ion else "# LSTOP  = .TRUE.",
        "",
    ]

    # 使用 join 方法将列表中的各行内容连接成一个字符串，每行之间用换行符分隔
    content = '\n'.join(content_lines)

    with open("STOPCAR", "w") as file:
        file.write(content)
