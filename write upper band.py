import serial
import binascii

# Function for converting decimal to binary 
def float_bin(number, places = 3): 
    whole, dec = str(number).split(".")  
    whole = int(whole)  
    dec = int (dec) 
    res = bin(whole).lstrip("0b") + "."
  
    for x in range(places):  
        whole, dec = str((decimal_converter(dec)) * 2).split(".")  
        dec = int(dec)  
        res += whole    
    return res  
  
def decimal_converter(num):   
    while num > 1:  
        num /= 10
    return num  
  
def IEEE754(n) : 
  
    # identifying whether the number 
    # is positive or negative 
    sign = 0
    if n < 0 : 
        sign = 1
        n = n * (-1) 
    p = 30
  
    # convert float to binary 
    dec = float_bin (n, places = p)
  
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
    byte1 = "0000"+final[0:4]
    byte2 = "0"+final[4:11]
    byte3 = "0"+final[11:18]
    byte4 = "0"+final[18:25]
    byte5 = "0"+final[25:32]
    databyte1 = bytearray([int(byte1,2)])
    databyte2 = bytearray([int(byte2,2)])
    databyte3 = bytearray([int(byte3,2)])
    databyte4 = bytearray([int(byte4,2)])
    databyte5 = bytearray([int(byte5,2)])

    return (databyte1,databyte2,databyte3,databyte4,databyte5)

def write_serial_float(command,operand,valueToWrite):
    databytes = IEEE754(valueToWrite)
    
    data = bytearray()
    echo = bytearray()
    #command=bytearray([178])
    #operand =bytearray([15])
    databyte1 = databytes[0]
    databyte2 = databytes[1]
    databyte3 = databytes[2]
    databyte4 = databytes[3]
    databyte5 = databytes[4]
    
    sleepy = 0.05
    
    ser = serial.Serial(
    port='/dev/ttyUSB1',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout = 0.1)
    
    data = bytearray()
    ser.write(command) #send command byte
    echo = ser.read(10) #recieve command byte
    data = data + echo
    
    
    ser.write(operand)
    echo = ser.read(10)
    data = data + echo
    
    ser.write(databyte1)
    echo = ser.read(10)
    data = data + echo
    
    ser.write(databyte2)
    echo = ser.read(10)
    data = data + echo
    
    ser.write(databyte3)
    echo = ser.read(10)
    data = data + echo
    
    
    ser.write(databyte4)
    echo = ser.read(10)
    data = data + echo
    
    ser.write(databyte5)
    echo = ser.read(10)
    data = data + echo
    return(data)

    ser.close()

# converts raw h2o data to ppb
def raw_to_ppb (data):
    raw_hex = str(binascii.hexlify(data[2:]))                                                       # converts raw bin data to hex (leaving off the first two command bytes)
    

    c = [raw_hex[i:i+2] for i in range (0, len(raw_hex), 2)]                                        # splits up the hex data into a list (b' is the first on the list so it is skipped
    
    
    
    try:                                                                                            
        byte1 = "{:08b}".format(int(c[1], base=16))
        byte2 = "{:08b}".format(int(c[2], base=16))
        byte3 = "{:08b}".format(int(c[3], base=16))
        byte4 = "{:08b}".format(int(c[4], base=16))
        byte5 = "{:08b}".format(int(c[5], base=16))
    
        h20_bin = byte1+byte2+byte3+byte4+byte5                                                     # converts hex data list into one string of binary
    
        m1 = h20_bin[14:16]
        m2 = h20_bin[17:24]
        m3 = h20_bin[25:32]
        m4 = h20_bin[33:40]
        m = m1+m2+m3+m4                                                                             # breaks apart the binary string into mantissa portions
            
        mantissa =      (int(m[0])*2**22+int(m[1])*2**21+int(m[2])*2**20+int(m[3])*\
                    2**19+int(m[4])*2**18+int(m[5])*2**17+int(m[6])*2**16+int(m[7])*\
                    2**15+int(m[8])*2**14+int(m[9])*2**13+int(m[10])*2**12+int(m[11])*\
                    2**11+int(m[12])*2**10+int(m[13])*2**9+int(m[14])*2**8+int(m[15])*\
                     2**7+int(m[16])*2**6+int(m[17])*2**5+int(m[18])*2**4+int(m[19])*\
                     2**3+int(m[20])*2**2+int(m[21])*2**1+int(m[22])*2**0)/8388608                  # mantissa calculation according to IEEE754 32 bit float calculation
        
        e1 = h20_bin[5:8]
        e2 = h20_bin[9:14]
        e = e1+e2
        exponent = int(e,2)
        sign = (-1)**(int(h20_bin[4],2))                                                            # exponent calculation according to IEEE754 32 bit float calculation
        
        h20_ppb = sign*(2**(exponent-127))*(1+mantissa)
    
        return(str(h20_ppb))
    except:
        pass

#def value_to_command(n):
    




        
def mainloop():
    print(raw_to_ppb(write_serial_float(command=bytearray([178]),operand =bytearray([15]),valueToWrite=22.18)))
    print(raw_to_ppb(write_serial_float(command=bytearray([178]),operand =bytearray([16]),valueToWrite=18.24)))


mainloop()
