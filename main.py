import os
import sys
import shutil
import platform

args = sys.argv[1:]
global funcs
funcs = []


def version():
    print('cpc 2.0.0')


def help():
    print('cpc version 2.0.0\nCopyright (c) 2022 Jiusoft\nUsage: cpc <filename (input)> <filename (optional, output)>\nArguments:\n\t-h, -H or --help: Display this help message\n\t-l, -L or --license: Display License Agreement\n\t-v, -V or --version: Display Version')


def license():
    print("""MIT License

Copyright (c) 2022 Jiusoft

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:from configparser import LegacyInterpolation

The above copyright notice and this permission notice shall be included in allfrom configparser import LegacyInterpolation
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""")


def compile(output=None):
    global origfilename
    skipappend = False
    origfilename = args[0].split('/')[-1]
    filename = args[0].split('/')[-1].split('.')[0]
    if os.path.isfile(args[0]):
        with open(filename + '.py', "a+") as f:
            f.write(
                'import socket, os, time, sys, platform\nhostname=socket.gethostname()\nhostip=socket.gethostbyname(hostname)\nglobal args\nargs=sys.argv[1:]\nif platform.system() == "Windows":\n\toperatingsystem = "windows"\nelif platform.system() == "Darwin":\n\toperatingsystem = "macos"\nelif platform.system() == "Linux":\n\toperatingsystem = "linux"\nelse:\n\toperatingsystem = "unknown"\nif len(args) > 9:\n\tprint("Application Crashed: Too much arguments to handle."); sys.exit(1)\nelse:\n\tfor n in range(len(args), 9):\n\t\targs.append("")\narg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9 = args\ndel args\nexeloc = os.path.abspath(sys.argv[0])\nexedir = os.path.dirname(exeloc)\ncwd = os.getcwd()\n')
        with open(args[0], "r") as f:
            for line in f.readlines():
                if line.startswith('//'):
                    skipappend = True
                else:
                    skipappend = False
                line = line.split('//')[0]
                toAppend = toPython(line) if not skipappend else ''
                with open(filename + '.py', "a") as nf:
                    nf.write(toAppend + '\n')
        if platform.system() == "Linux":
            os.system(f"python3 -m nuitka --quiet --remove-output {filename}.py 2> /dev/null")
        elif platform.system() == "Windows":
            os.system(f"python -m nuitka --quiet --remove-output {filename}.py 2> nul")
        if not output is None:
            if os.path.isdir(output):
                if platform.system() == "Linux":
                    shutil.move(filename + '.bin', f'{output}/{filename}')
                elif platform.system() == "Windows":
                    shutil.move(filename + '.exe', f'{output}/{filename}.exe')
            else:
                if platform.system() == "Linux":
                    shutil.move(filename + '.bin', output)
                elif platform.system() == "Windows":
                    shutil.move(filename + '.exe', output+'.exe')
        else:
            if platform.system() == "Linux":
                os.rename(filename + '.bin', filename)
        if platform.system() == "Windows":
            os.remove(filename + '.cmd')
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

