#!/usr/bin/python
import sys

arg1 = bytearray.fromhex(sys.argv[1])
arg2 = bytearray.fromhex(sys.argv[2])

for i in range(len(arg1)):
    arg1[i] ^= arg2[i]

print "".join(format(x, '02x') for x in arg1)
