#addmod libguimod
DEFFUNC helloworld
 putln Hello World!
gui setup testgui
gui createlabel Some random text
gui createtab First Tab
gui createtab Second Tab
gui tab1 createlabel Text for Tab 1
gui tab2 createbutton helloworld Button for Tab 2
gui createtab Third Tab
gui tab3 createinput
DEFFUNC submit
 gui input1 gettext variable
 putln {variable}
 gui input1 cleartext
gui tab3 createbutton submit Display Text in Terminal
gui run