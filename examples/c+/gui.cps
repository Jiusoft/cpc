#addmod libguimod
BEGIN examplefunc
 putln Hello World
gui setup examplegui
gui createlabel Click the Button Below to Display Hello World in Terminal
gui createbutton examplefunc Click Here for Hello World in Terminal
gui createbutton nocmd Click Here for Absolutely Nothing (also a feature of C+)
gui run