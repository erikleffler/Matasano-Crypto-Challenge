#!/usr/bin/python
import sys
import operator
import base64
from Crypto.Cipher import AES

with open(sys.argv[1]) as f:
    encryptedData = base64.b64decode(f.read().replace('\n', ''))
    cipher = AES.new("YELLOW SUBMARINE")
    msg = cipher.decrypt(encryptedData)
    print msg
