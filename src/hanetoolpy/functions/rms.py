import numpy as np
import pandas as pd


def get_distance(atom_a, atom_b):
    from pymatgen.core import Structure
    structure = Structure.from_file("SPOSCAR")
    atom_a_abc = structure[int(atom_a)-1].frac_coords
    atom_b_abc = structure[int(atom_b)-1].frac_coords
    diff_abc = []
    for i in range(3):
        diff_i = float(atom_b_abc[i])-float(atom_a_abc[i])
        # 去除周期性
        if diff_i > 0.5:
            diff_i = diff_i - 1
        elif diff_i < -0.5:
            diff_i = diff_i + 1
        diff_abc.append(diff_i)
    diff_xyz = structure.lattice.get_cartesian_coords(diff_abc)
    diff_xyz = np.array(diff_xyz)
    distance = np.sqrt(np.sum(diff_xyz ** 2))
    return distance


def read_force_constants(path='FORCE_CONSTANTS'):
    # 读取文件
    with open(path, 'r') as file:
        lines = file.readlines()
    # 去除首行，后每 4 行为一组
    data_groups = [" ".join(lines[i:i+4]) for i in range(1, len(lines), 4)]
    # 分列每组数据，得到二维列表
    data_list = [i.split() for i in data_groups]
    # 创建 DataFrame
    tensor = ['xx', 'xy', 'xz',
              'yx', 'yy', 'yz',
              'zx', 'zy', 'zz']
    columns = ['atom_a', 'atom_b'] + tensor
    df = pd.DataFrame(data_list, columns=columns)
    # 计算 RMS
    rms = (df[tensor].apply(lambda row: row.astype(float).pow(2)).sum(axis=1) / 9 ) ** 0.5
    df['rms'] = rms
    return df


def get_rms():
    df = read_force_constants()
    df['distance'] = df.apply(lambda row: get_distance(row['atom_a'], row['atom_b']), axis=1)
    return df

def plot_rms(df):
    import matplotlib.pyplot as plt
    x = df['distance']
    y = df['rms']
    plt.save()
    return plt

def main():
    df = get_rms()
    df[['distance','rms']].to_csv("rms.csv")
    plot_rms(df)
    plt.save("rms.png")


if __name__ == '__main__':
    df = get_rms()
    df[['distance','rms']].to_csv("rms.csv")
    plt = plot_rms(df)
    plt.save("rms.png")
    from pandasgui import show
    show(df)
