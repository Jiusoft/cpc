# C+ Tutorial

**Note: C+ uses spaces instead of tabs to make the language as simple as possible**

---

## Table of Contents

- [Syntax](#syntax)
  - [Syntax Overview](#syntax-overview)
  - [putln](#putln)
  - [getinput](#getinput)
  - [exit](#exit)
  - [pause](#pause)
  - [runcmd](#runcmd)
- [Variables](#variables)
  - [set](#set)
  - [unset](#unset)
  - [Using Variables](#using-variables)
- [Comments](#comments)
- [Modifications](#modifications)
  - [libguimod](#libguimod)
  - [libfilemod](#libfilemod)
- [Conditions and Loops](#conditions-and-loops)
  - [If Else Syntax](#if-else-syntax)
  - [For Loop Syntax](#for-loop-syntax)
  - [Forever Loop Syntax](#forever-loop-syntax)
  - [While Loop Syntax](#while-loop-syntax)
- [Functions](#functions)
  - [Creating a function](#creating-a-function)
  - [Calling a function](#calling-a-function)
- [Examples](#examples)

---

## Syntax

### Syntax Overview

C+ vs Python vs Bash
C+:

```
command subcommand(optional) argument1 argument2 argument3...
```

Python

```
function(argument1 argument2 argument3...)
```

Bash

```
command argument1 argument2 argument3...
```

### putln

Displays Text to Terminal Window. Similar to Python `print()` command or bash `echo` command.

Syntax:

```
putln <text to display>
```

### getinput

Asks user for input and stores input to user defined variable. Similar to Python `input()` command.

Syntax:

```
getinput <variable> <prompt>
```

### exit

Exits the program, arg1 will be return code. Similar to Python `sys.exit()` command or bash `exit` command.

Syntax:

```
exit <returncode (optional)>
```

### pause

Pauses to program, arg1 will be pause time (seconds). Similar to Python `time.sleep()` command or bash `sleep` command.

Syntax:

```
pause <seconds>
```

### runcmd

Runs a system command. Similar to Python `os.system()` command.

Syntax:

```
runcmd <command>
```

---

## Variables

### set

Sets a variable. Similar to Python `varname = varvalue` or bash `varname=varvalue`.

Syntax:

```
set <attributes> <variable name (cannot contain spaces)> <variable value>
```

Attributes are:

- i: intiger, local
- s: string, local
- ig/gi: intiger, global
- sg/gs: string, global

Taken Variable Names:

- arg1 - arg9 - Arguments passed to the program.
- hostname - For Checking Host Name.
- hostip - For Checking Host IP Address.
- exedir - For Directory the executable is in.
- exeloc - For the location of the executable on the system.
- operatingsystem - For your operating system.

### unset

Unsets a variable. Similar to Python `del` command.

Syntax:

```
unset <variable name>
```

### Using Variables

To use a variable, do `{variablename}`.

Examples:

```
putln Hello, {name}, you are handsome.
```

---

## Comments

Only Single Line Comments are supported for now, and to start it, use `//`. Everything after `//` will be considered a comment and will not be read by the compiler. For a full line comment, start the line with `//`

---

## Modifications

### libguimod

libguimod is a modification that allows you to build gui applications.

**Commands provided by `libguimod`:**

`gui setup` - Sets up a GUI Main Window, arg1 will be application name.

`gui createlabel` - Creates a label (Text) inside main window.

`gui createbutton` - Creates a button inside main window. Uses arg1 as command (nocmd for no command), uses arg2 to end for button text.

`gui run` - Runs the GUI.

### libfilemod

libfilemod is a modification that allows you manipulate files.

**Commands provided by `libfilemod`:**

`filerw read` - Reads a file, arg1 as filename and arg2 as the variable to save to. eg. `filerw read newfile var`, then var1 will be first line, var2 will be second line, etc.

`filerw write` - Writes to a file, arg1 as filename and arg2 as the text to write. If arg2 doesn't exist, it creates a blank file if the file doesn't exist.

`filerw append` - Appends to a file, arg1 as filename and arg2 as the text to append.

`filerw delete` - Deletes a file, arg1 as the filename to delete.

---

## Conditions and Loops

C+ Features If, For, Forever, and While Loops.

### If Else Syntax

This is used when you want to do something if a condition is true (for example, a variable is smaller or equal to 5).

```
IF condition THEN
 Do Something
ELSE
 IF condition THEN
  Do Something (This part will be the same as else if)
 ELSE
  Do Something (The actual else)
```

### For Loop Syntax

This is used when, for example, you want to do something how many times according to the number of letters in a string, then you can use this syntax:

```
FOR variable IN string DO
 Do Something
```

### Forever Loop Syntax

This is used when you want to do something forever until program is terminated.

```
FOREVER
 Do Something
```

### While Loop Syntax

This is used if you want to do something repetitively until a condition becomes false.

```
WHILE condition
 Do Something
```

---

## Functions

Functions are an essensial part of programming, it is a group of reuseable commands that can be called using only one command.

### Creating a function

To Create a Function, use the `DEFFUNC` Keyword like so.

```
DEFFUNC function_name
 Do Things...
```

Use fnarg{argumentnumber} for function argument access.

### Calling a function

To call a function, just put the function name on a line like so.

```
function_name arg1 arg2 arg3 ...
```

---

<div align="center">Copyright (c) 2022 Jiusoft</div>
