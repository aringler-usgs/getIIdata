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

#Here is where we will import our modules

from obspy import UTCDateTime
from obspy.core import read


debug = True


#Need to specify which station and day we want to get data for
#This should be added using argparser see line 155 to 177 or mdget.py 
net = 'II'
sta = 'PFO'
day = '001'
year = '2014'
loc = '00'
chan = 'LHZ'

#Need to make a UTCDateTime object
startTime = UTCDateTime(year + day +"T00:00:00.000")
endTime = startTime + 24*60*60
if debug:
	print "Here is our start time"
	print(startTime.formatIRISWebService())



#Need to pull the data
#Adam needs to clean this piece up 

webRequestString = 'http://service.iris.edu/fdsnws/dataselect/1/query?net=' + net + \
	'&sta=' + sta + '&loc=' + loc + '&cha=' + chan + '&start=' + \
	startTime.formatIRISWebService() + '&end=' + endTime.formatIRISWebService()
if debug:
	print webRequestString

#We have requested the data
try:
	blah = urllib.urlretrieve(webRequestString,filename='Blah.mseed')
	os.system('rdseed -f Blah.mseed -g /APPS/metadata/SEED/' + net + '.dataless -d -o 4')
	os.system('rm Blah.mseed')
	os.system('mv mini.seed ' + loc + '_' + chan + '.seed') 
except:
	print 'We were unable to get the data'



#Need to re-organize the data to be put in a location
#We still need to do this
#One parser flag could be to the local directory the other could go to /TEST_ARCHIVE









