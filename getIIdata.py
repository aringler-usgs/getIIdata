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

#Here is where we will import our modules

from obspy import UTCDateTime
from obspy.core import read
from obspy.fdsn import Client

#Need to specify which station and day we want to get data for
#Need to add an alternate to -j which would be a start and end day
parser = argparse.ArgumentParser(description='Code to get dataless from getIIdata.py')

parser.add_argument('-y', action = "store",dest="year", \
default = "*", help="Year of collected data: YYYY", type = str, required = True)

parser.add_argument('-j','--day        ', action = "store",dest="day", \
default = "*", help="Day of collected data: DDD", type = str, required = True)

parser.add_argument('-nslc', \
action = "store", dest= "nslc" , nargs = "+" , \
help="Enter NN SSSSS LL CCC", type = str, required = True)

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
	day = parserval.day
	net = parserval.nslc[0]
	sta = parserval.nslc[1]
	loc = parserval.nslc[2]
	chan = parserval.nslc[3]
	archive = parserval.archive
	if debug:
		print "Year: " + year
		print "Day: " + day
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

#Need to reparse each possible wildcard do station and channel

if net == "?":
	print "Wildcarding a network is not allowed"
	sys.exit(0)


#Here we set the day and year to a UTCDateTime object
startTime = UTCDateTime(year + day +"T00:00:00.000")
endTime = startTime + 24*60*60
if debug:
	print "Here is our start time" + startTime.formatIRISWebService()
	print "Here is our end time" + endTime.formatIRISWebService()

#Here we pull the data
client = Client("IRIS")
try:
	requestArray = [(net,sta,loc,chan,startTime,endTime)]
	if debug:
		print(requestArray)
	st = client.get_waveforms_bulk(requestArray)
	for tr in st:
#Here we remove the M data quality and go with D
		tr.stats.mseed['dataquality'] = 'D'
		if debug:
			print "Here is a trace we have"
			print(tr.stats)
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

#Now save the data into the directory

else:
#Here we write the data into the local directory
	try:
#Here we write the data using STEIM 2 and 512 record lengths
		for tr in st:
			tr.write(tr.stats.location + '_' + tr.stats.channel + \
				'.512.seed',reclen=512,format='MSEED',
				encoding='STEIM2')
		if debug:
			print "We are writing the data"
	except:
		print 'Problem writing data'
		sys.exit(0)





