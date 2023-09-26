import pyinputplus as pyip


def confirm(prompt, default=None):
    prompt = f"{prompt} (default:{default}) (y/n) : "
    if default == None:
        response = pyip.inputYesNo(prompt)
    else:
        response = pyip.inputYesNo(prompt, blank=True)
    if response == "":
        return default
    else:
        return response == "yes"

if __name__ == '__main__':
    while True:
        result = confirm("Confirm to submit this job?", default=True)
