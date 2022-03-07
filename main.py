import sys
import os
import PyInstaller.__main__
from shutil import rmtree
import contextlib
args = sys.argv[1:]


def toPython(code):
    tmp = list(code)
    tmp1 = []
    for item in tmp:
        if item != "\\":
            tmp1.append(item)
        else:
            tmp1.append("escape")
    for item in tmp1:
        if item == "escape":
            i = tmp1.index(item)
            del tmp1[i]
            del tmp1[i]
    command_list = "".join(tmp1).split()
    main = command_list[0]
    del tmp, tmp1

    if main == "putln":
        if len(command_list) != 2:
            pass
        else:
            return "print(" + command_list[1] + ")"


if not len(args) == 0:
    with open(args[0], 'r') as f:
        for line in f.readlines():
            toAppend = toPython(line.strip(" \n"))
            with open("temp.py", 'a') as f:
                f.write(toAppend + "\n")

    with contextlib.redirect_stdout(None):
        PyInstaller.__main__.run(["temp.py", "--onefile", "--distpath", "."])
    rmtree("build")
    os.remove("temp.spec"); os.remove("temp.py")
