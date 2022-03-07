import sys
import os
from shutil import rmtree
from subprocess import Popen
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
        return "print(" + " ".join(command_list[1:]) + ")"

    if main == "getinput":
        return "inputresult = input(" + " ".join(command_list[1:]) + ")"

    if "=" in command_list:
        return " ".join(command_list)




if len(args) == 1:
    filename = args[0].split("/")[-1].split(".")[0]
    with open(filename + ".py", 'a+') as f:
        f.write("import socket\nimport os\nimport math\nimport sys\nhostname=socket.gethostname()\nhostip=socket.gethostbyname(hostname)\n")
    with open(args[0], 'r') as f:
        for line in f.readlines():
            toAppend = toPython(line.strip(" \n"))
            with open(filename + ".py", 'a') as f:
                f.write(toAppend + "\n")

    compiletoSystem = Popen(["python", "-m", "PyInstaller", filename + ".py", "--onefile", "--distpath", "."])
    compiletoSystem.wait()
    rmtree("build")
    os.remove(filename + ".spec"); os.remove(filename + ".py")
