import pandas as pd
from rich import print
from rich.table import Table


class Eigenval:
    def __init__(self, path="./EIGENVAL", soc=False):
        self.path = path
        self.index_VB = None
        self.index_CB = None
        self.df = None
        self.soc = soc
        self.read()
        self.info = self.get_info()

    def print_table(self):
        table = Table(title="The data of bands")
        table.add_column("Key")
        table.add_column("Value")
        table.add_row("VB_index", str(self.index_VB))
        table.add_row("CB_index", str(self.index_CB))
        print(table)

    def read(self):
        header_num = 7
        with open(self.path, "r") as file:
            datalines = file.read().splitlines()
        band_info = datalines[5].split()
        n_electrons = int(band_info[0])
        n_kpoints = int(band_info[1])
        n_bands = int(band_info[2])
        n_loop = n_bands + 2  # 每一组数据的行数 = k点行+能带数+空行
        if self.soc:
            self.index_VB = int(n_electrons)
        else:
            self.index_VB = int(n_electrons / 2)
        self.index_CB = int(self.index_VB + 1)
        maindata = datalines[header_num:]
        data = []
        for kpoint_index in range(n_kpoints):
            kpoint_line_index = kpoint_index * n_loop
            kpoint_data = [float(string) for string in maindata[kpoint_line_index].split()]
            k_a, k_b, k_c = kpoint_data[:3]
            weight = kpoint_data[3]
            for band_index in range(n_bands):  # 从 0 开始
                band_line_index = kpoint_line_index + 1 + band_index  # maindata 中的行号
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

    def get_info(self):
        df = self.df
        line_vbm = df[df['band_index'] == self.index_VB - 1].nlargest(1, 'energy')
        line_cbm = df[df['band_index'] == self.index_CB - 1].nsmallest(1, 'energy')
        data = {
            "VB_index": self.index_VB,
            "CB_index": self.index_CB,
            "VBM_energy": line_vbm["energy"].iloc[0],
            "CBM_energy": line_cbm["energy"].iloc[0],
            "VBM_kabc": line_vbm[["k_a", "k_b", "k_c"]].values.flatten().tolist(),
            "CBM_kabc": line_cbm[["k_a", "k_b", "k_c"]].values.flatten().tolist(),
        }
        data["gap_type"] = "Direct" if (data["VBM_kabc"] == data["CBM_kabc"]) else "Indirect"
        data["gap_energy"] =  round(data["CBM_energy"] - data["VBM_energy"], 10)
        return data

    def print_info(self):
        info = self.info

        from rich.table import Table
        table = Table(title="Band edges\' quantities")
        table.add_column("Quantity", style="bold")
        table.add_column("VBM", justify="center")
        table.add_column("CBM", justify="center")

        table.add_row("Index",
                      str(info['VB_index']),
                      str(info['CB_index']))
        table.add_row("Energy",
                      "{:.6f}".format(info['VBM_energy']),
                      "{:.6f}".format(info['CBM_energy']))
        table.add_row("k_a",
                      "{:.8f}".format(info['VBM_kabc'][0]),
                      "{:.8f}".format(info['CBM_kabc'][0]))
        table.add_row("k_b",
                      "{:.8f}".format(info['VBM_kabc'][1]),
                      "{:.8f}".format(info['CBM_kabc'][1]))
        table.add_row("k_c",
                      "{:.8f}".format(info['VBM_kabc'][2]),
                      "{:.8f}".format(info['CBM_kabc'][2]))

        from rich import print
        print(table)


if __name__ == '__main__':
    eigenval = Eigenval()
    eigenval.print_info()
    data = eigenval.get_info()
    print(data)
