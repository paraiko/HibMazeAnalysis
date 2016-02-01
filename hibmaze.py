#! /usr/bin/env python

from numpy import binary_repr
import numpy as np
import time
from operator import add

#maybe import re to load regular expression module
import re

#Make a function for the decimals to binary conversion
def decbin(DecNum):
	Bin=binary_repr(DecNum, width=8)
	return Bin
#Finished defining the decbin function

#Define file name and give a name to the output file
InFileName = '201010100_test.txt' # change a later stage to input from commandline or directory loop (sys.argv[1])
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


# aggregate over specified binsize (in sec) and output in new file
binsize = 600 #(10 min)
nrbins = int(86400 / binsize)
binnr = 0

#get the date from the filename and convert
datestr = InFileName[0:8]
unitnr = InFileName[8:9]
currday = time.strptime(datestr,"%Y%m%d")
startsec = int(time.mktime(currday))
binstart = startsec
binend = startsec + binsize



#loop over 1 day in binsize increments

#count the amount of eventsobjects in the day list
agr_day = list() # create new array for aggregated data 

#create list with 48 empty channels for use later
ech = list()
for i in range(0,47):
	ech.append(0)

firstBinEvent = True

#iterate over the events in de day list
for (i, event) in enumerate(day):
	
	#create a list for the aggreated data of the bin ([0]= seconds sinds start, [1] array with channeldata
	#bindata = list() 
	#convert datetime to seconds sinds epoch and add the milliseconds
	eventt = time.strptime(day[i][0],"%Y%m%d%H%M%S") 
	eventsec = int(time.mktime(eventt)) #+ float(day[i][1]) /1000
	#print binend - eventsec
	
	# add empty bins if necessary
	print (eventsec-startsec)/nrbins
	while (binstart <= eventsec-601):
		bindata = list()
		bindata.append(binnr)
		bindata.append(ech)
		agr_day.append(bindata)
		
		#increase with binsize
		binstart += binsize
		binend += binsize
		firstBinEvent = True
		binnr += 1
		
		#print str(binnr) + "empty event"
		#print bindata
	
	if eventsec < binend :
		#print str(eventsec) + " " + str(binend)
		bindata = list()
		if firstBinEvent :
			#add new line with empth channels
			bindata = list()
			bindata.append(binnr)
			bindata.append(ech)
			agr_day.append(bindata)
			
			#add the existing channel list with the values in the current events.
			agr_day[binnr][1] = map(add, agr_day[binnr][1], day[i][2])
			firstBinEvent = False
			
			print str(binnr) + "first event"
			#print bindata
			#print day[i][2]
		
		else :
			agr_day[binnr][1] = map(add, agr_day[binnr][1], day[i][2])
			#print str(binnr) + "second event"
		
	else :
		#proceed to next bin
		#increase with binsize
		binstart += binsize
		binend += binsize
		firstBinEvent = True 
		binnr += 1
		
		#add new line with empty channels
		bindata = list()
		bindata.append(binnr)
		bindata.append(ech)
		agr_day.append(bindata)
		agr_day[binnr][1] = map(add, agr_day[binnr][1], day[i][2])
		firstBinEvent = False
		print str(binnr) + "first event, next"
		
# print agr_day
		

		
	





# sum the 17 channels of 1 maze (frst maze starts at channel 0 2nd maze at channgel 24

	
	



print "Output printed to outfile"
#print day

OutFileName = InFileName + '_agr.txt' 


OutFile = open(OutFileName, 'w')
#loop through each line of the file to write it to OutFile2:
for bin in agr_day:
	OutFile.write("%s\n" % bin)


#OutFile2.write(DatumTijd + '\t' + ListBinary + '\n')
#However it does not work: TypeError: can only concatenate list (not "str") to list
# I don't understand this...
# also when trying OutFile2.write(ListBinary + '\n') it does not work...

#SearchStr = '(\d+)(\t)(\d+)'
#Datumtijd = Result.group(1)
#Binaries = list(Result.group(3))

