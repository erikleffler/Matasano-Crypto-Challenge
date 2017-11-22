#!/bin/bash/python
import random
import binascii
import sys
import operator
import base64
from Crypto.Cipher import AES

class Server:

    def __init__(self):
        self.user_counter = 10
        self.cipher = AES.new(self.rand_key_gen(16))

    def rand_key_gen(self, size):
        key = bytearray(size)
        for i in range(size):
            key[i] = random.randint(0, 255)
        return bytes(key)

    def pad(self, msg):
        msg += bytearray((16-len(msg))%16)
        return bytes(msg) 

    def kv_parse(self, in_string):
        object_not = "{\n"
        object_array = [obj.split("=") for obj in in_string.split("&")]
        for i in range(len(object_array)):
            object_not += "\t" + object_array[i][0] + " : '" + object_array[i][1] +"',\n"
        return object_not + "}"

    def encrypt(self, data):
        data = self. pad(data)
        return self.cipher.encrypt(data)

    def profile_for(self, email):
        email = email.replace("=", "")
        email = email.replace("&", "")
        return self.encrypt("email=" + email + "&uid=%i&role=user" % self.user_counter)
    
    def parse_profile(self, email):
        print self.cipher.decrypt(email)
        profile = self.kv_parse(self.cipher.decrypt(email))
        return profile

def get_block_and_original_size(encrypt_function):
    prevlength = len(encrypt_function(bytearray()))
    for i in range(1, 2048):
        diff = len(encrypt_function(bytearray(i)))-prevlength
        if(diff > 0):
            return [diff, prevlength - i]
    return -1

def pad(msg, block_size):
    msg += bytearray((block_size-len(msg))%block_size)
    return bytes(msg) 

def construct_prefix(block_size, original_size, clip_size):
    return bytearray(["A"]*(((-original_size)%block_size)+clip_size-1))

def construct_postfix(block_size, pre_size, to_append):
    return bytearray([" "]*(block_size-pre_size-1)) + to_append + bytearray([" "]*(block_size-len(to_append)))

def construct_input(block_size, original_size, clip_size, pre_size, to_append, encrypt_function):
    prefix = encrypt_function(construct_prefix(block_size, original_size, clip_size))[:-block_size]
    postfix = encrypt_function(construct_postfix(block_size, pre_size, to_append))[block_size:2*block_size]
    return prefix + postfix 


def Main():
    s = Server()
    block_size, original_size = get_block_and_original_size(s.profile_for)
    mal_input = construct_input(block_size, original_size, 4, 5, "admin", s.profile_for)
    print len(mal_input)%16
    print s.parse_profile(mal_input)
if __name__ == '__main__':
    Main()
    



