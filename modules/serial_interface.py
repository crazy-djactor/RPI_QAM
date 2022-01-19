import serial
import binascii
import time

from modules.Util import raw_to_ppb
from modules.global_function import IEEE754

# write a decimal number to the meeco
###operand variables below:
### 0 for raw cell value
### 1 for avg cell value
### 15 for upper band limit
### 16 for lower band limit
### command=bytearray([178]) for sending
### command=bytearray([146]) for receiving

####Check to see which serial port sounds like a meeco and which sounds like a deltaf


class SerialInterface():
    def __init__(self):
        self.comPortOxygen = ""
        self.comPortMoist = ""
        self.deltafConnected = False
        self.meecoConnected = False

    def serial_checker(self):

        # #await asyncio.sleep(0.9)
        time.sleep(0.9)
        try:
            self.comPortOxygen = '/dev/ttyUSB1'
            testComOxygen = self.get_O2()
            self.deltafConnected = True

            if 'e' in testComOxygen:
                time.sleep(0.2)
                try:
                    testComOxygen = self.get_O2()
                    self.deltafConnected = True
                    time.sleep(0.2)
                except:
                    self.deltafConnected = False
                self.comPortOxygen = '/dev/ttyUSB0'
                time.sleep(0.2)
        except:
            self.deltafConnected = False
            print("deltaf not connected")
            pass

        self.comPortMoist = '/dev/ttyUSB0'
        try:
            testComMoisture = raw_to_ppb(self.get_h20())
            self.comPortMoist = '/dev/ttyUSB0'
            self.meecoConnected = True
        except:
            self.comPortMoist = '/dev/ttyUSB1'
            self.meecoConnected = False

        #         print("meeco not connected")
        # #await asyncio.sleep(1)
        time.sleep(1)


    def write_serial_float(self, command, operand, valueToWrite):
        databytes = IEEE754(valueToWrite)

        data = bytearray()
        echo = bytearray()
        # command=bytearray([178])
        # operand =bytearray([15])
        databyte1 = databytes[0]
        databyte2 = databytes[1]
        databyte3 = databytes[2]
        databyte4 = databytes[3]
        databyte5 = databytes[4]

        sleepy = 0.02

        ser = serial.Serial(
            port=self.comPortMoist, \
            baudrate=9600, \
            parity=serial.PARITY_NONE, \
            stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, \
            timeout=1)

        # time.sleep(sleepy)
        data = bytearray()
        ser.write(command)  # send command byte
        # time.sleep(sleepy)
        echo = ser.read(1)  # recieve command byte
        data = data + echo

        ser.write(operand)
        # time.sleep(sleepy)
        echo = ser.read(2)
        data = data + echo

        ser.write(databyte1)
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo

        ser.write(databyte2)
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo

        ser.write(databyte3)
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo

        ser.write(databyte4)
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo

        ser.write(databyte5)
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo
        return (data)
        # time.sleep(sleepy)

        ser.close()


    # uses the write_serial_float function to write values to upper and lower meeco bands
    def write_upperandlower(self, valueToUpper, valueToLower):
        self.write_serial_float(bytearray([178]), bytearray([15]), valueToUpper)
        # time.sleep(0.02)
        self.write_serial_float(bytearray([178]), bytearray([16]), valueToLower)



    # asks meeco for a decimal number
    ###operand variables below:
    ### 0 for raw cell value
    ### 1 for avg cell value
    ### 15 for upper band limit
    ### 16 for lower band limit
    def read_serial_float(self, operand):
        operand = bytearray([operand])

        data = bytearray()
        echo = bytearray()
        command = bytearray([146])
        # operand =bytearray([16])

        sleepy = 0.02

        ser = serial.Serial(
            port=self.comPortMoist, \
            baudrate=9600, \
            parity=serial.PARITY_NONE, \
            stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, \
            timeout=1)

        # time.sleep(sleepy)
        data = bytearray()
        ser.write(command)  # send command byte
        # time.sleep(sleepy)
        echo = ser.read(1)  # recieve command byte
        data = data + echo

        ser.write(operand)
        # time.sleep(sleepy)
        echo = ser.read(2)
        data = data + echo

        ser.write(bytearray([echo[-1]]))
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo

        ser.write(bytearray([echo[-1]]))
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo

        ser.write(bytearray([echo[-1]]))
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo

        ser.write(bytearray([echo[-1]]))
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo
        return (data)
        # time.sleep(sleepy)

        ser.close()



    # writes integers to meeco (current mode is the only thing that currently uses this)
    def write_serial_int(self, send, n):
        databyte0 = "00000000"
        databyte1 = "00000001"
        databyte2 = "00000010"
        if n == 0:
            byte1 = bytearray([int(databyte0, 2)])
            byte2 = bytearray([int(databyte0, 2)])
            byte3 = bytearray([int(databyte0, 2)])
        elif n == 1:
            byte1 = bytearray([int(databyte0, 2)])
            byte2 = bytearray([int(databyte0, 2)])
            byte3 = bytearray([int(databyte1, 2)])
        elif n == 2:
            byte1 = bytearray([int(databyte0, 2)])
            byte2 = bytearray([int(databyte0, 2)])
            byte3 = bytearray([int(databyte2, 2)])
        if send == True:
            command = bytearray([162])
        else:
            command = bytearray([130])
        operand = bytearray([4])
        data = bytearray()
        echo = bytearray()

        sleepy = 0.03

        ser = serial.Serial(
            port=self.comPortMoist, \
            baudrate=9600, \
            parity=serial.PARITY_NONE, \
            stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, \
            timeout=1)

        ser.write(command)  # send command byte
        # time.sleep(sleepy)
        echo = ser.read(1)  # recieve command byte
        data = data + echo

        ser.write(operand)
        # time.sleep(sleepy)
        echo = ser.read(2)
        data = data + echo

        ser.write(byte1)
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo

        ser.write(byte2)
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo

        ser.write(byte3)
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo
        return (int(data[4]))

        ser.close()
        if int(data[4]) == 1:
            currentMode.set('Inert')
        if int(data[4]) == 0:
            currentMode.set('Service')


    # gets O2 data and converts to ppb
    def get_O2(self):
        ser = serial.Serial(
            port=self.comPortOxygen, \
            baudrate=9600, \
            parity=serial.PARITY_NONE, \
            stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, \
            timeout=1)

        sleepy = 0.03
        i = 0
        fullcommand = bytearray([1, 2, 1, 0, 0, 3, 13])
        ser.write(fullcommand)
        ser.write(b' ')
        # await asyncio.sleep(sleepy)
        # time.sleep(sleepy)
        deldata = ser.read(8)
        data = str(binascii.hexlify(deldata[4:8]))
        # print(str(binascii.hexlify(deldata)))
        c = [data[i:i + 2] for i in range(0, len(data), 2)]
        try:
            byte1 = "{:08b}".format(int(c[1], base=16))
            byte2 = "{:08b}".format(int(c[2], base=16))
            byte3 = "{:08b}".format(int(c[3], base=16))
            byte4 = "{:08b}".format(int(c[4], base=16))

            o2_bin = byte1 + byte2 + byte3 + byte4
            # print(o2_bin)
            m = o2_bin[9:]
            mantissa = 0
            mantissa = (int(m[0]) * 2 ** 22 + int(m[1]) * 2 ** 21 + int(m[2]) * 2 ** 20 + int(m[3]) * \
                        2 ** 19 + int(m[4]) * 2 ** 18 + int(m[5]) * 2 ** 17 + int(m[6]) * 2 ** 16 + int(m[7]) * \
                        2 ** 15 + int(m[8]) * 2 ** 14 + int(m[9]) * 2 ** 13 + int(m[10]) * 2 ** 12 + int(m[11]) * \
                        2 ** 11 + int(m[12]) * 2 ** 10 + int(m[13]) * 2 ** 9 + int(m[14]) * 2 ** 8 + int(m[15]) * \
                        2 ** 7 + int(m[16]) * 2 ** 6 + int(m[17]) * 2 ** 5 + int(m[18]) * 2 ** 4 + int(m[19]) * \
                        2 ** 3 + int(m[20]) * 2 ** 2 + int(m[21]) * 2 ** 1 + int(m[22]) * 2 ** 0) / 8388608

            exponent = int(o2_bin[2:9], 2)
            sign = (-1) ** (int(o2_bin[0], 2))

            o2_ppm = sign * (2 ** (exponent - 127)) * (1 + mantissa)
            o2_ppb = 1000 * o2_ppm

            ser.close()
            # print(o2_ppb)
            return (str(o2_ppb))
        except Exception as e:
            print("get_O2 error:" + str(e))
            pass


    ########EXPERIMENTAL: use this copy of get_O2 and replace in animation function to try to figure out how to read over 2PPM
    def get_O2temp(self):
        ser = serial.Serial(
            port=self.comPortOxygen, \
            baudrate=9600, \
            parity=serial.PARITY_NONE, \
            stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, \
            timeout=1)

        sleepy = 0.01
        i = 0
        # fullcommand = bytearray([1,2,1,0,0,3,13])
        # ser.write(fullcommand)
        ser.write(bytearray([1]))
        time.sleep(sleepy)
        ser.write(bytearray([2]))
        time.sleep(sleepy)
        ser.write(bytearray([1]))
        time.sleep(sleepy)
        ser.write(bytearray([0]))
        time.sleep(sleepy)
        ser.write(bytearray([0]))
        time.sleep(sleepy)
        ser.write(bytearray([3]))
        time.sleep(sleepy)
        ser.write(bytearray([13]))
        # ser.write(b' ')
        # await asyncio.sleep(sleepy)
        # time.sleep(sleepy)
        deldata = ser.read(14)
        data = str(binascii.hexlify(deldata[4:8]))
        print(str(binascii.hexlify(deldata)))
        print(str(binascii.hexlify(deldata[4:8])))
        c = [data[i:i + 2] for i in range(0, len(data), 2)]
        try:
            byte1 = "{:08b}".format(int(c[1], base=16))
            byte2 = "{:08b}".format(int(c[2], base=16))
            byte3 = "{:08b}".format(int(c[3], base=16))
            byte4 = "{:08b}".format(int(c[4], base=16))

            o2_bin = byte1 + byte2 + byte3 + byte4
            # print(o2_bin)
            m = o2_bin[9:]
            mantissa = 0
            mantissa = (int(m[0]) * 2 ** 22 + int(m[1]) * 2 ** 21 + int(m[2]) * 2 ** 20 + int(m[3]) * \
                        2 ** 19 + int(m[4]) * 2 ** 18 + int(m[5]) * 2 ** 17 + int(m[6]) * 2 ** 16 + int(m[7]) * \
                        2 ** 15 + int(m[8]) * 2 ** 14 + int(m[9]) * 2 ** 13 + int(m[10]) * 2 ** 12 + int(m[11]) * \
                        2 ** 11 + int(m[12]) * 2 ** 10 + int(m[13]) * 2 ** 9 + int(m[14]) * 2 ** 8 + int(m[15]) * \
                        2 ** 7 + int(m[16]) * 2 ** 6 + int(m[17]) * 2 ** 5 + int(m[18]) * 2 ** 4 + int(m[19]) * \
                        2 ** 3 + int(m[20]) * 2 ** 2 + int(m[21]) * 2 ** 1 + int(m[22]) * 2 ** 0) / 8388608

            exponent = int(o2_bin[1:9], 2)
            sign = (-1) ** (int(o2_bin[0], 2))

            o2_ppm = sign * (2 ** (exponent - 127)) * (1 + mantissa)
            o2_ppb = 1000 * o2_ppm

            ser.close()
            print(o2_ppb)
            return (str(o2_ppb))

        except Exception as e:
            print("get_O2 error:" + str(e))
            pass


    # gets raw h2o data: need to use raw_to_ppb function to convert to ppb
    def get_h20(self):
        data = bytearray()
        echo = bytearray()
        command = bytearray([146])
        operand = bytearray([1])
        sleepy = 0.02

        ser = serial.Serial(
            port=self.comPortMoist, \
            baudrate=9600, \
            parity=serial.PARITY_NONE, \
            stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, \
            timeout=1)

        # time.sleep(sleepy)
        data = bytearray()
        ser.write(command)  # send command byte
        # await asyncio.sleep(sleepy)
        # time.sleep(sleepy)
        echo = ser.read(1)  # recieve command byte
        data = data + echo

        ser.write(operand)
        # await asyncio.sleep(sleepy)
        # time.sleep(sleepy)
        echo = ser.read(2)
        data = data + echo

        ser.write(bytearray([echo[-1]]))
        # await asyncio.sleep(sleepy)
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo

        ser.write(bytearray([echo[-1]]))
        # await asyncio.sleep(sleepy)
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo

        ser.write(bytearray([echo[-1]]))
        # await asyncio.sleep(sleepy)
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo

        ser.write(bytearray([echo[-1]]))
        # await asyncio.sleep(sleepy)
        # time.sleep(sleepy)
        echo = ser.read(1)
        data = data + echo
        return (data)
        # await asyncio.sleep(sleepy)
        # time.sleep(sleepy)
        ser.close()
