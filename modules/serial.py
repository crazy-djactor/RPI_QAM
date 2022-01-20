import binascii
import time
import serial

from modules.Util import raw_to_ppb


class SerialInterface:
    comPortOxygen = ""
    deltafConnected = False
    meecoConnected = False
    comPortMoist = ""
    demoMode = True

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
                    deltafConnected = True
                    # print("deltaf connected")
                    # await asyncio.sleep(0.2)
                    time.sleep(0.2)
                except:
                    deltafConnected = False
                comPortOxygen = '/dev/ttyUSB0'
                # await asyncio.sleep(0.2)
                time.sleep(0.2)
        except:
            deltafConnected = False
            print("deltaf not connected")
            pass

        global comPortMoist
        comPortMoist = '/dev/ttyUSB0'
        try:
            testComMoisture = raw_to_ppb(cls.get_h20())
            comPortMoist = '/dev/ttyUSB0'
            meecoConnected = True
        except:
            comPortMoist = '/dev/ttyUSB1'
            meecoConnected = False

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
        return (data)
        # await asyncio.sleep(sleepy)
        # time.sleep(sleepy)
        ser.close()

    @classmethod
    def get_O2(cls):
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
