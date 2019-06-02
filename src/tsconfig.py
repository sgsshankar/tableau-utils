"""
tsconfig provides list of tableau configuration
and ability to set the config.
"""

__author__      = "Shankar Narayanan SGS"
__copyright__   = "Copyright , Shankar Narayanan SGS"
__website__		= "www.shankarnarayanan.com"

import configparser
from datetime import datetime
import time
import sys
import logging
import os
import shutil
import easygui
import yaml
from configop import *

configloc = "config.ini"
logfile = "log.txt"

fmname = datetime.now().strftime("%H-%M-%S")
cyear = datetime.now().strftime("%Y")
cmonth = datetime.now().strftime("%m")
cdate = datetime.now().strftime("%d")

#backup files name
cbname=None

docs = None
text = []
cchoice = []

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, filename = logfile,level=logging.DEBUG)


def setbackup (dpath):

	global backuppath
	#organize in year/month/date

	#root folder
	if not os.path.exists(dpath):
		os.makedirs(dpath)
		os.chdir(dpath)
	else:
		os.chdir(dpath)
	#year
	if not os.path.exists(cyear):
		os.makedirs(cyear)
		os.chdir(cyear)
	else:
		os.chdir(cyear)
	#month
	if not os.path.exists(cmonth):
		os.makedirs(cmonth)
		os.chdir(cmonth)
	else:
		os.chdir(cmonth)
	#date
	if not os.path.exists(cdate):
		os.makedirs(cdate)
		os.chdir(cdate)
	else:
		os.chdir(cdate)
		
	backuppath=os.getcwd()

	global cbname
	cbname='config-'+fmname+'.yml'

	return;

def getconfig ():

	try:
		os.chdir(binpath)
		os.system('tabadmin configure -o "configbackup.yml"')
		os.rename('configbackup.yml',cbname)
		shutil.move(cbname,backuppath)
		logging.info(cbname+' backup to '+backuppath)
		os.chdir(backuppath)
		stream = open(cbname, 'r')
		global docs
		docs = yaml.load_all(stream)
		logging.info('configuration read from Tableau')

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

def commitconfig ():

	try:
		os.chdir(binpath)
		os.system('tabadmin config')
		os.system('tabadmin start')

	except:
		logging.exception('Error in applying configuration and starting server')

	return;

def stopserver ():

	try:
		os.chdir(binpath)
		os.system('tabadmin stop')

	except:
		logging.exception('Error in stopping server')

	return;

def showgui ():

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
			stopserver()
			for s in choice.splitlines():
				cchoice = s.split(':')
				setconfig(cchoice[0],cchoice[1])
			commitconfig()
		elif reply=='No':
				showgui()
		return;

def main():

	try:
		cjson=readConfig(configloc);
		global binpath,backuppath
		binpath = cjson['binpath']
		backuppath = cjson['backuppath']
		setbackup(backuppath)
		getconfig()
		showgui()

	except:
		logging.exception("Error in tsconfig")

	return 0;

if __name__ == "__main__":
    sys.exit(main())


