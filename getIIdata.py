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
import numpy.ma as ma

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

#One parser flag could be to the local directory the other could go to 
#/TEST_ARCHIVE

if archive:
	if debug:
		print "We are archiving the data to /TEST_ARCHIVE"

if True:
	if debug:
		print "We are writing the data" 
#Need to check if the directories exist and if not make them
	filename = loc + '_' + chan + '.512.seed'
	codepath = '/home/mkline/dev/getIIdata/TEST_ARCHIVE/'
	st.merge()
	st.sort()
	st.count()
	days = int(round((st[0].stats.endtime - st[0].stats.starttime)/(24*60*60)))
	stFinal = Stream()
	
	for dayIndex in range(0,days):
	#You will want to put the directory structures in here since you won't want to
	#add directory structures that you don't use
		if not os.path.exists(codepath + net + '_' + sta  + '/'):
			os.mkdir(codepath + net + '_' + sta  + '/')
		if not os.path.exists(codepath + net + '_' + sta  + '/' + year + '/'):
			os.mkdir(codepath + net + '_' + sta  + '/' + year + '/')
		print "Day properties: "
		print(dayIndex)
		trimStart = st[0].stats.starttime + (dayIndex)*24*60*60
		trimEnd = st[0].stats.starttime + (dayIndex+1)*24*60*60
		print(trimStart)
		print(trimEnd)
		print
		timesplit = re.split('T', str(trimStart))
		s = timesplit[0]
		timesplit1 = re.split('-', s)
		NewStartDay = '0' + timesplit1[2]
		if not os.path.exists(codepath + net + '_' + sta  + '/' + year + '/' \
			+ year + '_' + NewStartDay+ '/'):
			os.mkdir(codepath + net + '_' + sta  + '/' + year + '/' \
			+ year + '_' + NewStartDay + '/')
		stFinal = st.copy()
		stFinal.trim(starttime = trimStart, endtime = trimEnd)	

		# Here we write the data using STEIM 2 and 512 record lengths
		#stFinal.write(stFinal[0].stats.location + '_' + stFinal[0].stats.channel + 				'.512.seed', format='MSEED', reclen = 512, encoding='STEIM2')	
		
#This is the error code I get when the above statement is uncommented.
'''Traceback (most recent call last):
  File "./getIIdata.py", line 177, in <module>
    stFinal.write(stFinal[0].stats.location + '_' + stFinal[0].stats.channel + 			'.512.seed', format='MSEED', reclen = 512, encoding='STEIM2')	
  File "/home/aringler/obspy-0.9.2/obspy/core/stream.py", line 1331, in write
    raise NotImplementedError(msg)
NotImplementedError: Masked array writing is not supported. You can use np.array.filled() to convert the masked array to a normal array.'''

	print stFinal
	#stFinal.write(loc + '_' + chan + '.512.seed', format='MSEED', 
		#reclen = 512,encoding='STEIM2')	