def parseString(string):
    nums = min(string.count('{'), string.count('}'))
    for i in range(nums):
        illegal = False
        vstring = string[string.index('{')+1:string.index('}')]
        try:
            int(vstring[0])
            illegal = True
        except:
            pass
        for l in vstring:
            if not l.lower() in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_']:
                illegal = True
                break
        if illegal:
            string = string.replace('{', 'tmpillstartvar', 1).replace('}', 'tmpillendvar', 1)
        else:
            string = string.replace('{', 'tmpstartvar', 1).replace('}', 'tmpendvar', 1)
    string = string.replace('tmpstartvar', '{').replace('tmpendvar', '}')
    string = string.replace('tmpillstartvar', '{{').replace('tmpillendvar', '}}')
    return f'f"{string}"'

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
                global buttoncount, labelcount, tabcount, entrycount
                buttoncount = 0
                labelcount = 0
                tabcount = 0
                entrycount = 0
                imported.append('libguimod')
                to_return = 'import tkinter as tk\nfrom tkinter import ttk'
            elif command_list[1] == 'libfilemod' or code.split(' ')[1] == 'libfilemod\n':
                imported.append('libfilemod')
                to_return = ''
            else:
                return "print(\'ERROR: No such module!\')"
    elif main == 'putln':
        to_return = f'print({parseString(" ".join(command_list[1:]))})'
    elif main == 'getinput':
        spaces = 0
        while code.endswith(' ') or code.endswith(' \n'):
            if code.endswith(' '):
                spaces += 1
                code = code[:-1]
            elif code.endswith(' \n'):
                spaces += 1
                code = code[:-2]
        to_return = f'{command_list[1]} = input({parseString(" ".join(command_list[2:]))[:-1]}'
        for i in range(spaces):
            to_return += ' '
        to_return += '")'
    elif main == 'set':
        if command_list[1] == 'arg1' or command_list[1] == 'arg2' or command_list[1] == 'arg3' or command_list[1] == 'arg4' or command_list[1] == 'arg5' or command_list[1] == 'arg6' or command_list[1] == 'arg7' or command_list[1] == 'arg8' or command_list[1] == 'arg9' or command_list[1] == 'hostname' or command_list[1] == 'hostip' or command_list[1] == 'operatingsystem' or command_list[1] == 'exedir' or command_list[1] == 'exeloc' or command_list[1] == 'cwd':
            to_return = f'print("Taken Variable Name: {command_list[1]}'
        else:
            attrs = list(command_list[1])
            if len(attrs) > 2:
                to_return = 'print("Attributes could be: i (intiger), s (string), ig/gi (intiger and global), sg/gs (string and global)")'
            else:
                if 'i' in attrs:
                    if 'g' in attrs:
                        to_return = f"global {command_list[2]}; {command_list[2]} = int({parseString(' '.join(command_list[3:]))})"
                    else:
                        to_return = f"{command_list[2]} = int(f'{' '.join(command_list[3:])}')"
                elif 's' in attrs:
                    if 'g' in attrs:
                        to_return = f"global {command_list[2]}; {command_list[2]} = {parseString(' '.join(command_list[3:]))}"
                    else:
                        to_return = f"{command_list[2]} = f'{' '.join(command_list[3:])}'"
                else:
                    to_return = 'print("Variable Type not Specified.")'
    elif main == 'unset':
        if len(command_list) == 2:
            to_return = f'del {command_list[1]}'
        else:
            to_return = f'print("Expected 1 Argument but {len(command_list) - 1} found.")'
    elif main == 'IF':
        if not command_list[-1] == 'THEN':
            to_return = "print(\'ERROR: \\'THEN\\' expected\')"
        else:
            condition = command_list[1:-1]
            condition[0] = f'f\"{condition[0]}\"'
            condition[-1] = f'f\"{condition[-1]}\"'
            canint = 0
            try:
                condition[0] = int(condition[0])
                canint += 1
            except ValueError:
                pass
            try:
                condition[-1] = int(condition[-1])
                canint += 1
            except ValueError:
                pass
            if canint == 0:
                condtype = 's'
            elif canint == 1:
                condtype = 'error'
            elif canint == 2:
                condtype = 'i'
            if len(condition) == 3:
                if condtype == 'i' and condition[1] in ['<', '<=', '=', '>=', '>', '!=']:
                    to_return = "if " + \
                        ' '.join(
                            condition) + ':' if not condition[1] == '=' else "if " + condition[0] + " == " + condition[-1] + ":"
                elif condtype == 's' and condition[1] in ['=', '!=', 'is', 'isnot']:
                    if condition[1] == 'is':
                        if condition[-1] == 'f"empty"':
                            to_return = 'if ' + condition[0] + ' == "":'
                        elif condition[-1] == 'f"upper"':
                            to_return = 'if ' + condition[0] + '.isupper():'
                        elif condition[-1] == 'f"lower"':
                            to_return = 'if ' + condition[0] + '.islower():'
                        elif condition[-1] == 'f"title"':
                            to_return = 'if ' + condition[0] + '.istitle():'
                        else:
                            to_return = 'print("IF var is can only be empty, upper, lower, and title.")'
                    elif condition[1] == 'isnot':
                        if condition[-1] == 'f"empty"':
                            to_return = 'if ' + condition[0] + ' != "":'
                        elif condition[-1] == 'f"upper"':
                            to_return = 'if not ' + \
                                condition[0] + '.isupper():'
                        elif condition[-1] == 'f"lower"':
                            to_return = 'if not ' + \
                                condition[0] + '.islower():'
                        elif condition[-1] == 'f"title"':
                            to_return = 'if not ' + \
                                condition[0] + '.istitle():'
                        else:
                            to_return = 'print("IF var is can only be empty, upper, lower, and title.")'
                    else:
                        to_return = "if " + \
                            ' '.join(
                                condition) + ':' if not condition[1] == '=' else "if " + condition[0] + " == " + condition[-1] + ":"
                elif condtype == 'error':
                    to_return = 'print("Cannot compare int to string.")'
                else:
                    to_return = "print(\'ERROR: If then condition syntax must be: \\'IF <var> </<=/=/>=/>/!= <var> THEN\\' for intigers and \\'IF <var> =/!= <var> THEN for strings\\' an exception for strings is \\'IF <var> is <condition>\\'\')"
                    print(condition)
                    print(condtype)
                    print(condition[-1])
    elif main == 'WHILE':
        if not command_list[-1] == 'DO':
            to_return = "print(\'ERROR: \\'DO\\' expected\')"
        else:
            condition = command_list[1:-1]
            condition[0] = f'f\"{condition[0]}\"'
            condition[-1] = f'f\"{condition[-1]}\"'
            canint = 0
            try:
                condition[0] = int(condition[0])
                canint += 1
            except ValueError:
                pass
            try:
                condition[-1] = int(condition[-1])
                canint += 1
            except ValueError:
                pass
            if canint == 0:
                condtype = 's'
            elif canint == 1:
                condtype = 'error'
            elif canint == 2:
                condtype = 'i'
            if len(condition) == 3:
                if condtype == 'i' and condition[1] in ['<', '<=', '=', '>=', '>', '!=']:
                    to_return = "while " + \
                        ' '.join(
                            condition) + ':' if not condition[1] == '=' else "if " + condition[0] + " == " + condition[-1] + ":"
                elif condtype == 's' and condition[1] in ['=', '!=', 'is', 'isnot']:
                    if condition[1] == 'is':
                        if condition[-1] == 'f"empty"':
                            to_return = 'while ' + condition[0] + ' == "":'
                        elif condition[-1] == 'f"upper"':
                            to_return = 'while ' + condition[0] + '.isupper():'
                        elif condition[-1] == 'f"lower"':
                            to_return = 'while ' + condition[0] + '.islower():'
                        elif condition[-1] == 'f"title"':
                            to_return = 'while ' + condition[0] + '.istitle():'
                        else:
                            to_return = 'print("IF var is can only be empty, upper, lower, and title.")'
                    elif condition[1] == 'isnot':
                        if condition[-1] == 'f"empty"':
                            to_return = 'while ' + condition[0] + ' != "":'
                        elif condition[-1] == 'f"upper"':
                            to_return = 'while not ' + \
                                condition[0] + '.isupper():'
                        elif condition[-1] == 'f"lower"':
                            to_return = 'while not ' + \
                                condition[0] + '.islower():'
                        elif condition[-1] == 'f"title"':
                            to_return = 'while not ' + \
                                condition[0] + '.istitle():'
                        else:
                            to_return = 'print("IF var is can only be empty, upper, lower, and title.")'
                    else:
                        to_return = "while " + \
                            ' '.join(
                                condition) + ':' if not condition[1] == '=' else "if " + condition[0] + " == " + condition[-1] + ":"
                elif condtype == 'error':
                    to_return = 'print("Cannot compare int to string.")'
                else:
                    to_return = "print(\'ERROR: If then condition syntax must be: \\'IF <var> </<=/=/>=/>/!= <var> THEN\\' for intigers and \\'IF <var> =/!= <var> THEN for strings\\' an exception for strings is \\'IF <var> is <condition>\\'\')"
                    print(condition)
                    print(condtype)
                    print(condition[-1])
    elif main == 'DEFFUNC':
        if len(command_list) != 2:
            to_return = f'print("ERROR: Expected 1 argument but {len(command_list)-1} passed.")'
        else:
            to_return = f'def {command_list[1]}(fnargs=None):\n\tif not fnargs is None:\n\t\tfnargs = fnargs.split(' ')\n\t\tif len(fnargs) > 9:\n\t\t\tprint("Function Crashed: Too much arguments to handle."); sys.exit(1)\n\t\tfor n in range(len(fnargs), 9):\n\t\t\tfnargs.append("")\n\t\tfnarg1, fnarg2, fnarg3, fnarg4, fnarg5, fnarg6, fnarg7, fnarg8, fnarg9 = fnargs\n\tdel fnargs'
            funcs.append(command_list[1])
    elif main == 'FOR':
        if not command_list[-1] == 'DO':
            to_return = "print(\'ERROR: \\'DO\\' expected\')"
        else:
            if 'IN' == command_list[2]:
                command_list[3] = f'f"{command_list[3]}"'
                to_return = f'for {command_list[1]} in {command_list[3]}:'
            else:
                print(command_list[2])
                to_return = 'print("Expected IN but nowhere to be found.")'
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
                textarg = parseString(' '.join(command_list[3:]))
                if not cmdarg == 'nocmd':
                    to_return = f'button{buttoncount+1} = tk.Button(root, text={textarg}, command={cmdarg})\nbutton{buttoncount+1}.pack()'
                else:
                    to_return = f'button{buttoncount+1} = tk.Button(root, text={textarg})\nbutton{buttoncount+1}.pack()'
                buttoncount += 1
            elif subcommand == 'createlabel':
                textarg = parseString(' '.join(command_list[2:]))
                to_return = f'label{labelcount+1} = tk.Label(root, text={textarg})\nlabel{labelcount+1}.pack()'
            elif subcommand == 'createinput':
                if len(command_list) == 2:
                    to_return = f'entry{entrycount+1} = tk.Entry(root)\nentry{entrycount+1}.pack()'
                    entrycount += 1
                else:
                    to_return = f'Expected 0 arguments but {len(command_list)-2} found.'
            elif subcommand == 'createtab':
                if tabcount == 0:
                    to_return = f'tabs = ttk.Notebook(root)\ntab{tabcount+1} = ttk.Frame(tabs)\ntabs.add(tab{tabcount+1}, text = "{" ".join(command_list[2:])}")\ntabs.pack(expand = 1, fill ="both")'
                else:
                    to_return = f'tab{tabcount+1} = ttk.Frame(tabs)\ntabs.add(tab{tabcount+1}, text = "{" ".join(command_list[2:])}")\ntabs.pack(expand = 1, fill ="both")'
                tabcount+=1
            elif subcommand in ['tab'+str(item) for item in range(1, tabcount+1)]:
                subcommand = command_list[2]
                if len(command_list) < 3:
                    to_return = f'Expected 0 or more arguments but {len(command_list)-3} found.'
                elif subcommand == 'createbutton':
                    cmdarg = command_list[3]
                    textarg = parseString(' '.join(command_list[4:]))
                    if not cmdarg == 'nocmd':
                        to_return = f'button{buttoncount+1} = tk.Button({command_list[1]}, text={textarg}, command={cmdarg})\nbutton{buttoncount+1}.pack()'
                    else:
                        to_return = f'button{buttoncount+1} = tk.Button({command_list[1]}, text={textarg})\nbutton{buttoncount+1}.pack()'
                    buttoncount += 1
                elif subcommand == 'createlabel':
                    textarg = parseString(' '.join(command_list[3:]))
                    to_return = f'label{labelcount+1} = tk.Label({command_list[1]}, text={textarg})\nlabel{labelcount+1}.pack()'
                elif subcommand == 'createinput':
                    if len(command_list) == 3:
                        to_return = f'entry{entrycount+1} = tk.Entry({command_list[1]})\nentry{entrycount+1}.pack()'
                        entrycount += 1
                    else:
                        to_return = f'Expected 0 arguments but {len(command_list)-2} found.'
                else:
                    to_return = "print('Subcommand Not Found.')"
            elif subcommand in ['input'+str(item) for item in range(1, entrycount+1)]:
                subcommand = command_list[2]
                if len(command_list) < 3:
                    to_return = f'Expected 0 or more arguments but {len(command_list)-3} found.'
                elif subcommand == 'gettext':
                    if not len(command_list) == 4:
                        to_return = f'Expected 1 arguments but {len(command_list)-4} found.'
                    else:
                        to_return = f'{command_list[3]} = {command_list[1].replace("input", "entry")}.get()'
                elif subcommand == 'cleartext':
                    if not len(command_list) == 3:
                        to_return = f'Expected 1 arguments but {len(command_list)-3} found.'
                    else:
                        to_return = f'{command_list[1].replace("input", "entry")}.delete(0, tk.END)'
                else:
                    to_return = "print('Subcommand Not Found.')"
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
                    to_return = f'open("{command_list[2]}", "w").write({parseString(" ".join(command_list[3:]))})'
                elif len(command_list) == 3:
                    to_return = f'open("{command_list[2]}", "w").close()'
                else:
                    to_return = f'print("ERROR: Expected 1 argument but {len(command_list)-2} passed.")'
            elif subcommand == 'append':
                if len(command_list) >= 4:
                    to_return = f'if not open("{command_list[2]}", "r").readlines() or open("{command_list[2]}", "r").readlines()[-1].endswith("\\n"):\n\topen("{command_list[2]}", "a").write({parseString(" ".join(command_list[3:]))})\nelse:\n\topen("{command_list[2]}", "a").write(f"\\n{" ".join(command_list[3:])}")'
                else:
                    to_return = f'print("ERROR: Expected 2 arguments but {len(command_list)-2} passed.")'
            elif subcommand == 'delete':
                if len(command_list) == 3:
                    to_return = f'os.remove({parseString(" ".join(command_list[1:]))})'
            else:
                to_return = "print('Subcommand Not Found.')"
        else:
            to_return = 'print("Command not found: filerw")'
    else:
        if main in funcs:
            to_return = f'{main}(fnargs={parseString(" ".join(command_list[1:]))})'
        else:
            to_return = f'print("Command Not Found: {main}")'
    for i in range(indent):
        to_return = '\t' + to_return
        to_return.replace('\n', '\n\t')
    return to_return


if len(args) == 0:
    print('Required Argument: <filename>')
    print('Use -h, -H, or --help for help. ')
    print('Use -l, -L, or --license for license agreement. ')
    sys.exit(1)
elif len(args) == 1:
    if args[0] == '-h' or args[0] == '-H' or args[0] == '--help':
        help()
    elif args[0] == '-l' or args[0] == '-L' or args[0] == '--license':
        license()
    elif args[0] == '-v' or args[0] == '-V' or args[0] == '--version':
        version()
    else:
        compile()
elif len(args) == 2:
    if args[0] == '-h' or args[0] == '-H' or args[0] == '--help':
        help()
    elif args[0] == '-l' or args[0] == '-L' or args[0] == '--license':
        license()
    elif args[0] == '-v' or args[0] == '-V' or args[0] == '--version':
        version()
    else:
        compile(output=args[1])
else:
    print(f"ERROR: 1 or 2 Arguments expected but {len(args)} passed.")
    sys.exit(1)
