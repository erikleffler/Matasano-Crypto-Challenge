#!/usr/bin/python
import sys

message = bytearray("Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal")


def encryptXor(key, message):
    toRet = message[:]
    for i in range(len(toRet)):
        toRet[i] ^= key[i % len(key)]
    return toRet

encrypted = encryptXor(bytearray("ICE"), message)
print ''.join(format(x, '02x') for x in encrypted)
