import logging
from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import typer
from typing_extensions import Annotated

tensor = ["xx", "xy", "xz",
          "yx", "yy", "yz",
          "zx", "zy", "zz"]


def get_distance(structure, atom_a, atom_b):
    # 获取分数坐标
    atom_a_abc = structure[int(atom_a) - 1].frac_coords
    atom_b_abc = structure[int(atom_b) - 1].frac_coords
    # 计算分数坐标差
    diff_abc = []
    for i in range(3):
        diff_i = float(atom_b_abc[i]) - float(atom_a_abc[i])
        # 去除周期性
        if diff_i > 0.5:
            diff_i = diff_i - 1
        elif diff_i < -0.5:
            diff_i = diff_i + 1
        diff_abc.append(diff_i)
    # 计算物理坐标差
    diff_xyz = structure.lattice.get_cartesian_coords(diff_abc)
    # 计算距离
    diff_xyz = np.array(diff_xyz)
    distance = np.sqrt(np.sum(diff_xyz ** 2))
    return distance


def read_force_constants(path="FORCE_CONSTANTS"):
    # 读取文件
    with open(path, "r") as file:
        lines = file.readlines()
    # 去除首行，后每 4 行为一组
    data_groups = [" ".join(lines[i:i + 4]) for i in range(1, len(lines), 4)]
    # 分列每组数据，得到二维列表
    data_list = [i.split() for i in data_groups]
    # 创建 DataFrame
    columns = ["atom_a", "atom_b"] + tensor
    df = pd.DataFrame(data_list, columns=columns)
    return df


def plot_rms(df, order=False, poscar=None, supercell=None):
    x = df["distance"]
    y = df["rms"]
    plt.scatter(x, y, marker='+', s=50, alpha=1)
    if order:
        import numpy as np

        from hanetoolpy.functions.thirdorder import get_order_distance
        result = get_order_distance(poscar, supercell)
        order = np.array(list(result.keys()))
        distance = np.array(list(result.values())) * 10
        text_y_list = np.linspace(0.9, 0.2, len(result)) * max(y)
        for order, distance in result.items():
            plt.axvline(distance * 10, color='grey', linestyle='--', label='order', linewidth=0.8)
            plt.text(distance * 10 + 0.1, text_y_list[order],
                     order, ha='left', va='center', color='grey')
    plt.xlabel('Distance (Ang)')
    plt.ylabel('RMS')
    return plt


def rms(
        workdir: Annotated[
            str,
            typer.Option("--workdir", "-d")] \
                = "./",
        plot: Annotated[
            bool,
            typer.Option()] \
                = True,
        savename: Annotated[
            str,
            typer.Option("--savename", "-s")] \
                = "hanetoolpy-RMS_of_2FC",
        order: Annotated[
            bool,
            typer.Option(rich_help_panel="Order arguments",
                         help="Draws order vertical lines")] \
                = False,
        supercell: Annotated[
            Tuple[int, int, int],
            typer.Option("--supercell", "--sc",
                         rich_help_panel="Order arguments",
                         metavar="[INT * 3]",
                         help="Size of supercell")] \
                = (0, 0, 0),
):
    """
    Calculate and plot the root-mean-square (RMS) of FORCE_CONSTANTS.

    \b
    Required files:
    | FORCE_CONSTANTS
    | SPOSCAR
    Optional files:
    | POSCAR
    Output files:
    | hanetoolpy-RMS_of_2FC.csv
    | hanetoolpy-RMS_of_2FC.png
    """
    # 读取文件
    workdir = Path(workdir).resolve()
    logging.info("(1/4) Reading FORCE_CONSTANTS ...")
    df = read_force_constants(workdir / "FORCE_CONSTANTS")
    # 计算 RMS
    logging.info("(2/4) Calculating RMS ...")
    df["rms"] = (df[tensor].apply(lambda row: row.astype(float).pow(2)).sum(axis=1) / 9) ** 0.5
    # 计算距离
    logging.info("(3/4) Calculating atom distance ...")
    from pymatgen.core import Structure
    structure = Structure.from_file(workdir / "SPOSCAR")
    df["distance"] = df.apply(lambda row: get_distance(
        structure, row["atom_a"], row["atom_b"]), axis=1)
    # 输出结果
    logging.info("(4/4) Saving the results ...")
    df[["distance", "rms", "atom_a", "atom_b"]].to_csv(workdir / f"{savename}.csv", index=False)
    logging.info(f"{savename}.csv saved.")
    if order and supercell == (0, 0, 0):
        logging.error("if order is True, please input the --supercell.")
        quit()
    if plot:
        plot_rms(df, order, poscar=workdir / "POSCAR", supercell=supercell)
        plt.savefig(workdir / f"{savename}.png")
        logging.info(f"{savename}.png saved.")
    # 结束
    logging.info("Finish!")


if __name__ == '__main__':
    rms(workdir="../test_files/rms", order=True)
