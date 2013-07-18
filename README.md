#Changelog v0.0_10
##"Now with more sprites!"
##17 July 2013

### Weapons System
Weapons now have attack and defense values as stored in an xml document. The sword is 4,0, TestDot is 10,5, and TestDot2 is 1,20. Though those values currently mean absolutely nothing.
It now doesn't reset when you select something...that was fixed somehow...

### Sprite.py
There is a new class, Sprite.Enemy. It's extremely similar to Sprite.Sprite (copy paste similar) with the exception that this class cannot teleport. More differences will come as the whole fighting aspect of the game gets more fleshed out.

### Enemies
In the spirit of using things I write, there is hardcoded into the game.py script an enemy that just walks in a square endlessly, but it does collide with things so that's totally cool for now.

#Changelog v0.0_9.2 
##"Now with more efficiency!"
##12 July 2013

### Inventory System
The Inventory screens (so weapons and items) have been rewritten from the ground up in an effort to make the system more efficient. It no longer requires temporary files to be written and editted during the runtime (yikes! what was I thinking) which is always a plus. It's also shorter and easier to maintain
There are some aesthetic problems to fix but nothing major.

There are also now items to select from the inventory that give the character different items to hold.
See the Bug Fix section for more info
	
### Bug Fix
Bug number 3 as reported in v0.0_9.1 has been fixed (for the time being) so the folders should be a lot more pretty looking. Now there is a section for sprite sheets in spritedev to place animations of the character holding something
Item dev now contains the inventory tiles
A conf directory as created to hold map files, save files, and miscelaneous files needed to run. Modules still go in the root folder

#Changelog v0.0_9.1 
##"Now with more cross-compatibility!"
##7 July 2013

### File Paths
Changed it so all the paths are written with os.path.join instead of being hardcoded for my linux computer because I'm planning on making a .exe out of it and it won't run if the file paths aren't cross compatible
### Known Bugs to be fixed
[x] Selection from the inventory resets sprite location? (somehow fixed??)
[ ] Pressing left + right causes sprite not to move
[x] Clean up the main directory so put modules, maps, and config files into their own folders

#Changelog v0.0_9 
##"Now with more enter!"
##20 May 2013

### Text Display System
Still using the spacebar to actuate text examples. However it now switches panels based upon pressing the enter/return key.
	
### Inventory System
The weapons menu now allows you to actually select an item. Pressing enter over an item in there (any of them because I haven't coded it to differentiate between items) will cause the sprite on screen to hold onto a sword and walk with it.

#Changelog v0.0_8 
##"Now with more dialogue!"
#19 May 2013

### Inventory System
Pressing "w" no longer causes the program to crash but instead opens the weapons menu, you know, as it should. The weapons menu loads objects exactly the same as the inventory (I just copy and pasted the code so that should explain why)
	
### Text Display System
Pressing "Space" will (temporarily to show of the feature) bring up the text box and load text. There are three panels, each will display for about 2 seconds. The process receives a code and checks "Dialogue.config" for the related information (more documentation in Dialogue.config itself). This is used to read the appropriate text from "Dialogue.txt". Then a process handles newline characters if more than one line is requested. If more than 3 lines are requested, another process breaks it up into chunks of 3 lines, displays an arrow (unicode 25bc) and then displays each one in succession. Text can be added or removed from Dialogue.txt as long as the appropriate changes are made in Dialogue.config. that being said, I don't recommend changing Dialogue.txt by yourself, but who am I to judge. 
	
### Escape to Quit
While in inventory (and weapons), pressing inventory no longer quits to world (see XKCD 1172) but instead does as it's supposed to and exits the program as a whole.
	
### Dialogue.py
New module for dialogue related processes. Documentation will come eventually...

#Changelog v0.0_7 
##"Now with working inventory!"
##18 May 2013

### New Naming Convention
Versions will be named 0.0_# until more full-featured versions come out. v0.3* and v0.6* are retroactively named v0.0_3 and v0.0_6 respectively
	
### Inventory System
Pressing "e" opens inventory. pressing "q" closes inventory. The highlighted tile can be moved from tile to tile. The item "TestDot.png" is put in. You can add or remove them by going into "inventory.save" and adding or removing them. One item per row. Program fails if there is a newline character as the last line.
You can add your own item sprites: convention is 40px by 40px png image.
