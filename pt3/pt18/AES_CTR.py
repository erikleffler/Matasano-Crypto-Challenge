from Crypto.Cipher import AES
import base64
import binascii
import struct
import random
import sys

class AES_CTR: 

    def __init__(self, key, nonce):
        self.nonce = bytes(nonce)
        self.cipher = AES.new(bytes(key))

    def gen_stream(self, length):
        stream = bytearray()
        for i in range(length):
            count_array = bytearray(struct.pack('L', i))
            count_array = bytearray(((-len(count_array))%16)) + count_array
            stream += (bytearray(self.cipher.encrypt(self.nonce + str(count_array))))
        return stream

    def encrypt(self, data):
        stream = self.gen_stream(len(data)/16+1)
        return self.XOR(bytearray(data), stream)


    def rand_key_gen(self, size):
        key = bytearray(size)
        for i in range(size):
            key[i] = random.randint(0, 255)
        return str(key)

    def XOR(self, data1, data2):
        data = bytearray(min(len(data1), len(data2)))
        for i in range(len(data)):
            data[i] = (data1[i] ^ data2[i])
        return data

if __name__ == '__main__':
    s = AES_CTR("YELLOW SUBMARINE", bytearray(16))
    with open(sys.argv[1]) as f:
        print s.encrypt(base64.b64decode(f.read().replace('\n', '')))
