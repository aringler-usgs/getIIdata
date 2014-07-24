#!/usr/bin/env python
# Runs GetIIData.py script

import getIIdata
import os

# For {net, stat, loc} wildcards use '?'
homedir = os.getcwd()
year = '2014'
startday = '001'
network = 'II'
getIIdata.Help()
obj = getIIdata.GetArgs(year, startday, network,\
			endday='002', station='PFO',\
			location='00', channel='LHZ',\
			debug="true", archive="true")
