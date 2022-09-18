# C+ Tutorial

**Note: C+ uses spaces instead of tabs to make the language as simple as possible**

---

## Table of Contents
- [Syntax](#syntax)
  * [Syntax Overview](#syntax-overview)
  * [Commands Built-In](#commands-built-in)
- [Variables](#variables)
  * [Creating a variable](#creating-a-variable)
  * [Calling a variable](#calling-a-variable)
- [Modifications](#modifications)
  * [libguimod](#libguimod)
- [Conditions and Loops](#conditions-and-loops)
  * [If Else Syntax](#if-else-syntax)
  * [For Loop Syntax](#for-loop-syntax)
  * [Forever Loop Syntax](#forever-loop-syntax)
  * [While Loop Syntax](#while-loop-syntax)
- [Functions](#functions)
  * [Creating a function](#creating-a-function)
  * [Calling a function](#calling-a-function)
- [Examples](#examples)
  * [Hello World](#hello-world)
  * [Get User's Name and Age and then Display Information](#get-user-s-name-and-age-and-then-display-information)
  * [Example GUI](#example-gui)

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

### Commands Built-In
`putln` - Displays Text to Terminal Window.  Similar to Python `print()` command or bash `echo` command.

`getinput` - Asks user for input and stores input to `inputresult` variable. Similar to Python `input()` command.

`exit` - Exits the program, arg1 will be return code. Similar to Python `sys.exit()` command or bash `exit` command.

`pause` - Pauses to program, arg1 will be pause time (seconds). Similar to Python `time.sleep()` command or bash `sleep` command.

`runcmd` - Runs a system command. Similar to Python `os.system()` command.

---

## Variables
### Creating a variable
```
Types:
- string (s, str, or string can be used to declare a string)
- intiger (i, int, or intiger can be used to declare an intiger)
```
Syntax for creating a variable:
```
type varname = varvalue
```

### Built in Variables
- arg1 - arg9 - Arguments passed to the program.

### Calling a variable
To call a varible, use `{varname}`, for example:
```
str name = James
putln Hello, {name}, have a nice day!
```
then the output will be:
```
Hello, James, have a nice day!
```

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
This is used when, for example, you want to do something how many times according to the number of items in a list, then you can use this syntax:
```
FOR letter IN string
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
Functions are an essencial part of programming, it is a group of reuseable commands that can be called using only one command.

### Creating a function
To Create a Function, use the `DEFFUNC` Keyword like so.
```
DEFFUNC function_name
 Do Things...
```

### Calling a function
To call a function, just put the function name on a line like so.
```
function_name
```

---

## Examples
### Hello World

```
putln Hello World!
```
### Get User's Name and Age and then Display Information
```
getinput Please Enter your Name:
s name = inputresult
getinput Please Enter your Age:
s age = inputresult
putln Hello {name}, you are {age}.
```

### Example GUI
```
#addmod libguimod
DEFFUNC examplefunc
 putln Hello World
gui setup examplegui
gui createlabel Click the Button Below to Display Hello World in Terminal
gui createbutton examplefunc Click Here for Hello World in Terminal
gui createbutton nocmd Click Here for Absolutely Nothing (also a feature of C+)
gui run
```

---
<br>
<div style="text-align: center;"><small>Copyright (c) 2022 Jiusoft</small></div>