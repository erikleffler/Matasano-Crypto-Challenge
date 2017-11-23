import random
import binascii
import sys
import base64
from Crypto.Cipher import AES

class PaddingError(Exception):
    def __init__(self, str):
        self.str = str

    def __str__(self):
        return self.str

class padding_oracle:

    def __init__(self):
        self.iv = bytearray(self.rand_key_gen(16))
        self.cipher = AES.new(self.rand_key_gen(16),)

    def gen_cipher_text(self):
        strings = [
            "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
            "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
            "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
            "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
            "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
            "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
            "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
            "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
            "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
            "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
        ]
        return self.encrypt(self.pad(bytearray(base64.b64decode(strings[random.randint(0, len(strings)-1)]))))

    def pad(self, msg):
        to_append = (-len(msg)) % 16
        if to_append == 0:
            to_append = 16
        msg += bytearray([to_append]*(to_append))
        return msg

    def rand_key_gen(self, size):
        key = bytearray(size)
        for i in range(size):
            key[i] = random.randint(0, 255)
        return str(key)

    def validate_padding(self, data):
        data = bytearray(data[:])
        if (bytearray(data[-data[-1]:]) != bytearray([data[-1]]*data[-1])):
            raise PaddingError("BAD PADDING")
        return data[:-data[-1]]

    def XOR(self, data1, data2):
        data = []
        for i in range(min(len(data1), len(data2))):
            data.append(data1[i] ^ data2[i])
        return data

    def decrypt(self, data):
        if(len(self.iv) != 16):
            print("Initialization vector is not 16 bytes, it's: %i, bytes.") % len(self.iv)
            return None
        decrypted_data = data[:]
        decrypted_data[:16] = self.XOR(bytearray(self.cipher.decrypt(bytes(decrypted_data[:16]))), self.iv)
        for i in range(1, len(data)/16):
            decrypted_data[i*16:(i+1)*16] = bytearray(self.cipher.decrypt(bytes(decrypted_data[i*16:(i+1)*16])))
            decrypted_data[i*16:(i+1)*16] = self.XOR(decrypted_data[i*16:(i+1)*16], data[(i-1)*16:i*16])
        return self.validate_padding(decrypted_data)

    def encrypt(self, data):
        if(len(self.iv) != 16):
            print("Initialization vector is not 16 bytes, it's: %i, bytes.") % len(self.iv)
            return None
        data[:16] = self.XOR(data[:16], self.iv)
        encrypted_data = data[:]
        for i in range(0, (len(data)/16)-1):
            encrypted_data[i*16:(i+1)*16] = bytearray(self.cipher.encrypt(bytes(data[i*16:(i+1)*16])))
            data[(i + 1)*16:(i + 2)*16] = self.XOR(data[(i + 1)*16:(i + 2)*16], encrypted_data[i*16:(i+1)*16])

        encrypted_data[-16:] = bytearray(self.cipher.encrypt(bytes(data[-16:])))
        return encrypted_data

def XOR(data1, data2):
    data = data1[:]
    for i in range(min(len(data1), len(data2))):
        data[i] = (data1[i] ^ data2[i])
    return data

def get_block(cipher_block, valid_func):
    to_prepend = bytearray([255]*len(cipher_block))
    for i in range(1, len(cipher_block) + 1):
        for j in range(1, 256):
            to_prepend[-i] = j
            try:
                valid_func(to_prepend[:]+cipher_block[:])
                if(i < len(cipher_block) - 1):
                    assure_correct_byte = to_prepend[:]
                    assure_correct_byte[-i-1] ^= 255
                    valid_func(assure_correct_byte[:]+cipher_block[:])
                to_prepend = bytearray(reversed(XOR(bytearray(reversed(to_prepend)), bytearray([(i+1)^i]*i))))
                break
            except PaddingError:
                continue
    return XOR(to_prepend, bytearray([17]*16))

def main():
    p = padding_oracle()
    cipher_text = bytearray(p.gen_cipher_text())
    decrypted_text = bytearray(len(cipher_text))
    prev_block = p.iv
    for i in range(len(cipher_text)/16):
        decrypted_text[i*16:(i+1)*16] = get_block(cipher_text[i*16:(i+1)*16], p.decrypt)
        decrypted_text[i*16:(i+1)*16] = XOR(decrypted_text[i*16:(i+1)*16], prev_block[:])
        prev_block = cipher_text[i*16:(i+1)*16]

    print p.decrypt(cipher_text)
    print decrypted_text

if __name__ == '__main__':
    main()


