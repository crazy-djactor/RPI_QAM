import binascii
import random
import time
import serial
from datetime import datetime, timedelta

from modules.Util import raw_to_ppb, IEEE754


class SerialInterface:
    comPortOxygen = ""
    deltafConnected = False
    meecoConnected = False
    comPortMoist = ""
    demoMode = True
    last_getO2time = None
    last_getH2Otime = None
    try_failedO2 = 0
    try_failedH2O = 0

    def __init__(self):
        pass

    @classmethod
    def serial_checker(cls):
        # #await asyncio.sleep(0.9)
        time.sleep(0.9)
        try:
            cls.comPortOxygen = '/dev/ttyUSB1'
            testComOxygen = cls.get_O2()
            cls.deltafConnected = True

            if 'e' in testComOxygen:
                time.sleep(0.2)
                try:
                    testComOxygen = cls.get_O2()
                    cls.deltafConnected = True
                    # print("deltaf connected")
                    # await asyncio.sleep(0.2)
                    time.sleep(0.2)
                except:
                    cls.deltafConnected = False
                cls.comPortOxygen = '/dev/ttyUSB0'
                # await asyncio.sleep(0.2)
                time.sleep(0.2)
        except:
            cls.deltafConnected = False
            print("deltaf not connected")
            pass

        cls.comPortMoist = '/dev/ttyUSB0'
        try:
            cls.testComMoisture = raw_to_ppb(cls.get_h20())
            cls.comPortMoist = '/dev/ttyUSB0'
            cls.meecoConnected = True
        except:
            cls.comPortMoist = '/dev/ttyUSB1'
            cls.meecoConnected = False

        #         print("meeco not connected")
        # #await asyncio.sleep(1)
        time.sleep(1)

    # gets raw h2o data: need to use raw_to_ppb function to convert to ppb
    @classmethod
    def get_h20(cls):
        data = bytearray()
        echo = bytearray()
        command = bytearray([146])
        operand = bytearray([1])
        sleepy = 0.02
        try:
            ser = serial.Serial(
                port=cls.comPortMoist, \
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
            ser.close()
            SerialInterface.demoMode = False
            SerialInterface.meecoConnected = True
            return data
        except Exception as e:
            SerialInterface.meecoConnected = True if SerialInterface.demoMode else False
            print("get_h2O error:" + str(e))
            return 'err'
        # await asyncio.sleep(sleepy)
        # time.sleep(sleepy)


    @classmethod
    def get_O2(cls):
        try:
            ser = serial.Serial(
                port=cls.comPortOxygen, \
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
            SerialInterface.demoMode = False
            SerialInterface.deltafConnected = True
            return str(o2_ppb)
        except Exception as e:
            SerialInterface.deltafConnected = True if SerialInterface.demoMode else False
            print("get_O2 error:" + str(e))
            return 'err'

    @classmethod
    def get_valid_o2(cls, try_count):
        # return 'N/A' or valid float value
        attempts = 0
        while attempts < try_count:
            str_o2 = cls.get_O2()  #### comment out for random data###
            if SerialInterface.demoMode:
                cls.last_getO2time = datetime.now()
                cls.try_failedO2 = 0
                return round(float(random.random() * 10), 1)
            if str_o2 == 'err':
                # not demo mode and error string
                attempts += 1
                continue
            else:
                cls.last_getO2time = datetime.now()
                cls.try_failedO2 = 0
                return round(float(str_o2), 1)
        ##############
        cls.try_failedO2 = cls.try_failedO2 + 1
        print('attempt FAILED for O2')
        return 'N/A'

    @classmethod
    def get_valid_h2o(cls, try_count):
        # return 'N/A' or valid float value
        attempts = 0
        while attempts < try_count:
            str_h2o = cls.get_h20()  #### comment out for random data###
            if SerialInterface.demoMode:
                cls.last_getH2Otime = datetime.now()
                cls.try_failedH2O = 0
                return round(float(random.random() * 10), 1)
            if str_h2o == 'err':
                # not demo mode and error string
                attempts += 1
                continue
            else:
                try:
                    h2o = raw_to_ppb(str_h2o)
                    cls.last_getH2Otime = datetime.now()
                    cls.try_failedH2O = 0
                    return round(float(h2o), 1)
                except:
                    attempts += 1

        ##############
        print('attempt FAILED for h2o')
        cls.try_failedH2O = cls.try_failedH2O + 1
        return 'N/A'

    @classmethod
    # asks meeco for a decimal number
    ###operand variables below:
    ### 0 for raw cell value
    ### 1 for avg cell value
    ### 15 for upper band limit
    ### 16 for lower band limit
    def read_serial_float(cls, operand):
        operand = bytearray([operand])

        data = bytearray()
        echo = bytearray()
        command = bytearray([146])
        # operand =bytearray([16])

        sleepy = 0.02

        ser = serial.Serial(
            port=cls.comPortMoist, \
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
        ser.close()
        return (data)
        # time.sleep(sleepy)


    # write a decimal number to the meeco
    ###operand variables below:
    ### 0 for raw cell value
    ### 1 for avg cell value
    ### 15 for upper band limit
    ### 16 for lower band limit
    ### command=bytearray([178]) for sending
    ### command=bytearray([146]) for receiving
    @classmethod
    def write_serial_float(cls, command, operand, valueToWrite):
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
            port=cls.comPortMoist, \
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
        ser.close()       #  ?????????
        return (data)
        # time.sleep(sleepy)

    # writes integers to meeco (current mode is the only thing that currently uses this)
    @classmethod
    def write_serial_int(cls, send, n):
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
            port=cls.comPortMoist, \
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
        ser.close()  #  ?????????
        return int(data[4])

    # uses the write_serial_float function to write values to upper and lower meeco bands
    @classmethod
    def write_upperandlower(cls, valueToUpper, valueToLower):
        cls.write_serial_float(bytearray([178]), bytearray([15]), valueToUpper)
        # time.sleep(0.02)
        cls.write_serial_float(bytearray([178]), bytearray([16]), valueToLower)

    @classmethod
    def read_equip_raw_cell(cls):
        return round(float(raw_to_ppb(SerialInterface.read_serial_float(0))), 1)

    @classmethod
    def read_equip_upper_cell(cls):
        return round(float(raw_to_ppb(SerialInterface.read_serial_float(15))), 1)

    @classmethod
    def read_equip_lower_cell(cls):
        return round(float(raw_to_ppb(SerialInterface.read_serial_float(16))), 1)

# ########EXPERIMENTAL: use this copy of get_O2 and replace in animation function to try to figure out how to read over 2PPM
# def get_O2temp(comPortOxygen):
#     ser = serial.Serial(
#         port=comPortOxygen, \
#         baudrate=9600, \
#         parity=serial.PARITY_NONE, \
#         stopbits=serial.STOPBITS_ONE, \
#         bytesize=serial.EIGHTBITS, \
#         timeout=1)
#
#     sleepy = 0.01
#     i = 0
#     # fullcommand = bytearray([1,2,1,0,0,3,13])
#     # ser.write(fullcommand)
#     ser.write(bytearray([1]))
#     time.sleep(sleepy)
#     ser.write(bytearray([2]))
#     time.sleep(sleepy)
#     ser.write(bytearray([1]))
#     time.sleep(sleepy)
#     ser.write(bytearray([0]))
#     time.sleep(sleepy)
#     ser.write(bytearray([0]))
#     time.sleep(sleepy)
#     ser.write(bytearray([3]))
#     time.sleep(sleepy)
#     ser.write(bytearray([13]))
#     # ser.write(b' ')
#     # await asyncio.sleep(sleepy)
#     # time.sleep(sleepy)
#     deldata = ser.read(14)
#     data = str(binascii.hexlify(deldata[4:8]))
#     print(str(binascii.hexlify(deldata)))
#     print(str(binascii.hexlify(deldata[4:8])))
#     c = [data[i:i + 2] for i in range(0, len(data), 2)]
#     try:
#         byte1 = "{:08b}".format(int(c[1], base=16))
#         byte2 = "{:08b}".format(int(c[2], base=16))
#         byte3 = "{:08b}".format(int(c[3], base=16))
#         byte4 = "{:08b}".format(int(c[4], base=16))
#
#         o2_bin = byte1 + byte2 + byte3 + byte4
#         # print(o2_bin)
#         m = o2_bin[9:]
#         mantissa = 0
#         mantissa = (int(m[0]) * 2 ** 22 + int(m[1]) * 2 ** 21 + int(m[2]) * 2 ** 20 + int(m[3]) * \
#                     2 ** 19 + int(m[4]) * 2 ** 18 + int(m[5]) * 2 ** 17 + int(m[6]) * 2 ** 16 + int(m[7]) * \
#                     2 ** 15 + int(m[8]) * 2 ** 14 + int(m[9]) * 2 ** 13 + int(m[10]) * 2 ** 12 + int(m[11]) * \
#                     2 ** 11 + int(m[12]) * 2 ** 10 + int(m[13]) * 2 ** 9 + int(m[14]) * 2 ** 8 + int(m[15]) * \
#                     2 ** 7 + int(m[16]) * 2 ** 6 + int(m[17]) * 2 ** 5 + int(m[18]) * 2 ** 4 + int(m[19]) * \
#                     2 ** 3 + int(m[20]) * 2 ** 2 + int(m[21]) * 2 ** 1 + int(m[22]) * 2 ** 0) / 8388608
#
#         exponent = int(o2_bin[1:9], 2)
#         sign = (-1) ** (int(o2_bin[0], 2))
#
#         o2_ppm = sign * (2 ** (exponent - 127)) * (1 + mantissa)
#         o2_ppb = 1000 * o2_ppm
#
#         ser.close()
#         print(o2_ppb)
#         return (str(o2_ppb))
#
#     except Exception as e:
#         print("get_O2 error:" + str(e))
#         pass


