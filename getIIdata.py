#!/usr/bin/env python

###################################################################################################
#This code pulls network data from IRIS and sets it up to be put in a directory structure
#
#
#
#
###################################################################################################


#TO DO: Add start and end day to parser
#	Create directory structure to add to /TEST_ARCHIVE
#	Finish adding wildcards
#	If not adding the data to /TEST_ARCHIVE we should include the station


import glob
import urllib
import os
import argparse
import sys
import datetime
import re, string, time

#Here is where we will import our modules

from obspy import UTCDateTime
from obspy.core import read
from obspy.core.trace import Trace
from obspy.core.stream import Stream
from obspy.core.utcdatetime import UTCDateTime
from obspy.fdsn import Client

#Need to specify which station and day we want to get data for
#Need to add an alternate to -j which would be a start and end day
parser = argparse.ArgumentParser(description='Code to get dataless from getIIdata.py')

parser.add_argument('-y', action = "store",dest="year", \
default = "*", help="Year of collected data: YYYY", type = str, required = True)

parser.add_argument('-sd','--start day        ', action = "store",dest="startday", \
default = "*", help="Day of collected data: DDD", type = str, required = True)

parser.add_argument('-ed','--end day        ', action = "store",dest="endday", \
default = "*", help="Day of collected data: DDD", type = str, required = True)

parser.add_argument('-nslc', action = "store", dest= "nslc" , nargs = "+" , \
help="Enter NN SSSSS LL CCC cannot wildcard network", type = str, required = True)

parser.add_argument('-d','--debug',action = "store_true",dest="debug", \
default = False, help="Run in debug mode")

parser.add_argument('-a','--archive',action = "store_true",dest="archive", \
default = False, help="Archive the data in /TEST_ARCHIVE")

parserval = parser.parse_args()

#Here is debug mode
if parserval.debug:
	debug = True
else:
	debug = False

try:
	year = parserval.year
	startday = parserval.startday
	endday = parserval.endday
	net = parserval.nslc[0]
	sta = parserval.nslc[1]
	loc = parserval.nslc[2]
	chan = parserval.nslc[3]
	archive = parserval.archive
	if debug:
		print "Year: " + year
		print "Start Day: " + startday
		print "End Day: " + endday
		print "Net: " + net
		print "Station: " + sta
		print "Location: " + loc
		print "Channel: " + chan
except:
	print "Can not read in values"
	sys.exit(0)

#Here we reparse the wildcards
if loc == "?":
	loc = "*"
if sta == "?":
	sta = "*"
if chan == "?":
	chan = "*"

if net == "?":
	print "Wildcarding a network is not allowed"
	sys.exit(0)


#Here we set the day and year to a UTCDateTime object
startTime = UTCDateTime(year + startday +"T00:00:00.000")
#If no end day in parser default to 1 day
if endday == "?":
	endTime = startTime + 24*60*60
else: 
	endTime = UTCDateTime(year + endday +"T00:00:00.000")

if debug:
	print "Here is our start time " + startTime.formatIRISWebService()
	print "Here is our end time   " + endTime.formatIRISWebService()
	print 	

#Here we pull the data
client = Client("IRIS")
try:
	requestArray = [(net,sta,loc,chan,startTime,endTime)]
	if debug:
		print(requestArray)
		print 
	st = client.get_waveforms_bulk(requestArray)
	for tr in st:
#Here we remove the M data quality and go with D
		tr.stats.mseed['dataquality'] = 'D'
		if debug:
			print "Here is a trace we have"
			print(tr.stats)
			print 
except:
	print 'Trouble getting data'
	sys.exit(0)

#Need to re-organize the data to be put in a location
#We still need to do this
#One parser flag could be to the local directory the other could go to 
#/TEST_ARCHIVE


if archive:
	if debug:
		print "We are archiving the data to /TEST_ARCHIVE"
