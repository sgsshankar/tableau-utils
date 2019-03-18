"""
Shared module to read configuration files
"""

__author__      = "Shankar Narayanan SGS"
__copyright__   = "Copyright , Shankar Narayanan SGS"
__website__		= "www.shankarnarayanan.com"

import configparser
import sys
import logging
import json

logfile = "log.txt"
cjson = {}

#tableau variables
binpath=None
backupname=None
logbackup=None
databackup=None
cleanup=None
restart=None
warmup=None
bconfig=None

#backup variables
backuppath=None
backuppath=None
backupretention=None
logdays=None
datadays=None

#alternate backup variables
alternateenable=None
alternatepath=None

#s3 variables
s3enable=None
s3accesskey=None
s3secretkey=None
s3bucket=None

#glacier variables
glacierenable=None
glacieraccesskey=None
glaciersecretkey=None
glacierregion=None
glaciervault=None

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, filename = logfile,level=logging.DEBUG)

#reading config file
def readConfig (configloc):

	try:
		config = configparser.ConfigParser()
		config.read(configloc)
		global binpath,backupname,logbackup,databackup,backuppath,backupretention,logdays,datadays,cleanup,restart,s3enable,s3accesskey,s3secretkey,s3bucket,warmup,bconfig,alternateenable,alternatepath,glacierenable,glaciersecretkey,glacieraccesskey,glacierregion,glaciervault

		#read tableau variables
		binpath = config['TABLEAU']['BINPATH']
		cjson['binpath'] = binpath
		backupname = config['TABLEAU']['BACKUPNAME']
		cjson['backupname'] = backupname
		logbackup = config['TABLEAU']['LOGBACKUP']
		logbackup = int(logbackup)
		cjson['logbackup'] = logbackup
		databackup = config['TABLEAU']['DATABACKUP']
		databackup = int(databackup)
		cjson['databackup'] = databackup
		cleanup = config['TABLEAU']['CLEANUP']
		cleanup = int(cleanup)
		cjson['cleanup'] = cleanup
		restart = config['TABLEAU']['RESTART']
		restart = int(restart)
		cjson['restart'] = restart
		warmup = config['TABLEAU']['WARMUP']
		warmup = int(warmup)
		cjson['warmup'] = warmup
		configbackup = config['TABLEAU']['CONFIGBACKUP']
		configbackup = int(bconfig)
		cjson['bconfig'] = bconfig

		#read backup variables
		backuppath = config['TSBACK']['PATH']
		cjson['backuppath'] = backuppath
		backupretention = config['TSBACK']['RETENTION']
		backupretention = int(backupretention)
		cjson['backupretention'] = backupretention
		logdays = config['TSBACK']['LOGDAYS']
		logdays = int(logdays)
		cjson['logdays'] = logdays
		datadays = config['TSBACK']['DATADAYS']
		datadays = int(datadays)
		cjson['datadays'] = datadays

		#read alternate backup variables
		alternateenable = config['ALTERNATE']['ENABLE']
		alternateenable = int(alternateenable)
		cjson['alternateenable'] = alternateenable
		alternatepath = config['ALTERNATE']['PATH']
		cjson['alternatepath'] = alternatepath

		#read s3 variables
		s3enable = config['AWSS3']['ENABLE']
		s3enable = int(s3enable)
		cjson['s3enable'] = s3enable
		s3accesskey = config['AWSS3']['ACCESSKEY']
		cjson['s3accesskey'] = s3accesskey
		s3secretkey = config['AWSS3']['SECRETKEY']
		cjson['s3secretkey'] = s3secretkey
		s3bucket = config['AWSS3']['BUCKET']
		cjson['s3bucket'] = s3bucket

		#read glacier variables
		glacierenable = config['AWSGLACIER']['ENABLE']
		glacierenable = int(glacierenable)
		cjson['glacierenable'] = glacierenable
		glacieraccesskey = config['AWSGLACIER']['ACCESSKEY']
		cjson['glacieraccesskey'] = glacieraccesskey
		glaciersecretkey = config['AWSGLACIER']['SECRETKEY']
		cjson['glaciersecretkey'] = glaciersecretkey
		glacierregion = config['AWSGLACIER']['REGION']
		cjson['glacierregion'] = glacierregion
		glaciervault = config['AWSGLACIER']['VAULT']
		cjson['glaciervault'] = glaciervault

		logging.info('Read config file')

		return cjson

	except:
		logging.exception('Error in reading log file')

	return;