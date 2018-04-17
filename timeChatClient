#!/usr/bin/env python2
import socket
import sys
from time import time
from binascii import unhexlify

#ip = "localhost"
#port = 31337

ip = "jeangourd.com"
port = 31337

ZERO = 0.020
ONE = 0.09

#create and connect to socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip,port))

covert_bin = ""
#receive data
data = s.recv(4096)
while(data.rstrip("\n") != "EOF"):
    sys.stdout.write(data)
    sys.stdout.flush()

    t0 = time()
    data = s.recv(4096)
    t1 = time()
    delta = round(t1 - t0, 3)
    if (delta >= ONE):
        covert_bin += "1"
    else:
        covert_bin += "0"

    covert = ""
    i=0
    while (i < len(covert_bin)):
        b = covert_bin[i:i + 8]
        n = int("0b{}".format(b), 2)
        try:
            covert += unhexlify("{0:x}".format(n))
        except TypeError:
            covert += "?"
        i += 8
s.close
print(covert)
