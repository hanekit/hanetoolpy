from hanetoolpy.cui.options import print_options
from .global_band_plotter import plot as global_band_plotter
from functools import partial

vasp_option_dic = {
    "1": {"name": "Plot Global Band (VB)", "function": partial(global_band_plotter, index="VB")},
    "2": {"name": "Plot Global Band (CB)", "function": partial(global_band_plotter, index="CB")},
}

def vasp():
    print_options(vasp_option_dic)