"""
A set of functions for retrieving previous instant message conversations.
All functions return an interable whose items are tuples in the form of:
(date/time,screenname,message)
"""

import os,re
from datetime import datetime

recordre=re.compile(r'^\((\d\d?\:\d\d\:\d\d(\s+[A|P]M)?)\)\s+(.*?)\:\s+(.*)\s*$', re.I|re.L)

def PidginLogs(LogDir):
	"""Returns all conversations by parsing Pidgin log files"""
	assert os.path.isdir(LogDir), 'Not a directory: '+str(LogDir)
	messages=[]
	for d in [LogDir+os.sep+f for f in os.listdir(LogDir) if os.path.isdir(LogDir+os.sep+f)]:
		for logf in os.listdir(d):
			doy=logf.split('.')[0]
			logf=d+os.sep+logf
			for rec in open(logf).readlines()[1:]:
				messages.append(_ParsePidginRecord(rec,doy))
	return messages


def _ParsePidginRecord(recordtext,dayofyear):
	m=recordre.search(recordtext.strip())
	if not m:
		raise ValueError("malformed log record: '%s'"%recordtext.strip())
	tod,isampm,scrnname,msg=m.groups()
	if isampm:
		dtime=datetime.strptime('%s %s'%(dayofyear,tod), '%Y-%m-%d %I:%M:%S %p')	
	else:
		dtime=datetime.strptime('%s %s'%(dayofyear,tod), '%Y-%m-%d %I:%M:%S')
	return (dtime,scrnname,msg,)
