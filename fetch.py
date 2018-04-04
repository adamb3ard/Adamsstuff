#!/usr/bin/env python2

from ftplib import FTP
from StringIO import StringIO
import sys
import binascii

'''
Recycled binary code
'''
def specChar(n,arr): #if ascii value is not basic text
	if n == 8: #BACKSPACE
		arr = arr[:-1]
	return arr

#Takes binary, and converts to 8 bit ascii
def cypherEight(ciphText):
	start = 0
	end = start + 8
	plain = []
	while start <= len(ciphText)-8:
		n = int(ciphText[start:end],2)
		try:
			plain.append(binascii.unhexlify('%x' % n))
		except:
			plain = specChar(n,plain)
		start=end
		end=start+8
	plainStr = ''.join(plain)
	print(plainStr)

#Takes binary and converts to 7 bit ascii
def cypherSeven(ciphText):
	start = 0
	end = start + 7
	plain = []
	while start <= len(ciphText)-7:
		n = int(ciphText[start:end],2)
		try:
			plain.append(binascii.unhexlify('%x' % n))
		except:
			plain = specChar(n,plain)
		start=end
		end=start+7
	print(''.join(plain))


'''
This function takes stdout from ls from a ftp server,
then isolates the 7 right most permissions to turn into binary
that can be turned into 7bit ascii
'''
def sevenPermDecode(listing):
    charInd = 0 #used to move left to right in each line
    permOut = [] #holds the permissions to be turned into binary
    binOut = [] #holds binary output
    tag1=False
    tag2=False
    tag3=False

    # goes through stdout isolating the permissions
    #if a file has the first 3 bits clear, it will record that
    for char in listing:

        if charInd == 0 and char == '-': tag1 = True
        if charInd == 1 and char == '-': tag2 = True
        if charInd == 2 and char == '-': tag3 = True

        if charInd > 2 and charInd < 10 and tag1 == True and tag2 == True and tag3 == True:
            permOut.append(char)

        if char == '\n': # tests for a new line, which means next file
            #permOut.append('|') #use to break up lines for test aesthetic
            #reset values for next line
            tag1=False
            tag2=False
            tag3=False
            charInd = 0
        else:
            charInd += 1


    #print ''.join(permOut) #print permOut as a string (7 right most permissions)

    #goes through saved permissions and turns into binary
    for perm in permOut:
        if perm == '-':
            binOut.append('0')
        else:
            binOut.append('1')

    #prints binary can be put into file to be decoded from binary
    #print ''.join(binOut) #print binOut as a string (the final binary number)

    cypherSeven(''.join(binOut)) #print 7bit ascii

'''
This function takes stdout from ls from a ftp server,
then isolates the permissions to turn into binary
that can be turned into 7bit ascii
'''
def tenPermDecode(listing):
    charInd = 0
    permOut = []
    binOut = []

    # goes through stdout isolating the permissions
    for char in listing:
        if charInd < 10:
            permOut.append(char)
        if char == '\n':
            charInd = 0
        else:
            charInd += 1

    #print ''.join(permOut) #print permOut as a string (all 10 perm)

    #goes through saved permissions and turns into binary
    for perm in permOut:
        if perm == '-':
            binOut.append('0')
        else:
            binOut.append('1')

    #remove extra bits
    while len(binOut) % 7 != 0:
        binOut.pop()

    #print ''.join(binOut) #print binOut as a string (final binary number)

    cypherSeven(''.join(binOut)) #print 7bit ascii

'''
FTP SERVER CODE
'''

#ftp=FTP('jeangourd.com') #hostname
#ftp=FTP('localhost') #test host
#ftp.login('anonymous','') #log in as anonymous; password is ''

'''
Specify port for FTP
'''
HOST = "jeangourd.com"
PORT = 21
ftp = FTP()
ftp.connect(HOST, PORT)
ftp.login('anonymous','') #log in as anonymous; password is ''




#stores everything sent to stdout
old_stdout=sys.stdout
result=StringIO()
sys.stdout=result


ftp.cwd('new') #CHANGE DIR HERE

#put comands that cause stdout here
ftp.retrlines('LIST')

sys.stdout=old_stdout #redirect stdout to screen

ftp.quit()

'''
MAIN
'''
termOut=result.getvalue()

#print termOut #print stdout

print("seven running...")
try:
    sevenPermDecode(termOut)
except:
    print("Seven failed")

print("ten running...")
try:
    tenPermDecode(termOut)
except:
    print("ten failed")
