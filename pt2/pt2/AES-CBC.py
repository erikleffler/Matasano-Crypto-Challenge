#!/bin/bash/python
import sys
import operator
import base64
from Crypto.Cipher import AES

def encryptAES_ECB(data, key):
    cipher = AES.new(key)
    return cipher.encrypt(data)

def XOR(data1, data2):
    for i in range(min(len(data1), len(data2))):
        data1[i] ^= data2[i]
    return data1

def encryptAES_CBC(data, key, iv):
    if(len(iv) != 16):
        print("Initialization vector is not 16 bytes, it's: %i, bytes.") % len(iv)
        return None
    data[:16] = XOR(data[:16], iv)
    encryptedData = pad(data)
    for i in range(1, (len(data))/16-2):
        encryptedData[i*16:(i+1)*16] = bytearray(encryptAES_ECB(bytes(data[i*16:(i+1)*16]),key))
        data[(i + 1)*16:(i + 2)*16] = XOR(data[(i + 1)*16:(i + 2)*16], encryptedData[i*16:(i+1)*16])

    encryptedData[-16:] = bytearray(encryptAES_ECB(bytes(data[-16:]), key))
    return encryptedData

def pad(msg):
    msg += (bytearray("0")*(16-(len(msg)%16)))
    return msg 

with open(sys.argv[1]) as f:
    data = base64.b64decode(f.read().replace('\n', ''))
    print encryptAES_CBC(bytearray(data), "YELLOW SUBMARINE", bytearray(16))
