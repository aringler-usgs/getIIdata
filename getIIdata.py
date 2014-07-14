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
DupStations = []
DupLocations = []
DupChannels = []
STAWILD = False
LOCWILD = False
CHANWILD = False
try:
	requestArray = [(net,sta,loc,chan,startTime,endTime)]
	if debug:
		print(requestArray)
		print 
	st = client.get_waveforms_bulk(requestArray)
#	print st
#	sys.exit(0)
	for tr in st:
		#Here we remove the M data quality and go with D
		tr.stats.mseed['dataquality'] = 'D'
		if debug:
			#print "Here is a trace we have"
			#print(tr.stats)
			if sta == '*':
				STAWILD = True
				DupStations.append(tr.stats.station)				
		    	elif sta != '*':
                		STAWILD = False

            		if loc == '*':
				LOCWILD = True	
                		DupLocations.append(tr.stats.location)
		    	elif loc != '*':
				LOCWILD = False 
			
			if chan == '*':
				CHANWILD = True	
                		DupChannels.append(tr.stats.channel)
		    	elif chan != '*':
				CHANWILD = False 
except:
	print 'Trouble getting data'
	sys.exit(0)
#takes duplicate stations out of list
stations = list(set(DupStations))
locations = list(set(DupLocations))
channels = list(set(DupChannels))
print stations
print locations
print channels
#One parser flag could be to the local directory the other could go to 
#/TEST_ARCHIVE
if archive:
	if debug:
		print "We are archiving the data to /TEST_ARCHIVE"

if True:
	if debug:
		print "We are writing the data" 

	#Need to check if the directories exist and if not make them
	#Main program
	codepath = '/home/mkline/dev/getIIdata/TEST_ARCHIVE/'
	days = int(round((st[-1].stats.endtime - st[0].stats.starttime)/(24*60*60)))
	stFinal = Stream()

	if STAWILD:
		for sta in stations:
			trace = st.select(station = sta)
			trace.merge()
			trace.sort()
			trace.count()
			#Converting date into julian day
			#this is here to make sure that all the traces start on the same day
			timesplit = re.split('T', str(trace[0].stats.starttime))
			s = timesplit[0]
			fmt = '%Y-%m-%d'
			dt = datetime.datetime.strptime(s, fmt)
			tt = dt.timetuple()
			if tt.tm_yday < 10:
				NewStartDay = '00' + str(tt.tm_yday)
			elif tt.tm_yday < 100:
				NewStartDay = '0' + str(tt.tm_yday)
			else:
				NewStartDay = str(tt.tm_yday)
			#index error if these dont match for the given station
			if startday != NewStartDay :
				stations.remove(sta)
				print "This station doesnt have seed data for this day"
			else:
				for dayIndex in range(0,days):
					print "Day properties: "
					trimStart = trace[0].stats.starttime + (dayIndex)*24*60*60
					trimEnd = trace[0].stats.starttime + (dayIndex+1)*24*60*60
					print "Start of day: " + str(trimStart)
					print "End of day:   " + str(trimEnd)
					#Converting date into julian day
					timesplit = re.split('T', str(trimStart))
					s = timesplit[0]
					fmt = '%Y-%m-%d'
					dt = datetime.datetime.strptime(s, fmt)
					tt = dt.timetuple()
					if tt.tm_yday < 10:
						NewStartDay = '00' + str(tt.tm_yday)
					elif tt.tm_yday < 100:
						NewStartDay = '0' + str(tt.tm_yday)
					else:
						NewStartDay = str(tt.tm_yday)
					stFinal = trace.copy()
					stFinal.trim(starttime = trimStart, endtime = trimEnd)	
					stFinal = stFinal.split()
					#Added the directory structures in here since you won't want to
					#add directory structures that you don't use
					if not os.path.exists(codepath + net + '_' + sta  + '/'):
						os.mkdir(codepath + net + '_' + sta  + '/')
					if not os.path.exists(codepath + net + '_' + sta  + '/' + year + '/'):
						os.mkdir(codepath + net + '_' + sta  + '/' + year + '/')
					stpath = codepath + net + '_' + sta  + '/' + year + '/' \
						+ year + '_' + NewStartDay + '/'
					if not os.path.exists(stpath):
						os.mkdir(stpath)
					# Here we write the data using STEIM 2 and 512 record lengths
					stFinal.write(stpath + stFinal[0].stats.location + '_' + stFinal[0].stats.channel \
						+ '.512.seed', format='MSEED',reclen = 512, encoding='STEIM2')
					print stFinal
					print
    	elif LOCWILD: 
		for loc in locations:
			trace = st.select(location = loc)
			trace.merge()
			trace.sort()
			trace.count()
			print "For station: " + sta
			for dayIndex in range(0,days):
				print "Day properties: "
				trimStart = trace[0].stats.starttime + (dayIndex)*24*60*60
				trimEnd = trace[0].stats.starttime + (dayIndex+1)*24*60*60
				print "Start of day: " + str(trimStart)
				print "End of day:   " + str(trimEnd)
				#Converting date into julian day
				timesplit = re.split('T', str(trimStart))
				s = timesplit[0]
				fmt = '%Y-%m-%d'
				dt = datetime.datetime.strptime(s, fmt)
				tt = dt.timetuple()
				if tt.tm_yday < 10:
					NewStartDay = '00' + str(tt.tm_yday)
				elif tt.tm_yday < 100:
					NewStartDay = '0' + str(tt.tm_yday)
				else:
					NewStartDay = str(tt.tm_yday)
				stFinal = trace.copy()
				stFinal.trim(starttime = trimStart, endtime = trimEnd)	
				stFinal = stFinal.split()
				#Added the directory structures in here since you won't want to
				#add directory structures that you don't use
				#problem with this is the current loop does not run through all of the stations!
				print
				if not os.path.exists(codepath + net + '_' + sta  + '/'):
					os.mkdir(codepath + net + '_' + sta  + '/')
				if not os.path.exists(codepath + net + '_' + sta  + '/' + year + '/'):
					os.mkdir(codepath + net + '_' + sta  + '/' + year + '/')
				stpath = codepath + net + '_' + sta  + '/' + year + '/' \
					+ year + '_' + NewStartDay + '/'
				if not os.path.exists(stpath):
					os.mkdir(stpath)
				print
				# Here we write the data using STEIM 2 and 512 record lengths
				stFinal.write(stpath + stFinal[0].stats.location + '_' + stFinal[0].stats.channel \
					+ '.512.seed', format='MSEED',reclen = 512, encoding='STEIM2')
				print stFinal
