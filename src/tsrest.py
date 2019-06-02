"""
tsrest restores Tableau Backup into the Server. 
It looks into the Backup directory from the configuration
and restores the backup into the tableau server
"""

__author__      = "Shankar Narayanan SGS"
__copyright__   = "Copyright , Shankar Narayanan SGS"
__website__		= "www.shankarnarayanan.com"

import configparser
import time
import sys
import logging
import os
from fnmatch import fnmatch
import easygui
from configop import *

configloc = "config.ini"
logfile = "log.txt"

bfilespath=[]

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, filename = logfile,level=logging.DEBUG)


#reading backup folder
def readbackup (bpath):

	try:
		global bfilespath
		pattern = '.tsbak'

		for root, dirs, files in os.walk(bpath):
			for file in files:
				if file.endswith(pattern):
					bfilespath.append(os.path.join(root, file))

	except:
		logging.exception('Error in reading backup files')

	return;

# tableau restore
def tabrest (restfile,resconfig):

	try:
		os.chdir(binpath)
		os.system('tabadmin stop')
		if resconfig==1:
			os.system('tabadmin restore --no-config '+restfile)
		elif resconfig==0:
			os.system('tabadmin restore '+restfile)
		os.system('tabadmin start')

	except:
		logging.exception('Error in restoring backup '+restfile)

	return;

def showgui ():
	msg ="Select a Backup to Restore \n Backup Path will have Year\Month\Day and filename will have time HH-MM-SS"
	title = "tsrest - Tableau Restore Utility"
	choice = easygui.choicebox(msg, title, bfilespath)
	confirmmsg ="Do you want to restore with config \n"+choice
	confirmchoices = ["Yes","No","Cancel"]
	reply = easygui.buttonbox(confirmmsg, title, choices=confirmchoices, default_choice='Yes')
	if reply=='Yes':
		logging.info('Tableau Restored with config started for backup '+choice)
		tabrest(choice,1)
		logging.info('Tableau Restored completed')
	elif reply=='No':
		logging.info('Tableau Restored started for backup '+choice)
		tabrest(choice,0)
		logging.info('Tableau Restored completed')
	elif reply=='Cancel':
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
		logging.info('tsrest exit')

	return 0;

if __name__ == "__main__":
    sys.exit(main())