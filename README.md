getIIdata
=========

Repository to get different network data from IRIS 

Usage
=========

Usage:  This code pulls network data from IRIS and sets    
	it up to be put in a directory structure. The data that is pulled is     
	from the II network given the year and start day that the data is from.     
	The end day is an optional arguement; if no end day specified, it will      
	be one day after start day given. Station, location, and channel can be      
	wildcards or given a specific value. If the station, location, and channel       
	given do not return any data(trace(s)), IRIS did not collect data for       
	that specific start day given.  
    
	Optionally the user can:
        - choose the given start day to begin gathering data for (sday)
		- specify an end day to collect data for multiple days (eday)    
		- choose a specific station, location, and/or channel    
		- archive the data if it has yet to be stored in the directory structure   
	Arguments will be passed to:  
		- getIIdata.Help() 
		- getIIdata.GetArgs(posargs,optargs)    
		- posargs - positional arguments (network, year, startday)     
		- optargs - optional arguments (endday, station, location, channel, debug, archive)    

Example
=========

./runII.py 

		#Runs GetIIData.py script

import getIIdata    
import os

		#For {net, stat, loc} wildcards use '?'

homedir = os.getcwd()    
year = '2014'    
sday = 1
eday = 15
network = 'II'    
getIIdata.Help()
for curday in range (sday,eday): #to query data faster    
    startday = str(curday).zfill(3)    
    edday = str(curday + 1).zfill(3)    
    obj = getIIdata.GetArgs(year, startday, network,     
			endday=edday, station='?',     
			location='?', channel='LHZ',     
			debug="true", archive="true")    

