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

def compile():
    global origfilename
    origfilename = args[0].split("/")[-1]
    filename = args[0].split("/")[-1].split(".")[0]
    if os.path.isfile(origfilename):
        with open(filename + ".py", 'a+') as f:
            f.write(
                "import socket\nimport os\nimport math\nimport sys\nhostname=socket.gethostname("
                ")\nhostip=socket.gethostbyname(hostname)\nglobal args\nargs=sys.argv[1:]\n")
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
    else:
        print("ERROR: File not found")
        sys.exit(1)


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
        if open(origfilename).readline().rstrip().startswith("#addmod"):
            try:
                if code.split(" ")[1] == "libguimod\n":
                    global buttoncount, labelcount
                    buttoncount=0
                    labelcount=0
                    return "import tkinter as tk"
                else:
                    return 'print(\"ERROR: No such module!\")'
            except IndexError:
                return 'print(\"ERROR: Syntax for adding module is \\"#addmod MODULE\\"\"'
        else:
            return "print('ERROR: #addmod must be first line')"

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
            to_return = "print(f'" + " ".join(command_list[1:]) + "')"
        elif main == "getinput":
            to_return = "inputresult = input(f'" + " ".join(command_list[1:]) + "')"
        elif "=" in command_list:
            if "args" in command_list:
                to_return = "print('Taken Variable Name: args (used for arguments passed to program)')"
            else:
                to_return = " ".join(command_list)
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
        elif main == "WHILE":
            if not command_list[-1] == "DO":
                to_return = 'print(\"ERROR: \\"DO\\" expected\")'
            else:
                condition = command_list[1:-1]
                if len(condition) != 3 or not (condition[1] in ["<", "<=", "==", ">=", ">"]):
                    to_return = 'print(\"ERROR: While do condition syntax must be: \\"WHILE <var> </<=/==/>=/> <var> ' \
                                'DO\\"\")'
                else:
                    to_return = 'while ' + " ".join(condition) + ":"
        elif main == "BEGIN":
            if len(command_list) != 2:
                to_return = f"print('ERROR: Expected 1 argument {len(command_list)} passed.')"
            else:
                to_return = f"def {command_list[1]}(funcargs=None):"
        elif main == "FOR":
            if len(command_list) == 4 and command_list[2] == "IN":
                to_return = f"for {command_list[1]} in {command_list[3]}:"
        elif main == "FOREVER":
            to_return = 'while True:'
        elif main == "ELSE":
            to_return = "else:"
        elif main == "exit":
            if len(command_list) == 2:
                to_return = f"sys.exit({command_list[1]})"
            elif len(command_list) == 1:
                to_return = f"sys.exit()"
            else:
                to_return = "print('ERROR: Syntax of exit command: exit <exitcode (optional, default 0)>')"
        elif main == "runcmd":
            to_return = "os.system(f' + " ".join(command_list[1:]) + ')"
        elif main == "pause":
            if len(command_list) != 2:
                to_return = f"print('ERROR: 1 Argument expected but {len(command_list)} passed.')"
            else:
                to_return = f"time.sleep({command_list[1]})"
        elif main == "gui":
            if len(command_list) < 2:
                to_return = "print('ERROR: Expected 1 or more arguments but 0 passed.')"
            subcommand = command_list[1]
            if subcommand == "setup":
                if len(command_list) == 2:
                    to_return = "root = tk.Tk(className='nonamegui')\nroot.title('nonamegui')"
                else:
                    to_return = f"root = tk.Tk(className='{' '.join(command_list[2:])}')\nroot.title('{' '.join(command_list[2:])}')"
            elif subcommand == "run":
                if not len(command_list) > 2:
                    to_return = "root.mainloop()"
                else:
                    to_return = f"print('ERROR: 0 Arguments expected but {len(command_list)} passed.')"
            elif subcommand == "createbutton":
                cmdarg = command_list[2]
                textarg = " ".join(command_list[3:])
                if not cmdarg == "nocmd":
                    to_return = f"button{str(buttoncount)} = tk.Button(root, text=f'{textarg}', command={cmdarg})\nbutton{str(buttoncount)}.pack()"
                else:
                    to_return = f"button{str(buttoncount)} = tk.Button(root, text=f'{textarg}')\nbutton{str(buttoncount)}.pack()"
                buttoncount += 1
            elif subcommand == "createlabel":
                    textarg = " ".join(command_list[2:])
                    to_return = f"label{str(labelcount)} = tk.Label(root, text=f'{textarg}')\nlabel{str(labelcount)}.pack()"
                
        else:
            to_return = f"print('Command Not Found: {main}')"
        for i in range(indent):
            to_return = "\t" + to_return
        return to_return


if len(args)==0:
    print("Required Argument: <filename>")
    sys.exit(1)
elif len(args)==1:
    compile()
else:
    print(f'ERROR: 1 Argument expected but {len(args)} passed.')
    sys.exit(1)