#Need to check if the directories exist and if not make them
filename = loc + '_' + chan + '.512.seed'
pathtoseed = '/home/mkline/dev/getIIdata/src/'
codepath = '/home/mkline/dev/getIIdata/TEST_ARCHIVE/'

if not os.path.exists(codepath + net + '_' + sta  + '/'):
	os.mkdir(codepath + net + '_' + sta  + '/')
os.chdir(codepath + net + '_' + sta  + '/')

if not os.path.exists(codepath + net + '_' + sta  + '/' + year + '/'):
	os.mkdir(codepath + net + '_' + sta  + '/' + year + '/')
os.chdir(codepath + net + '_' + sta  + '/' + year + '/')

if not os.path.exists(codepath + net + '_' + sta  + '/' + year + '/' \
	+ year + '_' + startday + '/'):
	os.mkdir(codepath + net + '_' + sta  + '/' + year + '/' \
	+ year + '_' + startday + '/')
os.chdir(codepath + net + '_' + sta  + '/' + year + '/' \
	+ year + '_' + startday + '/')

#Now save the data into the directory

#Here we write the data into the local directory

#Here we write the data using STEIM 2 and 512 record lengths
try:
	if debug:
		print "We are writing the data" 
	
	'''for tr in st:
		mytraces = []
		print tr
		print tr.stats.location
		print tr.stats.channel
		tr.write(tr.stats.location + '_' + tr.stats.channel + \
			'.512.seed',reclen=512,format='MSEED',
			encoding='STEIM2')
		mytraces.append(tr.write)
		print mytraces'''
	
	st.write(st[0].stats.location + '_' + st[0].stats.channel + \
			'.512.seed', format='MSEED', encoding='STEIM2')
	stnew = st
	stnew.merge()
	'''
	print st
	print
	if len(st) > 2:
		stnew = st[0]
		for i in range(1, len(st)):
			print "i = %d" % i
			stnew = stnew + st[i]
		print stnew
	elif len(st) == 2:
		stnew = st[0] + st[1]
		print stnew
	else:
		stnew = st[0]
		print stnew
	'''
#This is me trying to split the traces into separate days.
	stcopy = stnew
	mytraces = Stream()
	print "This is the trace we are splitting: "
	print
	tracestart = stnew.stats.starttime
	traceend = stnew.stats.starttime + (60*60*24)-1
	print "Day Trace start: " + str(tracestart)
	print "Day Trace end:   " + str(traceend)
	while tracestart < stnew.stats.endtime:
		stcopy = stnew
		trace = stcopy.trim(starttime=tracestart, endtime=traceend)
		mytraces += trace
		print "This is the trace of the first day: "
		print trace
		print 
		print stcopy
		print "new trace we are splitting: "
		print stcopy
		tracestart = traceend + (60*60*24)
		traceend = tracestart + (60*60*24)-1
		print "Day Trace start: " + str(tracestart)
		print "Day Trace end:   " + str(traceend)
	print "These are the separated traces: " 
	print(mytraces)
#Need to convert date to julian day
#this needs to be done in a loop for multiple days
	#tt.tm_yday = 0
	
	'''while tt.tm_yday < endday: # this need to be the endday that is requested
		daytraces = []
		fmt1 = '%Y-%m-%d'
		tstart = newtr.stats.starttime
		tend = tstart + (60*60*24) - 1
		tstart_string = str(tstart)
		timesplit = re.split('T', tstart_string)
		s = timesplit[0]
		dt = datetime.datetime.strptime(s,fmt)
		tt = dt.timetuple()
		daytraces.append(dt)
		print tt.tm_yday
		print daytraces
		tend = tend + 1'''
# idea behind this is to separate the traces into complete days, trying to attach the days
# in a stream and pull each one out separately into its own directory.
except:
	print 'Problem writing data'
	sys.exit(0)

'''#Just me fooling around with array shit
t1 = st[0 + 1]
print t1
t2 = st[1]
print t2
print ' '
print st'''




