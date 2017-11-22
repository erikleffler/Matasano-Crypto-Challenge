#!/bin/bash/python
import random
import binascii
import sys
import operator
import base64
from Crypto.Cipher import AES

class cbc_oracle:

    def __init__(self):
        self.iv = bytearray(self.rand_key_gen(16))
        self.cipher = AES.new(self.rand_key_gen(16),)

    def parse_data(self, data):
        data = str(data[:]).replace(";", "';'").replace("=", "'='")
        data += ";comment2=%20like%20a%20pound%20of%20bacon"
        data = "comment1=cooking%20MCs;userdata=" + data
        return self.encrypt(self.pad(data))

    def check_encrypted(self, data):
        data = self.decrypt(data[:])
        print data
        return ";admin=true;" in data #self.strip_padding(data)

    def strip_padding(self, data):
        if(data[-data[-1]:] != bytearray([data[-1]]*data[-1])):
            raise Exception("Bad PKCS#7 padding.")
        return data[:-data[-1]]

    def rand_key_gen(self, size):
        key = bytearray(size)
        for i in range(size):
            key[i] = random.randint(0, 255)
        return bytes(key)

    def pad(self, msg):
        msg = msg[:]
        msg += bytearray((16-len(msg))%16)
        return bytes(msg)


    def XOR(self, data1, data2):
        data = []
        for i in range(min(len(data1), len(data2))):
            data.append(data1[i] ^ data2[i])
        return data

    def decrypt(self, data):
        if(len(self.iv) != 16):
            print("Initialization vector is not 16 bytes, it's: %i, bytes.") % len(self.iv)
            return None
        decryptedData = self.pad(data[:])
        decryptedData[:16] = self.XOR(bytearray(self.cipher.decrypt(bytes(decryptedData[:16]))), self.iv)
        for i in range(1, len(data)/16):
            decryptedData[i*16:(i+1)*16] = bytearray(self.cipher.decrypt(bytes(decryptedData[i*16:(i+1)*16])))
            decryptedData[i*16:(i+1)*16] = self.XOR(decryptedData[i*16:(i+1)*16], data[(i-1)*16:i*16])
        return decryptedData

    def encrypt(self, data):
        if(len(self.iv) != 16):
            print("Initialization vector is not 16 bytes, it's: %i, bytes.") % len(self.iv)
            return None
        data[:16] = self.XOR(data[:16], self.iv)
        encryptedData = self.pad(data)
        for i in range(0, (len(data)/16)-1):
            encryptedData[i*16:(i+1)*16] = bytearray(self.cipher.encrypt(bytes(data[i*16:(i+1)*16])))
            data[(i + 1)*16:(i + 2)*16] = self.XOR(data[(i + 1)*16:(i + 2)*16], encryptedData[i*16:(i+1)*16])

        encryptedData[-16:] = bytearray(self.cipher.encrypt(bytes(data[-16:])))
        return encryptedData

    def pad(self, msg):
        msg += (bytearray([(-len(msg)%16)])*((-len(msg))%16))
        return msg 

def XOR(data1, data2):
    data = data1[:]
    for i in range(min(len(data1), len(data2))):
        data[i] = (data1[i] ^ data2[i])
    return data

def gen_mal_cipher(enc_func):
    return XOR(bytearray(enc_func(bytearray(32))), bytearray(16) + bytearray(";admin=true;"))

def Main():
    e = cbc_oracle()
    print e.check_encrypted(gen_mal_cipher(e.parse_data))

if __name__ == '__main__':
    Main()
