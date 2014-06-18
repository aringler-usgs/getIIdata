getIIdata
=========

Repository to get different network data from IRIS 

Usage
=========

usage: getIIdata.py [-h] -y YEAR -j DAY -nslc NSLC [NSLC ...] [-d] [-a]

Code to get dataless from getIIdata.py

optional arguments:
  -h, --help            show this help message and exit
  -y YEAR               Year of collected data: YYYY
  -j DAY, --day         DAY
                        Day of collected data: DDD
  -nslc NSLC [NSLC ...]
                        Enter NN SSSSS LL CCC
  -d, --debug           Run in debug mode
  -a, --archive         Archive the data in /TEST_ARCHIVE

Example
=========

./getIIdata.py -y 2014 -j 001 -nslc IU ANMO ? LHZ -d

TO DO
=========

Add start and end day to parser
Create directory structure to add to /TEST_ARCHIVE
Finish adding wildcards
If not adding the data to /TEST_ARCHIVE we should include the station
