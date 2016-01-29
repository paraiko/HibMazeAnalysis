#! /usr/bin/env python

from numpy import binary_repr
import numpy as np
#import os #maybe for the more files

#maybe import re to load regular expression module
import re

#Make a function for the decimals to binary conversion
def decbin(DecNum):
	Bin=binary_repr(DecNum, width=8)
	return Bin
#Finished defining the decbin function

#Define file name and give a name to the output file
InFileName = '201010100_test.txt' #sys.argv[1]
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
	
print "Output printed to outfile"
	
#Close the files
InFile.close()

#print the 3D list 'dag'	
print day	

#loop through each line of the file to write it to OutFile2:
#for line in dag:
#	OutFile2.write("%s\n" % line)


#OutFile2.write(DatumTijd + '\t' + ListBinary + '\n')
#However it does not work: TypeError: can only concatenate list (not "str") to list
# I don't understand this...
# also when trying OutFile2.write(ListBinary + '\n') it does not work...

#SearchStr = '(\d+)(\t)(\d+)'
#Datumtijd = Result.group(1)
#Binaries = list(Result.group(3))

