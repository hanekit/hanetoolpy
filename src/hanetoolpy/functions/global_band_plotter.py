#!/usr/bin/env python
import logging
import math
from logging import info

import matplotlib
import numpy as np
import pandas as pd
import typer
from hanetool.utils.vasp.eigenval import Eigenval
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

matplotlib.use('Agg')
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)-s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def rotate_xy(xy, angle):
    """ 将 二维坐标 围绕原点旋转 angle 角度 """
    x, y = xy
    rad = np.radians(angle)
    rotation_matrix = np.array([[math.cos(rad), -math.sin(rad)],
                                [math.sin(rad), math.cos(rad)]])
    x2, y2 = np.dot(rotation_matrix, (x, y))
    return x2, y2


def ab_to_xy(df, sym):
    df = df.copy()
    if sym == "hex":  # 六角胞
        df['k_x'] = df['k_a'] + 0.5 * df['k_b']
        df['k_y'] = (3 ** 0.5) / 2 * df['k_b']
    elif sym == "rec":  # 矩形胞
        df['k_x'] = df['k_a']
        df['k_y'] = df['k_b']
    else:
        raise NotImplementedError(f"Unsupported Symmetry {sym}")
    return df


def mirror(points):
    new_points = []
    for point in points:
        x, y, z = point
        new_point = (x, -y, z)
        new_points.append(new_point)
    return new_points


def rotate(points, angles):
    new_points = []
    for angle in angles:
        for point in points:
            x, y, z = point
            x2, y2 = rotate_xy((x, y), angle)
            new_point = (x2, y2, z)
            new_points.append(new_point)
    return new_points


def get_colormap(style):
    from matplotlib.colors import LinearSegmentedColormap
    if style == "Excel-RYG":
        colors = ['#F8696B', '#FFEB84', '#63BE7B']  # 颜色
        positions = [0.0, 0.5, 1.0]  # 颜色位置
    elif style == "Depth":
        colors = ['#000000', '#EEEEEE']  # 颜色
        positions = [0.0, 1.0]  # 颜色位置
    # 生成色卡
    colormap = LinearSegmentedColormap.from_list('custom_colormap', list(zip(positions, colors)))
    return colormap


def get_fermi_by_vaspkit(path="./FERMI_ENERGY"):
    """
    备用方法，暂未使用。
    """
    with open(path, "r") as file:
        dataline = file.readlines()
        fermi = float(dataline[1].split()[0])
    return fermi


def get_fermi(outcar="./OUTCAR"):
    key_text = "E-fermi"
    with open(outcar, 'r') as file:
        lines = file.readlines()
    for line_number, line in enumerate(lines, start=1):
        if key_text in line:
            # info("Find \"E-fermi\" line:")
            # text = f"{line_number} |" + line.replace("\n", "")
            # print(Panel(text, title=outcar))
            e_fermi = float(line.split()[2])
    info(f"Get Fermi energy: {e_fermi} eV")
    return e_fermi


def 添加外边缘(ax, sym):
    length = 1
    if sym == "hex":  # 六角胞
        angles = np.pi * (1 / 6 + 1 / 3 * np.arange(7))
        points = length * np.sqrt(3) / 3 * np.exp(1j * angles)
        points = np.c_[point_complex.real, point_complex.imag]
    elif sym == "rec":  # 矩形胞
        l = 0.5 * length
        points = [(l, l), (-l, l), (-l, -l), (l, -l)]
    else:
        raise NotImplementedError(f"Unsupported Symmetry {sym}")
    border = Polygon(points,
                     lw=2,  # 线宽
                     edgecolor='black',  # 边缘颜色
                     clip_on=False,  # 允许绘制的图形超出绘图轴的范围
                     facecolor='none')  # 不填充内部，只绘制边缘
    ax.add_patch(border)


