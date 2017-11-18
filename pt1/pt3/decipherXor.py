#!/usr/bin/python
import sys

message = bytearray.fromhex(sys.argv[1])

def charXor(char, message):
    toRet = message[:]
    for i in range(len(toRet)):
        toRet[i] ^= char
    return toRet

def getCharFreq(message):
    score = 0
    for char in message:
        if(65 <= int(char) <= 90):
            score += 1

        elif(97 <= int(char) <= 122):
            score += 1
    return score


def decryptSingleCharXor(message):
    currentBest =0
    for i in range(1, 256):
        guess = charXor(i, message)
        guessScore = getCharFreq(guess)
        if(guessScore > currentBest):
            current = guess
            currentBest = guessScore
    return current, currentBest

print decryptSingleCharXor(message)[0].decode()
