import typer


def add_commands(parent):
    # 添加 vasp 命令
    vasp = typer.Typer(no_args_is_help=True,
                       invoke_without_command=True)
    parent.add_typer(vasp, name="vasp", help="VASP tools")

    # 添加 vasp 子命令
    from hanetoolpy.functions.vasp_run import vasp_run
    vasp.command("run")(vasp_run)
    from hanetoolpy.functions.vasp import check_vasp_end
    vasp.command("check_end")(check_vasp_end)
    from hanetoolpy.functions.vasp_stop import vasp_stop
    vasp.command("stop", no_args_is_help=True)(vasp_stop)
    from hanetoolpy.functions.global_band_plotter import plot as f101
    vasp.command("f101")(f101)
    from hanetoolpy.functions.ebs_unfold_plotter import main as f102
    vasp.command("f102")(f102)

    # 添加 vaspkit 命令
    vaspkit = typer.Typer(no_args_is_help=True,
                          invoke_without_command=True)
    parent.add_typer(vaspkit, name="vaspkit", help="VASPKIT tools")

    # 添加 vaspkit 子命令
    from hanetoolpy.functions.vaspkit import vaspkit_281
    vaspkit.command("f281")(vaspkit_281)

    # 添加 thirdorder 命令
    thirdorder = typer.Typer(no_args_is_help=True,
                             invoke_without_command=True)
    parent.add_typer(thirdorder, name="thirdorder", help="thirdorder tools")

    # 添加 thirdorder 子命令
    from hanetoolpy.functions.thirdorder import main as thirdorder_f101
    thirdorder.command("f101")(thirdorder_f101)
    from hanetoolpy.functions.thirdorder import \
        check_thirdorder_jobs as thirdorder_f102
    thirdorder.command("f102")(thirdorder_f102)
    from hanetoolpy.functions.thirdorder import \
        organize_files as thirdorder_f103
    thirdorder.command("f103")(thirdorder_f103)

    # phonopy
    phonopy = typer.Typer(no_args_is_help=True,
                          invoke_without_command=True)
    parent.add_typer(phonopy, name="phonopy", help="phonopy tools")

    # phonopy 子命令
    from hanetoolpy.functions.rms import main as rms
    phonopy.command("rms")(rms)
