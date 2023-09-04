def print_options(option_dic):
    for key, value in option_dic.items():
        name = value["name"]
        print(f"({key}) {name}")
    option = input(" ------------>>\n")
    try:
        option_dic[option]["function"]()
    except KeyError:
        print("Error: 非法参数，请重新输入。")
        print_options()