def 添加能带路径(ax, sym):
    if sym == "hex":  # 六角胞
        g = (0, 0)
        m = (0.5, 0)
        k = (0.5, 0.5 / 3 ** 0.5)
        points = [g, m, k]
        # 绘制高对称点字符
        ax.annotate("Γ",
                    xy=g,
                    xycoords='data',
                    xytext=(0, 10),
                    textcoords='offset points')
        ax.annotate("M",
                    xy=m,
                    xycoords='data',
                    xytext=(5, 5),
                    textcoords='offset points')
        ax.annotate("K",
                    xy=k,
                    xycoords='data',
                    xytext=(5, 5),
                    textcoords='offset points')
    elif sym == "rec":  # 矩形胞
        g = (0, 0)
        x = (0.5, 0)
        y = (0, 0.5)
        s = (0.5, 0.5)
        points = [g, x, s, y]
        # 绘制高对称点字符
        ax.annotate("Γ",
                    xy=g,
                    xycoords='data',
                    xytext=(5, 5),
                    textcoords='offset points')
        ax.annotate("X",
                    xy=x,
                    xycoords='data',
                    xytext=(5, 5),
                    textcoords='offset points')
        ax.annotate("S",
                    xy=s,
                    xycoords='data',
                    xytext=(5, 5),
                    textcoords='offset points')
        ax.annotate("Y",
                    xy=y,
                    xycoords='data',
                    xytext=(5, 5),
                    textcoords='offset points')
    else:
        raise NotImplementedError(f"Unsupported Symmetry {sym}")
    # 绘制路径
    path = Polygon(points,
                   lw=2,  # 线宽
                   edgecolor='black',  # 边缘颜色为红色
                   clip_on=False,  # 允许绘制的图形超出绘图轴的范围
                   facecolor='none')  # 不填充多边形，只绘制边缘
    ax.add_patch(path)
    # 绘制高对称点
    for point in points:
        ax.plot(*point, 'o', color="black")


def draw_dot(ax, xy, text):
    ax.plot(*xy, 'o', color="black", markerfacecolor='white')
    # 添加点的图例
    label_xy = (0.30, 0.55)
    ax.plot(*label_xy, 'o', color="black", markerfacecolor='white')
    ax.annotate(text,
                xy=label_xy,
                xycoords='data',
                xytext=(12, -5),
                textcoords='offset points',
                fontsize=15)


def print_args(args):
    console = Console()
    arg_table = Table(title="Running Parameters")
    arg_table.add_column("arg")
    arg_table.add_column("value")
    for key, value in args.items():
        arg_table.add_row(str(key), str(value))
    console.print(arg_table)


