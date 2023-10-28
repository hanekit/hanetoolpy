class Eigenval:
    def __init__(self, path="./EIGENVAL", soc=False):
        self.path = path
        self.index_VB = None
        self.index_CB = None
        self.df = None
        self.soc = soc
        self.read()

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