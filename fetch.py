#!/usr/bin/env python2

from ftplib import FTP
from StringIO import StringIO
import sys

'''
This function takes stdout from ls from a ftp server,
then isolates the 7 right most permissions to turn into binary
that can be turned into 7bit ascii
'''
def sevenbitDecode(listing):
    charInd = 0 #used to move left to right in each line
    permOut = [] #holds the permissions to be turned into binary
    tag1=False
    tag2=False
    tag3=False

    # goes through stdout isolating the permissions
    #if a file has the first 3 bits clear, it will record that
    for char in termOut:

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
    print ''.join(binOut) #print binOut as a string (the final binary number)


'''
FTP SERVER CODE
'''

ftp=FTP('jeangourd.com') #hostname
ftp.login('anonymous','') #log in as anonymous; password is ''

#stores everything sent to stdout
old_stdout=sys.stdout
result=StringIO()
sys.stdout=result


ftp.cwd('7') #CHANGE DIR HERE

#put comands that cause stdout here
ftp.retrlines('LIST')

sys.stdout=old_stdout #redirect stdout to screen

ftp.quit()

'''
MAIN
'''
termOut=result.getvalue()

#print termOut

sevenbitDecode(termOut)

'''
Work Cited
https://docs.python.org/2/library/ftplib.html
https://wrongsideofmemphis.wordpress.com/2010/03/01/store-standard-output-on-a-variable-in-python/
'''
