from rich.console import Console
from rich.table import Table


def dict_table(data: dict,
               title=None,
               header=("Key", "Value"),
               show_header: bool = False,
               ) -> Table:
    """
    将一个词典转化为 Table 对象
    """
    table = Table(title=title,
                  show_header=show_header)
    table.add_column(header[0])
    table.add_column(header[1])
    for key, value in data.items():
        table.add_row(str(key), str(value))
    return table


def print_args(args):
    """
    将参数词典以表格的形式打印出来展示
    """
    console = Console()
    table = dict_table(args,
                       title="Running arguments",
                       header=("Arg", "Value"),
                       show_header=True)
    console.print(table)


if __name__ == '__main__':
    def testfuc():
        a = 1
        b = 2
        print_args(locals())


    test_dict = {"A": "string",
                 "B": 123456,
                 "C": 1.2345,
                 "D": ["1", "2", "3"]}
    test_table = dict_table(test_dict)
    test_console = Console()
    test_console.print(test_table)
    testfuc()
