import sys
import os
from shutil import rmtree
from subprocess import Popen
args = sys.argv[1:]

class globalVars:
    def __init__(self):
        self.indent = 0


def toPython(code):
    global toReturn
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
        toReturn = "print(" + " ".join(command_list[1:]) + ")"

    if main == "getinput":
        toReturn = "inputresult = input(" + " ".join(command_list[1:]) + ")"

    if "=" in command_list:
        toReturn = " ".join(command_list)

    if main == "IF":
        if not command_list[-1]=="THEN":
            toReturn = 'print(\"\\"THEN\\" expected\")'
        else:
            condition = command_list[1:-1]
            if len(condition) != 3 or not(condition[1] in ["<", "<=", "==", ">=", ">"]):
                toReturn = 'print("If then condition syntax must be: \\"IF <var> </<=/==/>=/> <var> THEN")'
            else:
                toReturn = 'if ' + " ".join(condition) + ": "
                globalVars().indent += 1

    return toReturn




if len(args) == 1:
    filename = args[0].split("/")[-1].split(".")[0]
    with open(filename + ".py", 'a+') as f:
        f.write("import socket\nimport os\nimport math\nimport sys\nhostname=socket.gethostname()\nhostip=socket.gethostbyname(hostname)\n")
    with open(args[0], 'r') as f:
        for line in f.readlines():
            toAppend = toPython(line.strip(" \n"))
            for i in range(globalVars().indent):
                toAppend = "\t" + toAppend
            with open(filename + ".py", 'a') as nf:
                nf.write(toAppend + "\n")

    compiletoSystem = Popen(["python3", "-m", "PyInstaller", filename + ".py", "--onefile", "--distpath", "."])
    compiletoSystem.wait()
    rmtree("build")
    os.remove(filename + ".spec"); os.remove(filename + ".py")
