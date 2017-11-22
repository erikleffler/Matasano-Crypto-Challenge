def validate_padding(data):
    if(data[-data[-1]:] != bytearray([data[-1]]*data[-1])):
        raise Exception("Bad PKCS#7 padding.")
    return data[:-data[-1]]

print validate_padding(bytearray("ICE ICE BABY") + bytearray([4]*4))
print validate_padding(bytearray("ICE ICE BABY") + bytearray([6]*4))
