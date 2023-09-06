from hanetoolpy.cui.options import print_options
from .global_band_plotter import plot as global_band_plotter
from functools import partial

sym = "hex"

vasp_option_dic = {
    "1": {"name": "Plot Global Band (VB)", "function": partial(global_band_plotter, index="VB", sym=sym)},
    "2": {"name": "Plot Global Band (CB)", "function": partial(global_band_plotter, index="CB", sym=sym)},
    "3": {"name": "Plot Global Band (VB) (SOC)", "function": partial(global_band_plotter, index="VB", sym=sym, soc=True)},
    "4": {"name": "Plot Global Band (CB) (SOC)", "function": partial(global_band_plotter, index="CB", sym=sym, soc=True)},
}


def vasp():
    print_options(vasp_option_dic)
