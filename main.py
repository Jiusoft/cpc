import os, sys, shutil, platform

args = sys.argv[1:]
global funcs
funcs = []

def help():
    print('cpc version 2.0.0\nCopyright (c) 2022 Jiusoft\nUsage: cpc <filename>\n\nArguments:\n\t-h, -H or --help: Display this help message')

def compile():
    global origfilename
    skipappend=False
    origfilename = args[0].split('/')[-1]
    filename = args[0].split('/')[-1].split('.')[0]
    if os.path.isfile(args[0]):
        with open(filename + '.py', "a+") as f:
            f.write(
                'import socket\nimport os\nimport time\nimport sys\nhostname=socket.gethostname('
                ')\nhostip=socket.gethostbyname(hostname)\nglobal args\nargs=sys.argv[1:]\nif len(args) > 9:\n\tprint("Application Crashed: Too much arguments to handle."); sys.exit(1)\nelse:\n\tfor n in range(len(args), 9):\n\t\targs.append("")\narg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9 = args\ndel args\n')
        with open(args[0], "r") as f:
            for line in f.readlines():
                if line.startswith('//'):
                    skipappend=True
                else:
                    skipappend=False
                line = line.split('//')[0]
                toAppend = toPython(line) if not skipappend else ''
                with open(filename + '.py', "a") as nf:
                    nf.write(toAppend + '\n')

        if platform.system() == "Linux" or platform == "Darwin":
            os.system(f"python3 -m PyInstaller --onefile --distpath . {filename}.py")
        elif platform.system() == "Windows":
            os.system(f"python -m PyInstaller --onefile --distpath . {filename}.py")
        shutil.rmtree('build')
        os.remove(filename + '.spec')
        os.remove(filename + '.py')
    else:
        print('ERROR: File not found')
        sys.exit(1)

def checkindent(code, indent=0):
    if code.startswith(' '):
        indent += 1
        code = code[1:]
        if code.startswith(' '):
            checkindent(code, indent=indent)
        else:
            return indent

