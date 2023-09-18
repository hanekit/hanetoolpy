#!/usr/bin/env python
import typer
from typing_extensions import Annotated
import math
import numpy as np
import pandas as pd

import logging
from logging import info
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from rich.console import Console
from rich.table import Table

matplotlib.use('Agg')
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)-s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Eigenval:
    def __init__(self, path="./EIGENVAL", soc=False):
        self.path = path
        self.index_VB = None
        self.index_CB = None
        self.df = None
        self.soc = soc
        self.read()
        pass

    def read(self):
        header_num = 7
        with open(self.path, "r") as file:
            datalines = file.read().splitlines()
        band_info = datalines[5].split()
        n_electrons = int(band_info[0])
        n_kpoints = int(band_info[1])
        n_bands = int(band_info[2])
        n_loop = n_bands + 2
        if self.soc:
            self.index_VB = int(n_electrons)
        else:
            self.index_VB = int(n_electrons / 2)
        self.index_CB = int(self.index_VB + 1)
        console = Console()
        table = Table(title="The data of bands")
        table.add_column("Key")
        table.add_column("Value")
        table.add_row("VB_index", str(self.index_VB))
        table.add_row("CB_index", str(self.index_CB))
        console.print(table)
        maindata = datalines[header_num:]
        data = []
        for kpoint_index in range(n_kpoints):
            kpoint_line_index = kpoint_index * n_loop
            kpoint_data = [float(string) for string in maindata[kpoint_line_index].split()]
            k_a, k_b, k_c = kpoint_data[:3]
            weight = kpoint_data[3]
            for band_index in range(n_bands):  # 从 0 开始
                band_line_index = kpoint_line_index + 1 + band_index
                energy = [float(string) for string in maindata[band_line_index].split()][1]
                data.append([k_a, k_b, k_c, weight, band_index, energy])
        self.df = pd.DataFrame(
            data, columns=["k_a", "k_b", "k_c", "weight", "band_index", "energy"])
        self.df['band_index'] = self.df['band_index'].astype(int)

    def get_band(self, index, simple=False):
        if index == "VB":
            index = self.index_VB
        elif index == "CB":
            index = self.index_CB
        band_data = self.df[self.df["band_index"] == int(index) - 1]
        if not simple:
            return band_data
        else:
            return band_data.loc[:, ["k_a", "k_b", "energy"]]


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


def get_colormap():
    from matplotlib.colors import LinearSegmentedColormap
    colors = ['#F8696B', '#FFEB84', '#63BE7B']  # 颜色
    positions = [0.0, 0.5, 1.0]  # 颜色位置
    # 生成色卡
    colormap = LinearSegmentedColormap.from_list('custom_colormap', list(zip(positions, colors)))
    return colormap


def get_fermi(path="./FERMI_ENERGY"):
    with open(path, "r") as file:
        dataline = file.readlines()
        fermi = float(dataline[1].split()[0])
    return fermi


def 添加外边缘(ax, sym):
    length = 1
    if sym == "hex":  # 六角胞
        point_complex = length * np.sqrt(3) / 3 * np.exp(1j * np.pi * (1. / 6 + 1. / 3 * np.arange(7)))
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
         color: Annotated[str, typer.Option(help="(Default/Depth/None/...) The color map to draw. (\"None\" to skip)")] = "Default",
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
        config = {"font.family": font_name}
        plt.rcParams.update(config)
    # 修改字号
    config = {"font.size": 20,
              "mathtext.fontset": 'cm'}
    plt.rcParams.update(config)
    # 等高线
    if line:
        ax.tricontour(x, y, e, linewidths=0.5, colors='k')
    # 颜色映射
    if color == "Default":
        cmap = get_colormap()  # 生成色卡
    elif color == "Depth":
        cmap = "Greys"
    else:
        cmap = color
    if color != "None":
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
