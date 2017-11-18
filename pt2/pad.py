#!/usr/bin/python

def pad(msg, length):
    msg += (bytearray("S")*(length - (len(msg)%length)))
    return msg 

print(pad(bytearray("YELLOW SUBMARINE"), 20))
