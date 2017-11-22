#!/bin/bash/python
import random
import binascii
import sys
import operator
import base64
from Crypto.Cipher import AES

class encryption_oracle:

    def __init__(self, secret):
        self.cipher = AES.new(self.rand_key_gen(16))
        self.secret = secret
        self.rand_prefix = self.rand_key_gen(random.randint(0, 100))

    def encrypt(self, data):
        return self.cipher.encrypt(self.pad(self.rand_prefix+data+self.secret))

    def pad(self, msg):
        msg += (bytearray("0")*((-len(msg))%16))
        return bytes(msg)

    def rand_key_gen(self, size):
        key = bytearray(size)
        for i in range(size):
            key[i] = random.randint(0, 255)
        return bytes(key)

def detect_repetition(data):
    for i in range(len(data)-16):
        for j in range(1, (len(data)-1)/16):
            if(data[i:i+16] == data[i+j*16:i+(j+1)*16]):
                return i
    return -1

def detect_block_size(encrypt_function):
    prevlength = len(encrypt_function(bytearray()))
    for i in range(1, 2048):
        diff = len(encrypt_function(bytearray(i)))-prevlength
        if(diff > 0):
            return diff
    return -1

def len_prefix(encryption_function):
    to_insert = bytearray(0)
    while detect_repetition(encryption_function(to_insert)) == -1:
        to_insert.append(" ")
    return to_insert[:-32], detect_repetition(encryption_function(to_insert))

def gen_byte_dict(pre_string, encrypt_function):
    byte_dict = {}
    for i in range(256):
        string = pre_string + bytearray([i])
        byte_dict[clipped_encrypt(encrypt_function, string)[:16]] = i
    return byte_dict

def get_byte(encrypt_function, known_part, block_size, index):
    amount_to_prepend = (block_size-len(known_part)-1)%block_size
    pre_string = bytearray([0]*amount_to_prepend)+known_part
    byte_dict = gen_byte_dict(pre_string[1-block_size:], encrypt_function)
    encrypted_string = clipped_encrypt(encrypt_function, bytearray(amount_to_prepend))
    crafted_string = encrypted_string[len(pre_string)-block_size+1:len(pre_string)+1]
    return byte_dict[crafted_string]

def clipped_encrypt(encrypt_function, data):
    return encrypt_function(to_prepend + data)[to_clip:]

def break_ECB_oracle(encrypt_function):
    message = bytearray([0]*len(clipped_encrypt(encrypt_function, bytearray())))
    size = detect_block_size(encrypt_function)
    if detect_repetition(encrypt_function(bytes(bytearray(size*3)))) == -1:
        print "Not ECB, returning"
        return
    for i in range(len(message)):
        message[i] = get_byte(encrypt_function, message[:i], size, i)
    return message

with open(sys.argv[1]) as f:
    secret = base64.b64decode(f.read().replace('\n', ''))
    e = encryption_oracle(secret)
    to_prepend, to_clip = len_prefix(e.encrypt)
    print break_ECB_oracle(e.encrypt)


