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


def pad(msg):
    msg += (bytearray("0")*((16-len(msg))%16))
    return bytes(msg) 

def rand_key_gen(size):
    key = bytearray(size)
    for i in range(size):
        key[i] = random.randint(0, 255)
    return bytes(key)

def detect_repetition(data):
    for i in range(len(data)-16):
        for j in range(1, (len(data)-1)/16):
            if(data[i:i+16] == data[i+j*16:i+(j+1)*16]):
                return True

def detect_block_size(encrypt_function):
    prevlength = len(encrypt_function(bytearray()))
    for i in range(1, 2048):
        diff = len(encrypt_function(bytearray(i)))-prevlength
        if(diff > 0):
            return diff
    return -1

def encrypt(data):
    data = pad(data+suffix)
    return encrypt_AES_ECB(data, rand_key)

def gen_byte_dict(pre_string, encrypt_function):
    byte_dict = {}
    for i in range(256):
        string = pre_string + bytearray([i])
        byte_dict[encrypt_function(string)[:16]] = i
    return byte_dict

def get_byte(encrypt_function, known_part, block_size, index):
    amount_to_prepend = (block_size-len(known_part)-1)%block_size
    pre_string = bytearray([0]*amount_to_prepend)+known_part
    byte_dict = gen_byte_dict(pre_string[1-block_size:], encrypt_function)
    encrypted_string = encrypt(bytearray(amount_to_prepend))
    crafted_string = encrypted_string[len(pre_string)-block_size+1:len(pre_string)+1]
    return byte_dict[crafted_string]

def break_ECB_oracle(encrypt_function):
    message = bytearray([0]*len(encrypt_function(bytearray())))
    size = detect_block_size(encrypt_function)
    if not detect_repetition(encrypt_function(bytes(bytearray(size*3)))):
        print "Not ECB, returning"
        return
    for i in range(len(message)):
        message[i] = get_byte(encrypt_function, message[:i], size, i)
    return message

with open(sys.argv[1]) as f:
    rand_key = rand_key_gen(16)
    suffix = base64.b64decode(f.read().replace('\n', ''))
    print break_ECB_oracle(encrypt)


