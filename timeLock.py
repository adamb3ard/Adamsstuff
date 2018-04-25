#!/usr/bin/env python2
#python2

import fileinput
import datetime
import hashlib


def getCode(hex):
	code = []
	#get first two letters
	for item in hex:
		if item.isdigit() == False: #test if item is number
			code.append(item)
		if len(code) == 2:
			break

	#get last two numbers
	for item in reversed(hex):
		if item.isdigit() == True: #test if item is a number
			code.append(item)
		if len(code) == 4:
			break

	print ''.join(code)

'''
uses modern daylight saving rules to determine is date is in dls
2016 rule: starts second sunday in March and ends on first sunday in November
takes datetime and returns True if in DLS
'''
def checkDLS(date):
	#check months
	if date.month >= 3 and date.month <= 11:
		return True
	else:
		return False

now = datetime.datetime.now()
#now = datetime.datetime(2010,06,13,12,55,34) test stdin time
#read epoch from file and save to epoTime
for line in fileinput.input():
	epoTime = line.split()
epoch = datetime.datetime(int(epoTime[0]),int(epoTime[1]),int(epoTime[2]),int(epoTime[3]),int(epoTime[4]),int(epoTime[5]))


#NOW IS IN DLS; EPOCH NOT IN DLS
if checkDLS(now) == True and checkDLS(epoch) == False:
	now = now - datetime.timedelta(hours=1)#subtracts hour

#NOW IS IN DLS; EPOCH IS IN DLS
#do nothing

#NOW IS NOT IN DLS; EPOCH NOT IN DLS
# do nothing

#NOW IS NOT IN DLS; EPOCH IS IN DLS
if checkDLS(now) == False and checkDLS(epoch) == True:
	now = now + datetime.timedelta(hours=1)#adds hour

timeElapsed = now - epoch
totalSec = int(timeElapsed.total_seconds())


beginInt =  totalSec - (totalSec % 60)

#create new md5 object for each encryption
m=hashlib.md5()
m.update(str(beginInt))

m2=hashlib.md5()
m2.update(m.hexdigest())

getCode(m2.hexdigest())

'''
datetime library:
https://docs.python.org/2/library/datetime.html

time library:
https://docs.python.org/2/library/time.html

hashlib:
https://docs.python.org/2/library/hashlib.html#module-hashlib
'''
