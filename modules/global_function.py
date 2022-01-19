# converts whole numbers to decimal equivalent (234 becomes .234)
def decimal_converter(num):
    while num > 1:
        num /= 10
    return num

    # function for converting a float number to a 5 byte IEEE-754 packet


#### ~lines0-500 are serial communication functions ###
# Function for converting decimal to binary
def float_bin(number, places=3):
    whole, dec = str(number).split(".")
    print("whole = " + str(whole))
    print("dec = " + str(dec))
    whole = int(whole)
    dec = int(dec)
    if dec == 0:
        dec = 1
    if dec < 10:
        dec += 10
    for z in str(dec):
        if z == 0:
            z = 1
    res = bin(whole).lstrip("0b") + "."
    print("res = " + str(res))
    for x in range(places):
        whole, dec = str((decimal_converter(dec)) * 2).split(".")
        dec = int(dec)
        res += whole

    return res


def IEEE754(n):
    # identifying whether the number
    # is positive or negative
    sign = 0
    if n < 0:
        sign = 1
        n = n * (-1)
    p = 30

    # convert float to binary
    dec = float_bin(n, places=p)

    # separate the decimal part
    # and the whole number part
    whole, dec = str(dec).split(".")
    whole = int(whole)

    # calculating the exponent(E)
    exponent = len(str(whole)) - 1
    exponent_bits = 127 + exponent

    # converting the exponent from
    # decimal to binary
    exponent_bits = bin(exponent_bits).lstrip("0b")

    # finding the mantissa
    mantissa = str(whole)[1:exponent + 1]
    mantissa = mantissa + dec
    mantissa = mantissa[0:23]

    # the IEEE754 notation in binary
    final = str(sign) + str(exponent_bits) + mantissa
    byte1 = "0000" + final[0:4]
    byte2 = "0" + final[4:11]
    byte3 = "0" + final[11:18]
    byte4 = "0" + final[18:25]
    byte5 = "0" + final[25:32]
    databyte1 = bytearray([int(byte1, 2)])
    databyte2 = bytearray([int(byte2, 2)])
    databyte3 = bytearray([int(byte3, 2)])
    databyte4 = bytearray([int(byte4, 2)])
    databyte5 = bytearray([int(byte5, 2)])

    return (databyte1, databyte2, databyte3, databyte4, databyte5)

