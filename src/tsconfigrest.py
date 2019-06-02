"""
tsconfigrest restores tableau configuration backup
that was backed up by the tsback utility
"""

__author__      = "Shankar Narayanan SGS"
__copyright__   = "Copyright , Shankar Narayanan SGS"
__website__		= "www.shankarnarayanan.com"

import configparser
import time
import sys
import logging
import os
import shutil
import os
from fnmatch import fnmatch
import easygui
import yaml
from configop import *

configloc = "config.ini"
logfile = "log.txt"

bfilespath=[]

docs = None
text = []
cchoice = []

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, filename = logfile,level=logging.DEBUG)

#reading backup folder
def readbackup (bpath):

	try:
		global bfilespath
		pattern = '.yml'

		for root, dirs, files in os.walk(bpath):
			for file in files:
				if file.endswith(pattern):
					bfilespath.append(os.path.join(root, file))

	except:
		logging.exception('Error in reading backup files')

	return;

def getconfig (cbname):

	try:
		stream = open(cbname, 'r')
		global docs
		docs = yaml.load_all(stream)
		logging.info('configuration read from Backup file'+cbname)

	except:
		logging.exception('Error in reading tableau configuration')

	return;

def setconfig (key,value):

	try:
		os.chdir(binpath)
		os.system('tabadmin set '+key+' '+value)
		logging.info(value+' has been set to '+key)

	except:
		logging.exception('Error in setting '+value+' to '+key)

	return;

def showgui ():
	msg ="Select a Configuration Backup to Restore \n Backup Path will have Year\Month\Day and filename will have time HH-MM-SS"
	title = "tsconfigrest - Tableau Configuration Restore Utility"
	choice = easygui.choicebox(msg, title, bfilespath)
	confirmmsg ="Do you want to restore this configuration \n"+choice
	confirmchoices = ["Yes","No"]
	reply = easygui.buttonbox(confirmmsg, title, choices=confirmchoices, default_choice='No')
	if reply=='Yes':
		logging.info('Tableau config Restored started for backup '+choice)
		getconfig(choice)
		for doc in docs:
			for k,v in doc.items():
				s = str(k)+":"+str(v)
				text.append(str(s))
				text.append("\n")
		msg ="Edit the parameter/Remove them and click on Ok to apply them to the tableau server \n It will take long time to set all the values if list is big"
		title = "tsconfig - Tableau Configuration Utility"
		choice = easygui.codebox(msg, title, text)
		confirmmsg ="Do you want to apply these configs \n"
		confirmchoices = ["Yes","No"]
		reply = easygui.buttonbox(confirmmsg, title, choices=confirmchoices, default_choice='No')
		if reply=='Yes':
			for s in choice.splitlines():
				cchoice = s.split(':')
				setconfig(cchoice[0],cchoice[1])
		elif reply=='No':
				showgui()
		return;
		logging.info('Tableau configuration Restored completed')
	elif reply=='No':
		showgui()

	return;

def main():

	try:
		cjson=readConfig(configloc);
		global binpath,backuppath
		binpath = cjson['binpath']
		backuppath = cjson['backuppath']
		readbackup(backuppath)
		showgui()

	except:
		logging.info('tsconfigrest exit')

	return 0;

if __name__ == "__main__":
    sys.exit(main())