#!/usr/bin/python
import sys
import operator
import base64
from Crypto.Cipher import AES

def detectRepetition(data):
    for i in range((len(data)-1)/16):
        for j in range(i + 1, (len(data)-1)/16):
            if(data[i*16:(i+1)*16] == data[j*16:(j+1)*16]):
                return True

with open(sys.argv[1]) as f:
    while(True):
        encryptedData = f.readline()
        if not encryptedData:
            break
        if detectRepetition(bytearray.fromhex(encryptedData.rstrip())):
            print encryptedData.rstrip()
            print '\n\n'
