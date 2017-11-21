#!/bin/bash/python
import random
import binascii
import sys
import operator
import base64
from Crypto.Cipher import AES

def decrypt_AES_ECB(data, key):
    cipher = AES.new(key)
    return cipher.decrypt(data)

def encrypt_AES_ECB(data, key):
    cipher = AES.new(key)
    return cipher.encrypt(data)

def XOR(data1, data2):
    for i in range(min(len(data1), len(data2))):
        data1[i] ^= data2[i]
    return data1

def decrypt_AES_CBC(data, key, iv):
    if(len(iv) != 16):
        print("Initialization vector is not 16 bytes, it's: %i, bytes.") % len(iv)
        return None
    decrypted_data = pad(data[:])
    decrypted_data[:16] = XOR(bytearray(decrypt_AES_ECB(bytes(decrypted_data[:16]), key)), iv)
    for i in range(1, len(data)/16):
        decrypted_data[i*16:(i+1)*16] = bytearray(decrypt_AES_ECB(bytes(decrypted_data[i*16:(i+1)*16]),key))
        decrypted_data[i*16:(i+1)*16] = XOR(decrypted_data[i*16:(i+1)*16], data[(i-1)*16:i*16])
    return decrypted_data

def encrypt_AES_CBC(data, key, iv):
    if(len(iv) != 16):
        print("Initialization vector is not 16 bytes, it's: %i, bytes.") % len(iv)
        return None
    data[:16] = XOR(data[:16], iv)
    encrypted_data = pad(data[:])
    for i in range(0, (len(data)/16)-1):
        encrypted_data[i*16:(i+1)*16] = bytearray(encrypt_AES_ECB(bytes(data[i*16:(i+1)*16]),key))
        data[(i + 1)*16:(i + 2)*16] = XOR(data[(i + 1)*16:(i + 2)*16], encrypted_data[i*16:(i+1)*16])

    encrypted_data[-16:] = bytearray(encrypt_AES_ECB(bytes(data[-16:]), key))
    return encrypted_data

def pad(msg):
    msg += (bytearray("0")*((16-len(msg))%16))
    return msg 

def rand_pad(data):
    bytes_to_add = 16-(len(data)%16)
    if(bytes_to_add < 10):
        bytes_to_add += 16
    bytes_to_prepend = random.randint(5, bytes_to_add - 5)
    bytes_to_append = bytes_to_add - bytes_to_prepend
    data += bytearray([0]*bytes_to_append)
    data = bytearray([0]*bytes_to_prepend) + data
    return data

def rand_mode_encrypt(data):
    data = bytes(rand_pad(data))
    key = bytearray(16)
    for i in range(16):
        key[i] = random.randint(0, 255)
    if(random.randint(0, 1) == 1):
        print "Actual: ECB"
        encrypted_data = encrypt_AES_ECB(data, bytes(key))  
    else:
        print "Actual: CBC"
        iv = bytearray(16)
        for i in range(16):
            iv[i] = random.randint(0, 255)
        encrypted_data = encrypt_AES_CBC(bytearray(data), bytes(key), iv)
    return encrypted_data

def detect_repetition(data):
    print "Length of data: %i." % len(data)
    for i in range(len(data)-16):
        for j in range(1, (len(data)-1)/16):
            if(data[i:i+16] == data[i+j*16:i+(j+1)*16]):
                return True


with open(sys.argv[1]) as f:
    data = f.read().replace('\n', '')
    if(detect_repetition(rand_mode_encrypt(data))):
        print "Guess: ECB"
    else:
        print "Guess: CBC"
