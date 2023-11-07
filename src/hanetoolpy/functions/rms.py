import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


tensor = ["xx", "xy", "xz",
          "yx", "yy", "yz",
          "zx", "zy", "zz"]


def get_distance(structure, atom_a, atom_b):
    # 获取分数坐标
    atom_a_abc = structure[int(atom_a)-1].frac_coords
    atom_b_abc = structure[int(atom_b)-1].frac_coords
    # 计算分数坐标差
    diff_abc = []
    for i in range(3):
        diff_i = float(atom_b_abc[i])-float(atom_a_abc[i])
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
    data_groups = [" ".join(lines[i:i+4]) for i in range(1, len(lines), 4)]
    # 分列每组数据，得到二维列表
    data_list = [i.split() for i in data_groups]
    # 创建 DataFrame
    columns = ["atom_a", "atom_b"] + tensor
    df = pd.DataFrame(data_list, columns=columns)
    return df


def plot_rms(df, order):
    x = df["distance"]
    y = df["rms"]
    plt.scatter(x, y)
    if order:
        # TODO
        pass
    return plt


def main(path: str = "FORCE_CONSTANTS",
         plot: bool = True,
         order: bool = False,
         savename: str = "hanetoolpy-RMS_of_2FC"):
    """
    Calculate and plot the root mean square (RMS) of FORCE_CONSTANTS.

    \b
    Required files:
    | FORCE_CONSTANTS
    | SPOSCAR
    \b
    Output files:
    | rms.csv
    | rms.png
    """
    # 读取文件
    logging.info("(1/4) Reading FORCE_CONSTANTS ...")
    df = read_force_constants(path)
    # 计算 RMS
    logging.info("(2/4) Calculating RMS ...")
    df["rms"] = (df[tensor].apply(lambda row: row.astype(float).pow(2)).sum(axis=1) / 9) ** 0.5
    # 计算距离
    logging.info("(3/4) Calculating atom distance ...")
    from pymatgen.core import Structure
    structure = Structure.from_file("SPOSCAR")
    df["distance"] = df.apply(lambda row: get_distance(
        structure, row["atom_a"], row["atom_b"]), axis=1)
    # 输出结果
    logging.info("(4/4) Saving the results ...")
    df[["distance", "rms", "atom_a", "atom_b"]].to_csv(f"{savename}.csv", index=False)
    logging.info(f"{savename}.csv saved.")
    if plot:
        plot_rms(df, order)
        plt.savefig(f"{savename}.png")
        logging.info(f"{savename}.png saved.")
    # 结束
    logging.info("Finish!")


if __name__ == '__main__':
    main()
