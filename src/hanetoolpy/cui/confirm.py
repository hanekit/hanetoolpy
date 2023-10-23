import os
import pyinputplus as pyip


def confirm(prompt, default=None):
    prompt = f"{prompt} (default:{default}) (y/n) : "
    in_pbs = os.environ.get("PBS_O_WORKDIR")

    if in_pbs != None:
        print(prompt + "y (Detected in pbs process, automatically confirmed.)")
        return True

    if default == None:
        response = pyip.inputYesNo(prompt)
    else:
        response = pyip.inputYesNo(prompt, blank=True)

    if response == "":
        return default
    else:
        return response == "yes"

if __name__ == '__main__':
    for i in range(10):
        result = confirm("Confirm to submit this job?", default=True)
        print(result)
