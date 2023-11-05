def grep_get(path, text: str, order: int):
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if text in line:
                return line.split()[order]
