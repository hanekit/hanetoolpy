from hanetoolpy.cui.options import print_options
from .global_band_plotter import plot as global_band_plotter
from functools import partial

vasp_option_dic = {
    "1": {"name": "Plot Global Band (VB)", "function": partial(global_band_plotter, index="VB")},
    "2": {"name": "Plot Global Band (CB)", "function": partial(global_band_plotter, index="CB")},
    "3": {"name": "Plot Global Band (VB) (SOC)", "function": partial(global_band_plotter, index="VB", soc=True)},
    "4": {"name": "Plot Global Band (CB) (SOC)", "function": partial(global_band_plotter, index="CB", soc=True)},
}

def vasp():
    print_options(vasp_option_dic)