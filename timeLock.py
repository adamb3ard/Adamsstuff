#!/usr/bin/env python2
#python2
import fileinput
import datetime
import hashlib

#todo check for DLS and figure out what to do if times are in it or not
def getCode(hex):
	output = []
	#get first two letters
	for item in hex:
		try:
			int(hex[hex.index(item)])
		except:
			output.append([item])
		if len(output) == 2:
			break
	#get last two numbers
	for item in reversed(hex):
		if item.isdigit() == True:
			output.append(item)
		if len(output) == 4:
			break


	print(output)

'''
uses modern daylight saving rules to determine is date is in dls
2016 rule: starts second sunday in March and ends on first sunday in November
takes datetime and returns True if in DLS
'''
def checkDLS(date):
	#easy checks
	if date.month > 3 and date.month < 11:
		print("month is", date.month)
		print("day is", date.weekday())
		return True
	else:
		return False

#test cases
#year, month, day , hour, min, sec
now=datetime.datetime(2013,05,06,07,43,25) #in dls must sub 1 hr
epoch=datetime.datetime(1999,12,31,23,59,59) #WORKS

#now=datetime.datetime(2017,03,23,18,02,06)
#epoch=datetime.datetime(2017,01,01,00,00,00)

#now=datetime.datetime(2015,05,15,14,00,0)
#epoch=datetime.datetime(2015,01,01,00,00,0)

'''
now = datetime.datetime.now()

#read epoch from file and save to epoTime
for line in fileinput.input():
	epoTime = line.split()
epoch = datetime.datetime(int(epoTime[0]),int(epoTime[1]),int(epoTime[2]),int(epoTime[3]),int(epoTime[4]),int(epoTime[5]))
'''

#NOW IS IN DLS; EPOCH NOT IN DLS
if checkDLS(now) == True and checkDLS(epoch) == False:
	now = now - datetime.timedelta(hours=1)

#NOW IS IN DLS; EPOCH IS IN DLS
#do nothing

#NOW IS NOT IN DLS; EPOCH NOT IN DLS
# do nothing

#NOW IS NOT IN DLS; EPOCH IS IN DLS
#add hour?

timeElapsed = now - epoch
totalSec = int(timeElapsed.total_seconds())


print("epoch is", str(epoch))
print("current time", str(now))
print("time elapsed", totalSec)#timeElapsed.total_seconds())

#compute md5 of of relevent 60 sec interval <421137780>
#sec of now + 1
#begin hash = elapsed - now.sec + 1

beginInt = totalSec - now.second - 1
print('begin int is', beginInt)

m=hashlib.md5()
#m.update(str(timeElapsed.total_seconds()))
m.update(str(beginInt))
print("first hash", m.hexdigest())


m2=hashlib.md5()
m2.update(m.hexdigest())
print("second hash", m2.hexdigest())

getCode(m2.hexdigest())





'''
datetime library:
https://docs.python.org/2/library/datetime.html

time library:
https://docs.python.org/2/library/time.html

hashlib:
https://docs.python.org/2/library/hashlib.html#module-hashlib
'''
