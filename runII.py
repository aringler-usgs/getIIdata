#!/usr/bin/env python
# Runs GetIIData.py script

import getIIdata
import os

# For {net, stat, loc} wildcards use '?'
homedir = os.getcwd()
year = '2014'
startday = '003'
network = 'II'
getIIdata.Help()
obj = getIIdata.GetArgs(year, startday, network,\
			endday='013', station='KWAJ',\
			location='00', channel='LHZ',\
			debug="true", archive="true")


''' File "/home/mkline/dev/getIIdataBackup/MKline_AG/API/getIIdata/getIIdata.py", line 194, in storeMSEED
    self.stFinal = self.stFinal.split()
  File "/home/aringler/obspy-0.9.2/obspy/core/stream.py", line 2626, in split
    new_stream.extend(trace.split())
  File "/home/aringler/obspy-0.9.2/obspy/core/trace.py", line 1996, in split
    for slice in slices:
TypeError: 'NoneType' object is not iterable'''

