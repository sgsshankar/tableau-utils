"""
tsback provides backup of data, logs and configurations 
to specified location and also to cloud services like AWS.
It also does housekeeping stuffs such as cleanup, restart and warmup
along with archival and deletion of backups
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
import tinys3
import boto.glacier.layer2
from configop import *

configloc = "config.ini"
logfile = "log.txt"
fmname = datetime.now().strftime("%H-%M-%S")
cyear = datetime.now().strftime("%Y")
cmonth = datetime.now().strftime("%m")
cdate = datetime.now().strftime("%d")
cjson = {}
apath = []
alterpath = []

#backup files name
lbname=None
dbname=None


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

	global lbname,dbname
	lbname='logs-'+fmname+'.zip'
	dbname=backupname+'-'+fmname+'.tsbak'

	return;

def setalternatebackup (dpath):

	global alterpath
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
		
	alterpath.append(os.getcwd())

	global lbname,dbname
	lbname='logs-'+fmname+'.zip'
	dbname=backupname+'-'+fmname+'.tsbak'

	return;

def lbackup ():

	try:
		os.chdir(binpath)
		os.system('tabadmin ziplogs -l -n -f')
		os.rename('logs.zip',lbname)
		if alternateenable==1:
			for path in alterpath:
				shutil.copy(lbname,path)
				logging.info(lbname+' backup to '+path)
		shutil.move(lbname,backuppath)
		logging.info(lbname+' backup to '+backuppath)
		
		logging.info('Logbackup completed')
	
	except:
		logging.exception('Error in log backup')

	return;

def dbackup ():

	try:		
		os.chdir(binpath)
		os.system('tabadmin backup '+backupname+' -d')
		listoffiles = os.listdir(os.curdir)
		for filename in listoffiles:
			if filename.endswith('.tsbak'):
				os.rename(filename,dbname)
				if alternateenable==1:
					for path in alterpath:
						shutil.copy(dbname,path)
						logging.info(dbname+' backup to '+path)
				shutil.move(dbname,backuppath)
				logging.info(dbname+' backup to '+backuppath)

		logging.info('DataBackup Completed')

	except:
		logging.exception('Error in data backup')

	return;

def cbackup ():

	try:
		cbname = backupname+'-'+fmname+'.yml'
		os.chdir(binpath)
		os.system('tabadmin configure -o "configbackup.yml"')
		os.rename('configbackup.yml',cbname)
		if alternateenable==1:
			for path in alterpath:
				shutil.copy(cbname,path)
				logging.info(cbname+' backup to '+path)
		shutil.move(cbname,backuppath)
		logging.info(cbname+' backup to '+backuppath)

		logging.info('Config backup Completed')

	except:
		logging.exception('Error in config backup')


	return;

def tabclean ():

	try:
		os.chdir(binpath)
		os.system('tabadmin cleanup')
		logging.info('Tableau cleanup completed')

	except:
		logging.exception('Error in tableau cleanup')

	return;

def tabrestart ():

	try:
		os.chdir(binpath)
		os.system('tabadmin cleanup --restart')
		logging.info('Tableau Restart Completed')

	except:
		logging.exception('Error in tableau restart')

	return;

def bretention (days,fend,bpath):

	try:
		deltime=time.time()-days*86400
		count=0

		os.chdir(bpath)
		listoffiles = os.listdir(os.curdir)
		for filename in listoffiles:
			if filename.endswith(fend):
				if os.stat(filename).st_mtime<deltime:
					os.remove(filename)
					count+=1

		logging.info(str(count)+' files removed')
		logging.info('Backup retention completed')

	except:
		logging.exception('Error in deleting old backup files')

	return;

def s3upload():

	try:
		os.chdir(backuppath)
		conn = tinys3.Connection(s3accesskey,s3secretkey)
		if (os.path.isfile(lbname)):
			lf = open(lbname,'rb')
			conn.upload(lbname,lf,bucket=s3bucket)
			lf.close()
			logging.info(lbname+' uploaded to S3')
		else:
			logging.info(lbname + ' not found')

		if (os.path.isfile(dbname)):
			df = open(dbname,'rb')
			conn.upload(dbname,df,bucket=s3bucket)
			df.close()
			logging.info(dbname+ ' uploaded to S3')
		else:
			logging.info(dbname + ' not found')

		if (os.path.isfile(cbname)):
			cf = open(cbname,'rb')
			conn.upload(cbname,cf,bucket=s3bucket)
			cf.close()
			logging.info(cbname+ ' uploaded to S3')
		else:
			logging.info(cbname + ' not found')

	except:
		logging.exception('Error uploading to S3')

	return;

def glacierupload():

	try:
		os.chdir(backuppath)
		glacier_layer2 = boto.glacier.layer2.Layer2(aws_access_key_id=glacieraccesskey, aws_secret_access_key=glaciersecretkey, region_name=glacierregion, suppress_consec_slashes=True)
		v = glacier_layer2.get_vault(glaciervault)
		if (os.path.isfile(lbname)):
			lb_id = v.upload_archive(lbname)
			logging.info(lbname+ ' uploaded to Amazon Glacier with archive id '+lb_id)
		else:
			logging.info(lbname + ' not found')

		if (os.path.isfile(dbname)):
			db_id = v.upload_archive(dbname)
			logging.info(dbname+ ' uploaded to Amazon Glacier with archive id '+db_id)
		else:
			logging.info(dbname + ' not found')

		if (os.path.isfile(cbname)):
			cb_id = v.upload_archive(cbname)
			logging.info(cbname+ ' uploaded to Amazon Glacier with archive id '+cb_id)
		else:
			logging.info(cbname + ' not found')

	except:
		logging.exception('Error uploading to Amazon Glacier')

	return;

def tabwarm():

	try:
		os.chdir(binpath)
		os.system('tabadmin warmup')
		logging.info('Tableau Warmup Completed')
	except:
		logging.exception('Error in tableau warmup')

	return;

def main():
	logging.info("Backup process started")
	cjson=readConfig(configloc);
	global binpath,backupname,logbackup,databackup,backuppath,backupretention,logdays,datadays,cleanup,restart,s3enable,s3accesskey,s3secretkey,s3bucket,warmup,configbackup,alternateenable,alternatepath,glacierenable,glaciersecretkey,glacieraccesskey,glacierregion,glaciervault
	binpath = cjson['binpath']
	backupname = cjson['backupname']
	logbackup = cjson['logbackup']
	databackup = cjson['databackup']
	backuppath = cjson['backuppath']
	backupretention = cjson['backupretention']
	logdays = cjson['logdays']
	datadays = cjson['datadays']
	cleanup = cjson['cleanup']
	restart = cjson['restart']
	s3enable = cjson['s3enable']
	s3accesskey = cjson['s3accesskey']
	s3secretkey = cjson['s3secretkey']
	s3bucket = cjson['s3bucket']
	warmup = cjson['warmup']
	configbackup = cjson['configbackup']
	alternateenable = cjson['alternateenable']
	alternatepath = cjson['alternatepath']
	glacierenable = cjson['glacierenable']
	glaciersecretkey = cjson['glaciersecretkey']
	glacieraccesskey = cjson['glacieraccesskey']
	glacierregion = cjson['glacierregion']
	glaciervault = cjson['glaciervault']

	setbackup(backuppath);
	
	if alternateenable==1:
		global apath
		apath = alternatepath.split(',')
		for path in apath:
			setalternatebackup(path.strip());
	elif alternateenable==0:
		logging.info('Alternate backup skipped')
	else:
		logging.info('ALTERNATE ENABLE can either have 1 or 0')

	if cleanup==1:
		tabclean();
	elif cleanup==0:
		logging.info('Tableau cleanup skipped')
	else:
		logging.info('CLEANUP can either have 1 or 0')

	if logbackup==1:
		lbackup();
	elif logbackup==0:
		logging.info('Log backup skipped')
	else:
		logging.error('LOGBACKUP can either have 1 or 0')

	if databackup==1:
		dbackup();
	elif databackup==0:
		logging.info('Data backup skipped')
	else:
		logging.error('DATABACKUP can either have 1 or 0')

	if configbackup==1:
		cbackup();
	elif configbackup==0:
		logging.info('Config backup skipped')
	else:
		logging.error('CONFIG can either have 1 or 0')

	if restart==1:
		tabrestart();
		if warmup==1:
			tabwarm();
		elif warmup==0:
			logging.info('Warmup skipped')
		else:
			logging.error('WARMUP can either have 1 or 0')
	elif restart==0:
		logging.info('Tableau restart skipped')
	else:
		logging.error('RESTART can either have 1 or 0')

	if backupretention==1:
		bretention(logdays,'.zip',backuppath)
		bretention(datadays,'.tsbak',backuppath)
	elif backupretention==0:
		logging.info('Backup retention skipped')
	else:
		logging.error('RETENTION can either have 1 or 0')

	if s3enable==1:
		s3upload()
	elif s3enable==0:
		logging.info('Upload to S3 skipped')
	else:
		logging.error("AWSS3 ENABLE can either have 1 or 0")

	if glacierenable==1:
		glacierupload()
	elif glacierenable==0:
		logging.info('Upload to Glacier skipped')
	else:
		logging.error("AWSGLACIER ENABLE can either have 1 or 0")

	logging.info('Backup process completed')

	return 0

if __name__ == "__main__":
    sys.exit(main())