from serial import Serial
import binascii
def get_O2():
    ser = Serial(
        port='/dev/ttyUSB1',\
        baudrate=9600,\
        timeout = 1)

    sleepy = 0.03
    i=0
    fullcommand = bytearray([1,2,1,0,0,3,13])
    ser.write(fullcommand)
    ser.write(b' ')
    #await asyncio.sleep(sleepy)
    #time.sleep(sleepy)
    deldata = ser.read(8)
    data = str(binascii.hexlify(deldata[4:8]))
    #print(str(binascii.hexlify(deldata)))
    c = [data[i:i+2] for i in range (0, len(data), 2)]
    try:
        byte1 = "{:08b}".format(int(c[1], base=16))
        byte2 = "{:08b}".format(int(c[2], base=16))
        byte3 = "{:08b}".format(int(c[3], base=16))
        byte4 = "{:08b}".format(int(c[4], base=16))

        o2_bin = byte1+byte2+byte3+byte4
        #print(o2_bin)
        m = o2_bin[9:]
        mantissa = 0
        mantissa =      (int(m[0])*2**22+int(m[1])*2**21+int(m[2])*2**20+int(m[3])*\
                    2**19+int(m[4])*2**18+int(m[5])*2**17+int(m[6])*2**16+int(m[7])*\
                    2**15+int(m[8])*2**14+int(m[9])*2**13+int(m[10])*2**12+int(m[11])*\
                    2**11+int(m[12])*2**10+int(m[13])*2**9+int(m[14])*2**8+int(m[15])*\
                     2**7+int(m[16])*2**6+int(m[17])*2**5+int(m[18])*2**4+int(m[19])*\
                     2**3+int(m[20])*2**2+int(m[21])*2**1+int(m[22])*2**0)/8388608
                     
        exponent = int(o2_bin[2:9],2)
        sign = (-1)**(int(o2_bin[0],2))
        
        o2_ppm = sign*(2**(exponent-127))*(1+mantissa)
        o2_ppb = 1000*o2_ppm



        ser.close()
        print(o2_ppb)
        #return(str(o2_ppb))
    except Exception as e:
        print("get_O2 error:" + str(e))
        pass
get_O2()