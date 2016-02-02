#! /usr/bin/env python

from numpy import binary_repr
import numpy as np
import time
import re
import os
from operator import add

#Make a function for the decimals to binary conversion
def decbin(DecNum):
	Bin=binary_repr(DecNum, width=8)
	return Bin
#Finished defining the decbin function

###############
###  read data from input file and store in list for further processing ###

for file in os.listdir("."):
    if file.endswith(".txt"):
	#Define file name and give a name to the output file
	InFileName = file # change a later stage to input from commandline or directory loop (sys.argv[1])
	#OutFileName = InFileName + 'bin.txt' 

	InFile = open(InFileName, 'r')
	#OutFile = open(OutFileName, 'w')

	day = list()

	#loop through each line in the file
	for Line in InFile:
		#Strip the line endings and white space
		Line=Line.strip()
		linelist= list()	
		#Split by one more occurrence of a space
		ElementList = re.split(" +", Line)

		#Format the date in one string add trailing zeros and separate milliseconds by:
		DateTime=str(ElementList[0])+str(ElementList[1]).zfill(2)+ \
		str(ElementList[2]).zfill(2)+str(ElementList[3]).zfill(2)+ \
		str(ElementList[4]).zfill(2)+ str(ElementList[5]).zfill(2)

		millisec = str(ElementList[6]).zfill(3)
		#OutFile.write(Time + '\t')
	
		#append datatime on the first position of the linelist
		linelist.append(DateTime)
		linelist.append(millisec)

		binstring = ""
		#convert the channels to binary data and store in array on 3rd position for each column in the range of 7 until 13,
		for Column in range(7,13):
			#write the binary number in integer form, followed by an end-of-line in the OutFile
			binstring += decbin(int(ElementList[Column]))
	
		channel = list()
		# for each character in col[1] (i) in range 0-47,
		# append the integer of it to the list 'channel'
		for i in range(0,47):
			#ch = int(col[1][i])
			ch = int(binstring[i])
			if ch > 0:
				ch = 0
			else:
				ch = 1 
		
			channel.append(ch)
	
		# append the list 'channel' (3rd dimension) to the list 'linelist' (2nd dimension)
		linelist.append(channel)
		# append the list 'linelist' to the list 'dag' (1st dimension)
		day.append(linelist)

	#Close the input file
	InFile.close()

	#print day
	#TempOutFileName = InFileName + 'temp.txt' 
	#OutFile = open(TempOutFileName, 'w')
	#for bin in day:
	#	OutFile.write("%s\n" % bin)
	#OutFile.close()

	###############
	###  aggregate over specified binsize (in sec) and output in new file ###

	binsize = 120 #(10 min)
	nrbins = int(86400 / binsize)
	binnr = 0

	#get the date from the filename and convert
	datestr = InFileName[0:8]
	unitnr = InFileName[8:9]
	currday = time.strptime(datestr,"%Y%m%d")
	startsec = time.mktime(currday)
	binstart = startsec
	binend = startsec + binsize

	#create list with 48 empty channels for use later
	ech = list()
	for i in range(0,47):
		ech.append(0)

	# create new array for aggregated data	
	agr_day = list() 

	#loop over 1 day in binsize increments as long as there are elements
	nrevents = len(day)
	ev = 0
	getNewEv = False
	eventt = time.strptime(day[ev][0],"%Y%m%d%H%M%S") 
	evsec = time.mktime(eventt) #+ float(day[i][1]) /1000

	#create the first bin
	bin = list()
	bin.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(binend)))
	bin.append(ech)

	while (True):
		if getNewEv:
			getNewEv = False
			ev += 1
	
			if ev >= nrevents:
				# break out of the loop if there are no more new events.
				agr_day.append(bin)
				break
			else:
				eventt = time.strptime(day[ev][0],"%Y%m%d%H%M%S") 
				evsec = time.mktime(eventt)
		
		if evsec > binend:
			#write the current bin
			agr_day.append(bin)
			binstart += binsize
			binend += binsize
	
			#create a new bin
			bin=list()
			bin.append(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(binend)))
			bin.append(ech)
			
		elif evsec > binstart and evsec <= binend: 
			getNewEv = True
			#add the existing channel list with the values in the current events.
			bin[1] = map(add, bin[1], day[ev][2])
	
		else:
			bin=list()
			bin.append(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(binend)))
			bin.append(ech)
			agr_day.append(bin)
			binstart += binsize
			binend += binsize
	
	
	#print agr_day


	# sum the 17 channels of 1 maze (frst maze starts at channel 0 2nd maze at channgel 24


	OutFileName = InFileName + '_' + str(binsize) + '.agr' 
	OutFile = open(OutFileName, 'w')
	#loop through each line of the file to write it to OutFile2:
	for bin in agr_day:
		OutFile.write("%s\n" % bin)
	print "Output printed to " + OutFileName

	#OutFile2.write(DatumTijd + '\t' + ListBinary + '\n')
	#However it does not work: TypeError: can only concatenate list (not "str") to list
	# I don't understand this...
	# also when trying OutFile2.write(ListBinary + '\n') it does not work...

	#SearchStr = '(\d+)(\t)(\d+)'
	#Datumtijd = Result.group(1)
	#Binaries = list(Result.group(3))

