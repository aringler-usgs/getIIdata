#!/usr/bin/env python

###################################################################################################
#This code pulls II data from IRIS and sets it up to be put in a directory structure
#
#
#
#
###################################################################################################


#TO DO: Add comments, update readme, finish additions to code
#Add wildcards

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
#This should be added using argparser see line 155 to 177 or mdget.py 
parser = argparse.ArgumentParser(description='Code to get dataless from getIIdata.py')

parser.add_argument('-y','--year      ', action = "store",dest="year", \
default = "*", help="Year of collected data: YYYY", type = str, required = True)

parser.add_argument('-j','--day        ', action = "store",dest="day", \
default = "*", help="Day of collected data: DDD", type = str, required = True)

parser.add_argument('-n','--network', action = "store",dest="network", \
default = "*", help="Name of the network of interest: NN", type = str, required = True)

parser.add_argument('-s','--station', type = str, action = "store", dest="station", \
default = "*", help="Name of the station of interest: SSSSS", required = True)

parser.add_argument('-l','--location', type = str, action = "store", dest="location", \
default = "*", help="Name of the location of interest: LL", required = True)

parser.add_argument('-c','--channel', action = "store",dest="channel", \
default ="*", help="Name of the channel of interest: CCC", type = str, required = True)

parser.add_argument('-d','--debug',action = "store_true",dest="debug", \
default = True, help="Run in debug mode")

parserval = parser.parse_args()

year = parserval.year
day = parserval.day
net = parserval.network
sta = parserval.station
loc = parserval.location
chan = parserval.channel

#Here is debug mode
if parserval.debug:
	debug = True
else:
	debug = False

#Need to make a UTCDateTime object
startTime = UTCDateTime(year + day +"T00:00:00.000")
endTime = startTime + 24*60*60
if debug:
	print "Here is our start time" + startTime.formatIRISWebService()
	print "Here is our end time" + endTime.formatIRISWebService()

#Need to pull the data
client = Client()
try:
	st = client.get_waveforms(net,sta,loc,chan,startTime,endTime)
	for tr in st:
#Here we remove the M data quality and go with D
		tr.stats.mseed['dataquality'] = 'D'
		if debug:
			print "Here is a trace we have"
			print(tr.stats)
except:
	print 'Trouble getting data'
	sys.exit(0)

try:
#Here we write the data using STEIM 2 and 512 record lengths
	st.write(loc + '_' + chan + '.512.seed',reclen=512, format='MSEED',encoding='STEIM2')
	if debug:
		print "We are writing the data"
except:
	print 'Problem writing data'
	sys.exit(0)


#Need to re-organize the data to be put in a location
#We still need to do this
#One parser flag could be to the local directory the other could go to /TEST_ARCHIVE









