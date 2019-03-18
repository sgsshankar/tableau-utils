### Development Setup ###

* Install python 3.4.3 from https://www.python.org/downloads/

* Install pywin32 32 bit Build 218 [pywin32-218.win32-py3.4.exe] (http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/))

* Restart the system and execute the following command as Administrator(root) 

* `python scripts\pywin32_postinstall.py -install`

* Install pyinstaller using the following command

* `pip install pyinstaller`

* Install py2exe using the following command

* `pip install py2exe`

* Run build.bat to build the program into executable file

### Dependencies ###

* `pip install -r requirements.txt`

### Packing and Dist ###

* Download Innosetup Quick start package from http://www.jrsoftware.org/isdl.php
* Run pack.bat to pack it into EXE