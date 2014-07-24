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
		- specify an end day to collect data for multiple days    
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
startday = '001'    
network = 'II'    
getIIdata.Help()    
obj = getIIdata.GetArgs(year, startday, network, 
			endday='002', station='?', 
			location='00', channel='LHZ', 
			debug="true", archive="true")

