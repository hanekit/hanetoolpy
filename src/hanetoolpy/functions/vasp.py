from hanetoolpy.cui.options import print_options
from .global_band_plotter import plot as global_band_plotter
from functools import partial

vasp_option_dic = {
    "1": {"name": "Plot Global Band", "function": partial(global_band_plotter, index="VB")},
}

def vasp():
    print_options(vasp_option_dic)