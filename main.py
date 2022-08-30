import sys
import os
from shutil import rmtree
from subprocess import Popen


args = sys.argv[1:]

def escape(string):
    toreturn=""
    for char in string:
        if char=="\"" or char=="(" or char==")":
            char=f"\\{char}"
            toreturn+=char
        else:
            toreturn+=char
    return toreturn


def shell():
    while True:
        cmd=input(">>> ")
        os.system(f"py {escape(toPython(cmd))}")

def compile():
    filename = args[0].split("/")[-1].split(".")[0]
    with open(filename + ".py", 'a+') as f:
        f.write(
            "import socket\nimport os\nimport math\nimport sys\nhostname=socket.gethostname("
            ")\nhostip=socket.gethostbyname(hostname)\n")
    with open(args[0], 'r') as f:
        for line in f.readlines():
            toAppend = toPython(line)
            with open(filename + ".py", 'a') as nf:
                nf.write(toAppend + "\n")

    compiletoSystem = Popen(["python3", "-m", "PyInstaller", filename + ".py", "--onefile", "--distpath", "."])
    compiletoSystem.wait()
    rmtree("build")
    os.remove(filename + ".spec")
    os.remove(filename + ".py")


def checkindent(code, indent=0):
    if code.startswith(" "):
        indent += 1
        code = code[1:]
        if code.startswith(" "):
            checkindent(code, indent=indent)
        else:
            return indent


def toPython(code):
    if code == "\n":
        return "\n"
    elif code.startswith("#addmod "):
        try:
            if code.split(" ")[1] == "libguimod\n":
                return "import tkinter as tk"
            else:
                return 'print(\"ERROR: No such module!\")'
        except IndexError:
            return 'print(\"ERROR: Syntax for adding module is \\"#addmod MODULE\\"\"'

    else:
        if checkindent(code) is None:
            indent = 0
        else:
            indent = checkindent(code)
        to_return = ""
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
            to_return = "print(" + " ".join(command_list[1:]) + ")"
        elif main == "getinput":
            to_return = "inputresult = input(" + " ".join(command_list[1:]) + ")"
        elif "=" in command_list:
            to_return = " ".join(command_list)
        elif main == "IF":
            if not command_list[-1] == "THEN":
                to_return = 'print(\"ERROR: \\"THEN\\" expected\")'
            else:
                condition = command_list[1:-1]
                if len(condition) != 3 or not (condition[1] in ["<", "<=", "==", ">=", ">"]):
                    to_return = 'print(\"ERROR: If then condition syntax must be: \\"IF <var> </<=/==/>=/> <var> ' \
                                'THEN\\"\")'
                else:
                    to_return = 'if ' + " ".join(condition) + ":"
        elif main == "ELSE":
            to_return = "else:"
        else:
            to_return = f"print('Command Not Found: {main}')"
        for i in range(indent):
            to_return = "\t" + to_return
        return to_return


if len(args)==0:
    shell()
elif len(args)==1:
    compile()
else:
    print("Sorry, but cpc can only handle one argument at this moment. ")