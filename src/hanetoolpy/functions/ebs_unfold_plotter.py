import os

import matplotlib.pyplot as plt
import pandas as pd
import typer
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib.ticker import MultipleLocator
from typing_extensions import Annotated

plt.rcParams["font.family"] = "Times New Roman"
# plt.rcParams['axes.unicode_minus'] = True
config = {"font.family": 'Times New Roman',
          "font.size": 8,
          "mathtext.fontset": 'cm'}
plt.rcParams.update(config)


def read_pband_elements(root_dir=None, path: str = "./PBAND_ELEMENTS.dat"):
    if root_dir is not None:
        path = os.path.join(root_dir, path)
    else:
        path = os.path.abspath(path)

    with open(path, 'r') as file:
        line = file.readlines()[0]
    atoms = line.split()[2:]
    return atoms


class KlabelData:
    """
    读取 KLABELS.txt 文件，返回 *.labels 和 *.index 列表
    """

    def __init__(self, root_dir=None, path: str = "./KLABELS.txt"):
        if root_dir is not None:
            self.path = os.path.join(root_dir, path)
        else:
            self.path = os.path.abspath(path)
        self.labels = []
        self.indexs = []
        self.read()

    def read(self):
        with open(self.path, 'r') as file:
            lines = file.readlines()[1:-1]
        self.labels.clear()
        self.indexs.clear()
        for line in lines:
            if line.strip():  # 如果不是空行
                klabel, kindex = line.split()
                klabel = klabel.replace("GAMMA", "Γ")
                self.labels.append(klabel)
                self.indexs.append(float(kindex))


def read_dat(path: str,
             quantity_list: list = None,
             show: bool = False) -> pd.DataFrame:
    """
    从 *.dat 文件中读取能带数据储存在 DataFrame 表格中
    """
    # 读取文件
    with open(path, 'r') as f:
        lines = f.readlines()
    # 过滤空行和以 "#" 开头的行
    lines = [line.strip() for line in lines if line.strip()
             and not line.startswith('#')]
    # 转化为 DataFrame 格式
    data_table = pd.DataFrame([line.split() for line in lines]).astype(float)
    # 去除重复行
    data_table = data_table.drop_duplicates()
    # 指定列名
    if quantity_list is not None:
        data_table.columns = quantity_list
    # 可视化显示
    if show == True:
        pandasgui.show(data_table)
    # 返回值
    return data_table


def read_ebs_dat(path: str = "./EBS.dat"):
    """
    从 EBS.dat 文件中读取能带数据储存在 DataFrame 表格中
    """
    quantity_list = ['K-Path', 'Energy', 'Weight']
    return read_dat(path=path, quantity_list=quantity_list)


def read_band_dat(path: str = "./BAND.dat"):
    """
    从 Band.dat 文件中读取能带数据储存在 DataFrame 表格中
    """
    quantity_list = ['K-Path', 'Energy']
    return read_dat(path=path, quantity_list=quantity_list)


def subplots_border_adjust(subplot, border=5, left=20, right=0, bottom=20, top=0):
    """
    调整 subplot 的外边距
    """
    border_l = 0 + (border + left) / 100
    border_r = 1 - (border + right) / 100
    border_b = 0 + (border + bottom) / 100
    border_t = 1 - (border + top) / 100
    subplot.subplots_adjust(left=border_l, right=border_r,
                            bottom=border_b, top=border_t)


def subplots_axis_adjust(ax):
    # 主刻度
    ax.tick_params(which='major', axis='both', length=5,
                   direction='in', labelsize=10)
    # ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1.0))
    # 修改小数位数，但是会导致负号显示错误
    # formatter = ticker.FormatStrFormatter(f'%.1f')
    # ax.yaxis.set_major_formatter(formatter)
    # 次刻度
    ax.tick_params(which='minor', axis='both', length=2, direction='in')
    # ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(0.2))
    # 标题
    # ax.set_xlabel('K-Path', fontsize=10)
    ax.set_ylabel('Energy (eV)', fontsize=10)
    # 范围
    # ax.set_xlim(0, 2)
    ax.set_ylim(-2.5, 2.5)
    # 绘制辅助线
    ax.axhline(0, color='grey', linestyle='dashed', linewidth=0.5, zorder=0)


