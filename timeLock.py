#!/usr/bin/env python2
#python2
import fileinput
import datetime
import hashlib


def getCode(hex):
	code = []
	#get first two letters
	for item in hex:
		try:
			int(hex[hex.index(item)])
		except:
			code.append(item)
		if len(code) == 2:
			break
	#get last two numbers
	for item in reversed(hex):
		if item.isdigit() == True:
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
	#easy checks
	if date.month >= 3 and date.month <= 11:
		#print("month is", date.month)
		#print("day is", date.weekday())
		return True
	else:
		return False

#test cases
#year, month, day , hour, min, sec
#now=datetime.datetime(2013,5,6,7,43,25) #in dls must sub 1 hr
#epoch=datetime.datetime(1999,12,31,23,59,59) #WORKS

#now=datetime.datetime(2017,03,23,18,02,06) #in dls
#epoch=datetime.datetime(2017,01,01,00,00,00) #WORKS!

#now=datetime.datetime(2015,05,15,14,00,0)
#epoch=datetime.datetime(2015,01,01,00,00,0) #WORKS

#now=datetime.datetime(2017,4,26,15,14,30)
#epoch=datetime.datetime(1974,6,1,8,57,23)



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

'''
print("epoch is", str(epoch))
print("current time", str(now))
print("time elapsed", totalSec)#timeElapsed.total_seconds())
'''
#compute md5 of of relevent 60 sec interval
#print("now seconds are",now.second)

beginInt =  totalSec - (totalSec % 60)

#print('begin interval is', beginInt)

m=hashlib.md5()
m.update(str(beginInt))
#print("first hash", m.hexdigest())


m2=hashlib.md5()
m2.update(m.hexdigest())
#print("second hash", m2.hexdigest())

getCode(m2.hexdigest())


'''
datetime library:
https://docs.python.org/2/library/datetime.html

time library:
https://docs.python.org/2/library/time.html

hashlib:
https://docs.python.org/2/library/hashlib.html#module-hashlib
'''
