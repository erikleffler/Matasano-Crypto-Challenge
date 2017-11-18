#!/usr/bin/python
import sys
import operator
import base64
import numpy as np

def hammingDist(m1, m2):
    hammingDist = 0
    for i in range(len(m1)):
        hammingDist += bin(m1[i] ^ m2[i]).count("1")
    return hammingDist

def getKeySizeRank(data, lower, upper):
    scoreDict = {}
    for i in range(lower, upper):
        curScore = 0
        for j in range(1, len(data) / i):
            curScore += hammingDist(data[0:i], data[j*i : (j+1)*i])
        scoreDict[i] = curScore * 1.0 / len(data)
    return sorted(scoreDict.items(), key=operator.itemgetter(1))

def transposeByteArray(data, n):
    toRet = data[:]
    for i in range(n):
        for j in range(len(data)/n):
            toRet[i * (len(data) / n) + j] = data[i + j * n]
    return toRet

def decipher(data):
    sizeRank = getKeySizeRank(data, 2, 40)
    for size in sizeRank:
        key = bytearray(size[0])
        tData = transposeByteArray(data, size[0])
        for i in range(size[0]):
            key[i] = decryptSingleCharXor(tData[i*len(data)/size[0] : (i+1)*len(data)/size[0]])
        print encryptXor(key, data).strip()
        print key
        if(raw_input("Is this correct? 1 for yes, 0 for no.\n") == "1"):
            return key
    return bytearray(0)

def encryptXor(key, message):
    toRet = message[:]
    for i in range(len(toRet)):
        toRet[i] ^= key[i % len(key)]
    return toRet

def charXor(char, message):
    toRet = message[:]
    for i in range(len(toRet)):
        toRet[i] ^= char
    return toRet

def getCharFreq(message):
    desiredFreq = np.array([0.0834, 0.0154, 0.0273, 0.0414, 0.126, 0.023, 0.0192, 0.0611, 0.0671, 0.0023, 0.0087, 0.0424, 0.0253, 0.068, 0.077, 0.0166, 0.0009, 0.0568, 0.0611, 0.0937, 0.0285, 0.0106, 0.0234, 0.002, 0.0204, 0.0006])
    guessFreq = np.zeros(26)
    score = 0.0
    for char in message:
        if(65 <= int(char) <= 90):
            score += 1.0
            guessFreq[int(char) - 65] += 1
        elif(97 <= int(char) <= 122):
            score += 1.0
            guessFreq[int(char) - 97] += 1
    return score * 1.0 / np.linalg.norm(desiredFreq - guessFreq * 1.0 / len(message))

def decryptSingleCharXor(message):
    currentBest = 0
    char = 0
    for i in range(1, 256):
        guess = charXor(i, message)
        guessScore = getCharFreq(guess)
        if(guessScore > currentBest):
            char = i
            current = guess
            currentBest = guessScore
    return char

with open(sys.argv[1]) as f:
    data = base64.b64decode(f.read().replace('\n', ''))
    decipher(bytearray(data))
