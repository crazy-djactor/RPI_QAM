import numpy as np



import serial
import binascii


def write_serial_int(n):
    databyte0 = "00000000"
    databyte1 = "00000001"
    databyte2 = "00000010"
    if n==0:
        byte1 = bytearray([int(databyte0,2)])
        byte2 = bytearray([int(databyte0,2)])
        byte3 = bytearray([int(databyte0,2)])
    elif n==1:
        byte1 = bytearray([int(databyte0,2)])
        byte2 = bytearray([int(databyte0,2)])
        byte3 = bytearray([int(databyte1,2)])
    elif n==2:
        byte1 = bytearray([int(databyte0,2)])
        byte2 = bytearray([int(databyte0,2)])
        byte3 = bytearray([int(databyte2,2)])
    
    command=bytearray([130])
    operand =bytearray([4])
    data = bytearray()
    echo = bytearray()
    
    sleepy = 0.05
    
    ser = serial.Serial(
    port='/dev/ttyUSB1',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout = 0.1)
    
    ser.write(command) #send command byte
    echo = ser.read(10) #recieve command byte
    #print(echo)
    data = data + echo
    
    
    ser.write(operand)
    echo = ser.read(10)
    #print(echo)
    data = data + echo
    
    ser.write(byte1)
    echo = ser.read(10)
    #print(echo)
    data = data + echo
    
    ser.write(byte2)
    echo = ser.read(10)
    #print(echo)
    data = data + echo
    
    ser.write(byte3)
    return(data)
    ser.close()
    


def read_serial_int(data):
    print(int(data[4]))
    
    




        
def mainloop():
    read_serial_int(write_serial_int(0))
    #print(write_serial_float(command=bytearray([162]),operand =bytearray([27]),valueToWrite=1))
    #print(write_serial_float(command=bytearray([162]),operand =bytearray([28]),valueToWrite=1))
    #print(write_serial_float(command=bytearray([162]),operand =bytearray([29]),valueToWrite=1))


mainloop()
