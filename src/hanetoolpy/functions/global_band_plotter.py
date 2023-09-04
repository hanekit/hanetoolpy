#!/usr/bin/env python
import math
import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.patches import Polygon


class Eigenval:
    def __init__(self, path="./EIGENVAL"):
        self.path = path
        self.index_VB = None
        self.index_CB = None
        self.df = None
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
        self.index_VB = int(n_electrons / 2)
        self.index_CB = int(self.index_VB + 1)
        print(self.index_VB, self.index_CB)
        maindata = datalines[header_num:]
        data = []
        for kpoint_index in range(n_kpoints):
            kpoint_line_index = kpoint_index * n_loop
            kpoint_data = [float(string) for string in maindata[kpoint_line_index].split()]
            k_x, k_y, k_z = kpoint_data[:3]
            kpoint_weight = kpoint_data[3]
            for band_index in range(n_bands):  # 从 0 开始
                band_line_index = kpoint_line_index + 1 + band_index
                energy = [float(string) for string in maindata[band_line_index].split()][1]
                data.append([k_x, k_y, k_z, kpoint_weight, band_index, energy])
        self.df = pd.DataFrame(
            data, columns=["k_x", "k_y", "k_z", "kpoint_weight", "band_index", "energy"])

    def get_band(self, index, simple=False):
        if index == "VB":
            index = self.index_VB
        elif index == "CB":
            index = self.index_CB
        band_data = self.df[self.df["band_index"] == index - 1]
        if simple:
            return band_data
        else:
            return band_data.loc[:, ["k_x", "k_y", "energy"]]


def rotate_xy(xy, angle):
    """ 将 二维坐标 围绕原点旋转 angle 角度 """
    x, y = xy
    rad = np.radians(angle)
    rotation_matrix = np.array([[math.cos(rad), -math.sin(rad)],
                                [math.sin(rad), math.cos(rad)]])
    x2, y2 = np.dot(rotation_matrix, (x, y))
    return x2, y2


def ab_to_xy(points):
    new_points = []
    for point in points:
        x, y, z = point
        x2 = x + 0.5 * y
        y2 = (3 ** 0.5) / 2 * y
        new_point = (x2, y2, z)
        new_points.append(new_point)
    return new_points


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


def 生成六边形(length=1):
    # 计算六边形端点的坐标
    point_complex = length * np.sqrt(3) / 3 * np.exp(1j * np.pi * (1./6 + 1./3 * np.arange(7)))
    point_xy = np.c_[point_complex.real, point_complex.imag]
    # 创建六边形对象
    border = Polygon(point_xy,
                     lw=2,  # 线宽
                     edgecolor='black',  # 边缘颜色
                     clip_on=False,  # 允许绘制的图形超出绘图轴的范围
                     facecolor='none')  # 不填充内部，只绘制边缘
    return border


def 添加能带路径(ax):
    g = (0, 0)
    m = (0.5, 0)
    k = (0.5, 0.5/3**0.5)
    path = Polygon([g, m, k],
                   lw=2,  # 线宽
                   edgecolor='black',  # 边缘颜色为红色
                   clip_on=False,  # 允许绘制的图形超出绘图轴的范围
                   facecolor='none')  # 不填充多边形，只绘制边缘
    ax.add_patch(path)
    # 绘制高对称点
    ax.plot(*g, 'o', color="black")
    ax.plot(*m, 'o', color="black")
    ax.plot(*k, 'o', color="black")
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


def draw_dot(ax, xy, text):
    ax.plot(*xy, 'o', color="black", markerfacecolor='white')
    # 添加图例
    label_xy = (0.30, 0.52)
    ax.plot(*label_xy, 'o', color="black", markerfacecolor='white')
    ax.annotate(text,
                 xy=label_xy,
                 xycoords='data',
                 xytext=(12, -5),
                 textcoords='offset points',
                 fontsize=15)


def plot(index, dot=True, line=True, color=True, minus_fermi=True):
    # 读取文件
    eigenval = Eigenval()
    # 获取数据
    points = np.array(eigenval.get_band(index=index))
    # 转化为笛卡尔坐标
    points = np.array(ab_to_xy(points))
    # 获取最值
    e = points[:, 2]
    max_xy = points[np.argmax(e)][:2]
    min_xy = points[np.argmin(e)][:2]
    # 镜面对称
    points = np.vstack((points, mirror(points)))
    # 旋转对称
    points = np.vstack((points, rotate(points, angles=list(range(60, 360, 60)))))
    # 去除重复值
    points = np.unique(points, axis=0)
    print(points.shape)
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
    ax.axis('off')  # 关闭数据轴
    cmap = get_colormap()  # 生成色卡
    # 修改字体
    config = {"font.family": 'Times New Roman',
              "font.size": 20,
              "mathtext.fontset": 'cm'}
    plt.rcParams.update(config)
    # 数据点
    if dot:
        # ax.plot(x, y, 'ko', markersize=3)
        pass
    # 等高线
    if line:
        # ax.tricontour(x, y, e, linewidths=0.5, colors='k')
        pass
    # 颜色映射
    if color:
        data_layer = ax.tricontourf(x, y, e, levels=100, cmap=cmap)
    # 布里渊区
    外边缘 = 生成六边形()
    ax.add_patch(外边缘)
    添加能带路径(ax)
    # 特殊值
    if index == "VB":
        draw_dot(ax, max_xy, "VBM")
    elif index == "CB":
        draw_dot(ax, min_xy, "CBM")
    # 图例
    cbar = fig.colorbar(data_layer)
    cbar.outline.set_linewidth(1.5)
    # cbar.set_label("test",loc="bottom")
    # 显示图片
    # plt.show(block=True)
    plt.savefig("GlobalBand.png", dpi=600)


if __name__ == '__main__':
    plot(index="VB")
    print("Finish!")