def set_klabels(ax, klabel_data):
    indexs = klabel_data.indexs
    labels = klabel_data.labels
    ax.set_xticks(indexs, labels)
    ax.set_xlim(indexs[0], indexs[-1])


def draw_klabel_lines(ax, kindexs):
    for index in kindexs:
        ax.axvline(index, color='black', linestyle='solid',
                   linewidth=0.8, zorder=0)


def main(cbar: Annotated[bool, typer.Option(help="Whether to draw the colorbar")] = True,
         color: Annotated[str, typer.Option(help="")] = "#4E64A2"):
    """
    plot the EBS of supercell.
    """
    # 所需输入文件
    input_files = ["BAND_KLABELS.txt",
                   "EBS.dat",
                   "BAND.dat"]
    # 建立画布
    if cbar:
        import matplotlib.gridspec as gridspec
        fig = plt.figure(figsize=(3, 3))
        gs = gridspec.GridSpec(1, 2, width_ratios=[15, 1])
        ax = plt.subplot(gs[0])
        ax_cbar = plt.subplot(gs[1])
    else:
        fig, ax = plt.subplots(figsize=(3, 3))  # 3 inch = 7.62 cm
    # 设置数据
    root_dir = R"./"
    save_path = R"EBS-unfold-output.png"
    # 设置 x 轴
    klabels = KlabelData(root_dir=root_dir, path="BAND_KLABELS.txt")
    # 设置
    draw_klabel_lines(ax, kindexs=klabels.indexs)
    set_klabels(ax, klabels)
    # 读取数据
    band_dat = read_band_dat(os.path.join(root_dir, "BAND.dat"))
    ebs_dat = read_ebs_dat(os.path.join(root_dir, "EBS.dat"))
    # 绘制基础能带图
    x = band_dat['K-Path'].values
    y = band_dat['Energy'].values
    ax.plot(x, y,
            color='black',
            linestyle='--',
            linewidth=0.6,
            alpha=0.8)
    # 绘制有效能带图
    x = ebs_dat['K-Path'].values
    y = ebs_dat['Energy'].values
    w = ebs_dat['Weight'].values
    width = [x[i]-x[i-1] for i in range(len(x))]
    width = width[0:] + width[-1:]

    # 透明度加工
    # points = np.array([[0, 0], [0.4, 0], [0.5, 1], [
    #     0.6, 1], [0.7, 1], [1, 1]])  # 控制点坐标
    # from utils.bazier import bezier_function
    # w = [bezier_function(i,points) for i in w]
    # w = [min(1, i*1.5) for i in w]

    # 创建长方形对象
    rect_width = 0.055  # 长方形的宽度
    rect_height = 0.08  # 长方形的高度
    rectangles = [Rectangle((x[i]-rect_width/2, y[i]-rect_height/2),
                            width[i],
                            rect_height,
                            ) for i in range(len(x))]
    # 绘制散点图
    collection = PatchCollection(rectangles,
                                 # facecolor="yellow",
                                 facecolor=color,
                                 alpha=w)
    ax.add_collection(collection)
    # 绘制图例
    import matplotlib as mpl
    from matplotlib.colors import LinearSegmentedColormap

    # 创建自定义 colormap
    cmap = LinearSegmentedColormap.from_list(
        'custom_colormap', [(0.0, f'{color}00'), (1.0, f'{color}FF')])
    # 设置轴
    subplots_axis_adjust(ax)
    # 设置边距
    subplots_border_adjust(subplot=fig, top=5, left=12, bottom=5)
    # 绘制 colorbar
    if cbar:
        cbar_cmap = LinearSegmentedColormap.from_list(
            'custom_colormap', [(0.0, '#FFFFFF'), (1.0, color)])
        cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=cbar_cmap),
                            cax=ax_cbar, orientation='vertical')
        subplots_border_adjust(subplot=fig, top=5, left=12, right=5, bottom=5)
    else:
        subplots_border_adjust(subplot=fig, top=5, left=12, right=0, bottom=5)
    # 设置背景颜色
    # ax.set_facecolor('darkblue')
    # 保存图片为PNG格式
    savepath = os.path.join(root_dir, save_path)
    plt.savefig(fname=savepath, dpi=900,
                # transparent=True,
                # pil_kwargs=dict(optimize=True)
                )
    # plt.show()
    print("Finish!")


if __name__ == "__main__":
    main()