def toPython(code):
    if checkindent(code) is None:
        indent = 0
    else:
        indent = checkindent(code)
    to_return = ''
    command_list = code.strip(' \n').split(' ')
    main = command_list[0]
    if code == '' or code == '\n':
        return '\n'
    elif main == '#addmod':
        global imported
        imported = []
        if len(command_list) > 2:
            to_return = "print(\'ERROR: Syntax for adding module is \\'#addmod MODULE\\'\'"
        else:
            if command_list[1] == 'libguimod' or code.split(' ')[1] == 'libguimod\n':
                global buttoncount, labelcount
                buttoncount=0
                labelcount=0
                imported.append('libguimod')
                to_return = 'import tkinter as tk'
            elif command_list[1] == 'libfilemod' or code.split(' ')[1] == 'libfilemod\n':
                imported.append('libfilemod')
                to_return = ''
            else:
                print(command_list)
                return "print(\'ERROR: No such module!\')"
    elif main == 'putln':
        to_return = 'print(f"' + ' '.join(command_list[1:]) + '")'
    elif main == 'getinput':
        spaces = 0
        while code.endswith(' ') or code.endswith(' \n'):
            if code.endswith(' '):
                spaces += 1
                code = code[:-1]
            elif code.endswith(' \n'):
                spaces += 1
                code = code[:-2]
        to_return = 'inputresult = input(f"' + ' '.join(command_list[1:])
        for _ in range(spaces):
            to_return += ' '
        to_return += '")'
    elif '=' in command_list:
        if len(command_list[:command_list.index('=')]) > 2:
            to_return = f'print("Variable name can only be one word.")'
        elif command_list[1] == 'arg1' or command_list[1] == 'arg2' or command_list[1] == 'arg3' or command_list[1] == 'arg4' or command_list[1] == 'arg5' or command_list[1] == 'arg6' or command_list[1] == 'arg7' or command_list[1] == 'arg8' or command_list[1] == 'arg9':
            to_return = f'print("Taken Variable Name: {command_list[1]}'
        elif command_list[1] == 'hostname':
            to_return = f'print("Taken Variable Name: {command_list[1]}'
        elif command_list[1] == 'hostip':
            to_return = f'print("Taken Variable Name: {command_list[1]}'
        elif command_list[0] == 'i' or command_list[0] == 'int' or command_list[0]== 'intiger':
            to_return = f"{command_list[1]} = int({' '.join(command_list[3:])})"
        elif command_list[0] == 's' or command_list[0] == 'str' or command_list[0] == 'string':
            to_return = f"{command_list[1]} = '{' '.join(command_list[3:])}'"
        else:
            to_return = 'print("Variable Type not Specified.")'
    elif main == 'IF':
        if not command_list[-1] == 'THEN':
            to_return = "print(\'ERROR: \\'THEN\\' expected\')"
        else:
            condition = command_list[1:-1]
            if len(condition) != 3 or not (condition[1] in ['<', '<=', '==', '>=', '>']):
                to_return = "print(\'ERROR: If then condition syntax must be: \\'IF <var> </<=/==/>=/> <var> " \
                            "THEN\\'\')"
            else:
                to_return = "if " + ' '.join(condition) + ':'
    elif main == 'WHILE':
        if not command_list[-1] == 'DO':
            to_return = "print(\'ERROR: \\'DO\\' expected\')"
        else:
            condition = command_list[1:-1]
            if len(condition) != 3 or not (condition[1] in ['<', '<=', '==', '>=', '>']):
                to_return = "print(\'ERROR: While do condition syntax must be: \\'WHILE <var> </<=/==/>=/> <var> " \
                            "DO\\'\')"
            else:
                to_return = "while " + ' '.join(condition) + ':'
    elif main == 'DEFFUNC':
        if len(command_list) != 2:
            to_return = f'print("ERROR: Expected 1 argument but {len(command_list)-1} passed.")'
        else:
            to_return = f'def {command_list[1]}(funcargs=None):'
            funcs.append(command_list[1])
    elif main == 'FOR':
        if len(command_list) == 4 and command_list[2] == 'IN':
            to_return = f'for {command_list[1]} in {command_list[3]}:'
    elif main == 'FOREVER':
        to_return = "while True:"
    elif main == 'ELSE':
        to_return = 'else:'
    elif main == 'exit':
        if len(command_list) == 2:
            to_return = f'sys.exit({command_list[1]})'
        elif len(command_list) == 1:
            to_return = f'sys.exit()'
        else:
            to_return = 'print("ERROR: Syntax of exit command: exit <exitcode (optional, default 0)>")'
    elif main == 'pass':
        if len(command_list) == 1:
            to_return = f'pass'
        else:
            to_return = f'print("ERROR: Expected 0 arguments but {len(command_list)-1} passed.'
    elif main == 'runcmd':
        to_return = f'os.system(f"{" ".join(command_list[1:])}")'
    elif main == 'pause':
        if len(command_list) != 2:
            to_return = f'print("ERROR: 1 Argument expected but {len(command_list)} passed.")'
        else:
            to_return = f'time.sleep({command_list[1]})'
    elif main == 'gui':
        if 'libguimod' in imported:
            if len(command_list) < 2:
                to_return = 'print("ERROR: Expected 1 or more arguments but 0 passed.")'
            subcommand = command_list[1]
            if subcommand == 'setup':
                if len(command_list) == 2:
                    to_return = 'root = tk.Tk(className="nonamegui")\nroot.title("nonamegui")'
                else:
                    to_return = f'root = tk.Tk(className="{" ".join(command_list[2:])}")\nroot.title("{" ".join(command_list[2:])}")'
            elif subcommand == 'run':
                if not len(command_list) > 2:
                    to_return = 'root.mainloop()'
                else:
                    to_return = f'print("ERROR: Expected 1 argument but {len(command_list)-2} passed.")'
            elif subcommand == 'createbutton':
                cmdarg = command_list[2]
                textarg = ' '.join(command_list[3:])
                if not cmdarg == 'nocmd':
                    to_return = f'button{str(buttoncount)} = tk.Button(root, text=f"{textarg}", command={cmdarg})\nbutton{str(buttoncount)}.pack()'
                else:
                    to_return = f'button{str(buttoncount)} = tk.Button(root, text=f"{textarg}")\nbutton{str(buttoncount)}.pack()'
                buttoncount += 1
            elif subcommand == 'createlabel':
                    textarg = ' '.join(command_list[2:])
                    to_return = f'label{str(labelcount)} = tk.Label(root, text=f"{textarg}")\nlabel{str(labelcount)}.pack()'
            else:
                to_return = "print('Subcommand Not Found.')"
        else:
            to_return = 'print("Command not found: gui")'
    elif main == 'filerw':
        if 'libfilemod' in imported:
            if len(command_list) < 2:
                to_return = 'print("ERROR: Expected 1 or more arguments but 0 passed.")'
            subcommand = command_list[1]
            if subcommand == 'read':
                if len(command_list) == 4:
                    to_return = f'for i in range(0, len(open("{command_list[2]}", "r").readlines())):\n\tlocals()["{command_list[3]}"+str(i+1)]=open("{command_list[2]}", "r").readlines()[i].strip("\\n")'
                else:
                    to_return = f'print("ERROR: Expected 1 argument but {len(command_list)-2} passed.")'
            elif subcommand == 'write':
                if len(command_list) >= 4:
                    to_return = f'open("{command_list[2]}", "w").write(f"{" ".join(command_list[3:])}")'
                elif len(command_list) == 3:
                    to_return = f'open("{command_list[2]}", "w").close()'
                else:
                    to_return = f'print("ERROR: Expected 1 argument but {len(command_list)-2} passed.")'
            elif subcommand == 'append':
                if len(command_list) >= 4:
                    to_return = f'if not open("{command_list[2]}", "r").readlines() or open("{command_list[2]}", "r").readlines()[-1].endswith("\\n"):\n\topen("{command_list[2]}", "a").write(f"{" ".join(command_list[3:])}")\nelse:\n\topen("{command_list[2]}", "a").write(f"\\n{" ".join(command_list[3:])}")'
                else:
                    to_return = f'print("ERROR: Expected 2 arguments but {len(command_list)-2} passed.")'
            elif subcommand == 'delete':
                if len(command_list) == 3:
                    to_return = f'os.remove(f"{command_list[2]}")'
            else:
                to_return = "print('Subcommand Not Found.')"
        else:
            to_return = 'print("Command not found: filerw")'
    else:
        if main in funcs:
            to_return = f'{main}()'
        else:
            to_return = f'print("Command Not Found: {main}")'
    for i in range(indent):
        to_return = '\t' + to_return
        to_return.replace('\n', '\n\t')
    return to_return

if len(args)==0:
    print('Required Argument: <filename>')
    print('Use -h, -H, or --help for help. ')
    sys.exit(1)
elif len(args)==1:
    if args[0]=='-h' or args[0]=='-H' or args[0]=='--help':
        help()
    else:
        compile()
else:
    print(f"ERROR: 1 Argument expected but {len(args)} passed.")
    sys.exit(1)