def plot(sym: Annotated[str, typer.Option(help="(hex/rec) Symmetry of the system")],
         index: Annotated[str, typer.Option(help="(Both/VB/CB) The index of the energy band to output")] = "Both",
         soc: Annotated[bool, typer.Option(help="Whether the SOC is used in the calculation")] = False,
         axis: Annotated[bool, typer.Option(help="Whether to draw the axis")] = False,
         border: Annotated[bool, typer.Option(help="Whether to draw Brillouin zone border")] = True,
         dot: Annotated[bool, typer.Option(help="Whether to draw sampling points")] = False,
         line: Annotated[bool, typer.Option(help="Whether to draw contour lines")] = False,
         color: Annotated[str, typer.Option(help="(Default/depth/none/...) The color map to draw. (\"none\" to skip)")] = "Default",
         minus_fermi: Annotated[bool, typer.Option(help="Whether to set the Fermi energy to 0")] = True,
         save_name: Annotated[str, typer.Option(help="The name of the saved file")] = "Auto"):
    """
    plot the band of 2D material.
    """
    print_args(locals())
    if index == "Both":
        info("Start for VB ...")
        plot(sym=sym, index="VB", soc=soc, axis=axis, dot=dot, line=line, color=color, minus_fermi=minus_fermi,
             save_name=save_name)
        info("Start for CB ...")
        plot(sym=sym, index="CB", soc=soc, axis=axis, dot=dot, line=line, color=color, minus_fermi=minus_fermi,
             save_name=save_name)
        return
    sym = sym.lower()
    # 读取文件
    eigenval = Eigenval(soc=soc)
    # 获取数据
    points_df = eigenval.get_band(index=index)
    # 得到笛卡尔坐标
    points_df = ab_to_xy(points_df, sym=sym)
    # 转换格式
    points = np.array(points_df.loc[:, ["k_x", "k_y", "energy"]])
    # 获取最值
    max_point = points_df.loc[points_df['energy'].idxmax()]
    max_xy = (max_point.k_x, max_point.k_y)
    min_point = points_df.loc[points_df['energy'].idxmin()]
    min_xy = (min_point.k_x, min_point.k_y)
    if sym == "hex":  # 六角胞
        points = np.vstack((points, mirror(points)))  # 镜面对称
        points = np.vstack((points, rotate(points, angles=[60, 120, 180, 240, 300])))  # 旋转对称
    elif sym == "rec":  # 矩形胞
        points = np.vstack((points, mirror(points)))  # 镜面对称
        points = np.vstack((points, rotate(points, angles=[180])))  # 旋转对称
    else:
        raise NotImplementedError(f"Unsupported Symmetry {sym}")
    # 去除重复值
    points = np.unique(points, axis=0)
    # 生成数据
    x = points[:, 0]
    y = points[:, 1]
    e = points[:, 2]
    # 费密能级设置为 0
    if minus_fermi:
        fermi = get_fermi()
        e = e - fermi
    # 绘图
    fig, ax = plt.subplots()  # 创建画布
    ax.axis('equal')  # 长宽等比例
    from matplotlib.ticker import MultipleLocator
    ax.xaxis.set_major_locator(MultipleLocator(0.1))
    ax.yaxis.set_major_locator(MultipleLocator(0.1))
    if axis is False:
        ax.axis('off')  # 关闭数据轴
    # 修改字体
    import matplotlib.font_manager as fm
    available_fonts = fm.findSystemFonts()
    font_name = 'Times New Roman'
    if font_name in available_fonts:
        plt.rcParams["font.family"] = font_name
    # 修改字号
    config = {"font.size": 20,
              "mathtext.fontset": 'cm'}
    plt.rcParams.update(config)
    # 等高线
    if line:
        ax.tricontour(x, y, e, linewidths=0.5, colors='k')
    # 颜色映射
    if color == "Default":
        cmap = get_colormap("Excel-RYG")
    elif color == "depth":
        cmap = get_colormap("Depth")
    else:
        cmap = color
    if color != "none":
        data_layer = ax.tricontourf(x, y, e, levels=100, cmap=cmap)
        # 图例
        cbar = fig.colorbar(data_layer)
        cbar.outline.set_linewidth(1.5)
        # cbar.set_label("Energy",loc="bottom")
    # 布里渊区
    if border:
        添加外边缘(ax, sym=sym)
        添加能带路径(ax, sym=sym)
    # 数据点
    if dot:
        points_weight = points_df[points_df.weight != 0]
        points_noweight = points_df[points_df.weight == 0]
        # 有权重的 SCF 点
        ax.plot(
            points_weight.k_x,
            points_weight.k_y,
            markerfacecolor='lightgrey',
            color="#444444",
            marker="o",
            markersize=3,
            linestyle="None")
        # 无权重的能带点
        ax.plot(
            points_noweight.k_x,
            points_noweight.k_y,
            markerfacecolor='lightblue',
            color="#666666",
            marker="o",
            markersize=2,
            linestyle="None",
            markeredgewidth=0.5)
    # 特殊值
    console = Console()
    table = Table()
    table.add_column("Key")
    table.add_column("Value")
    if index == "VB":
        draw_dot(ax, max_xy, "VBM")
        table.title = "The data of VBM"
        for key, value in max_point.items():
            table.add_row(str(key), str(value))
        console.print(table)
    elif index == "CB":
        draw_dot(ax, min_xy, "CBM")
        table.title = "The data of CBM"
        for key, value in min_point.items():
            table.add_row(str(key), str(value))
        console.print(table)
    # 显示图片
    # plt.show(block=True)
    if save_name == "Auto":
        save_name = f"GlobalBand_{index}"
    plt.savefig(f"{save_name}.png", dpi=600)
    info(f"The picture was saved to {save_name}.png")


if __name__ == '__main__':
    plot(index="VB", soc=True, dot=True, sym="hex", axis=True)
    print("Finish!")
