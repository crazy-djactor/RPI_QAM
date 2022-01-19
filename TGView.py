#!/usr/bin/python3

import matplotlib

from modules.AdjustFigure import AdjustFigure
from GlobalConst import dir_TGView, root_path
from Util import raw_to_ppb, time_elapsed_string
from component.PopupWindow import PopupWindow

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import SpanSelector
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
# ADDED AS AN EXPERIMENTAL WAY TO MANAGE THE TOOLBAR
# plt.rcParams['toolbar'] = 'toolmanager'
# from matplotlib.backend_tools import ToolBase, ToolToggleBase
from fpdf import FPDF
from statistics import mean

import math
import textwrap
import shutil
import random
import serial
import time
import binascii
import csv
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from tkinter import filedialog
from tkfilebrowser import askopendirname
import numpy as np
from datetime import datetime, timedelta
from PIL import ImageTk
from PIL import Image
from PIL import ImageFile
import os, sys

from tkinter import Toplevel

ImageFile.LOAD_TRUNCATED_IMAGES = True  ##required for loading certain images
QAM_GREEN = "#7fa6a3"  ###html color code for QAM green

#### initial animation intervals are adjusted later###
intervalO2 = 3500
intervalH2O = 3500


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


# converts whole numbers to decimal equivalent (234 becomes .234)
def decimal_converter(num):
    while num > 1:
        num /= 10
    return num

    # function for converting a float number to a 5 byte IEEE-754 packet


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


# uses the write_serial_float function to write values to upper and lower meeco bands
def write_upperandlower(valueToUpper, valueToLower):
    write_serial_float(bytearray([178]), bytearray([15]), valueToUpper)
    # time.sleep(0.02)
    write_serial_float(bytearray([178]), bytearray([16]), valueToLower)


# asks meeco for a decimal number
###operand variables below:
### 0 for raw cell value
### 1 for avg cell value
### 15 for upper band limit
### 16 for lower band limit
def read_serial_float(operand):
    operand = bytearray([operand])

    data = bytearray()
    echo = bytearray()
    command = bytearray([146])
    # operand =bytearray([16])

    sleepy = 0.02

    ser = serial.Serial(
        port=comPortMoist, \
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


# write a decimal number to the meeco
###operand variables below:
### 0 for raw cell value
### 1 for avg cell value
### 15 for upper band limit
### 16 for lower band limit
### command=bytearray([178]) for sending
### command=bytearray([146]) for receiving
def write_serial_float(command, operand, valueToWrite):
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
        port=comPortMoist, \
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


# writes integers to meeco (current mode is the only thing that currently uses this)
def write_serial_int(send, n):
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
        port=comPortMoist, \
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
def get_O2(comPortOxygen):
    ser = serial.Serial(
        port=comPortOxygen, \
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
def get_O2temp(comPortOxygen):
    ser = serial.Serial(
        port=comPortOxygen, \
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
def get_h20(comPortMoist):
    data = bytearray()
    echo = bytearray()
    command = bytearray([146])
    operand = bytearray([1])
    sleepy = 0.02

    ser = serial.Serial(
        port=comPortMoist, \
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


#####GUI

# assign font for final PDF graphs
font0 = FontProperties()
font0.set_family('sans-serif')
font0.set_weight('bold')
font0.set_size('xx-large')

# assign fonts for various GUI components
LARGEST_FONT = ("Lato", 68, 'bold')
LARGER_FONT = ("Lato", 45, 'bold')
LARGE_FONT = ("Lato", 28, 'bold')
SMALL_FONT = ("Lato", 20, 'bold')
SMALLER_FONT = ("Lato", 18)
SMALLERR_FONT = ("Lato", 14)
SMALLEST_FONT = ("Lato", 8)

# assign matplotlib plot style
style.use("seaborn-whitegrid")

## global figure and subplots assigned here
global a1, a2, a3
# global f1, f2
figure_conf = AdjustFigure.default_figure_conf()

f1 = Figure(figsize=(figure_conf['w'], figure_conf['h']), dpi=figure_conf['dpi'],
            facecolor=(0.35, 0.35, 0.35))  # Figure(figsize=(7,6),dpi=100
f2 = Figure(figsize=(figure_conf['w'], figure_conf['h']), dpi=figure_conf['dpi'],
            facecolor=(0.35, 0.35, 0.35))  # Figure(figsize=(7,6),dpi=100

# Testing a combined figure with two subplots 9/3/2020

a1 = f1.add_subplot(111, facecolor=(0.25, 0.25, 0.25))  # (121,
a2 = f2.add_subplot(111, facecolor=(0.25, 0.25, 0.25))  # f1 (122,

f2.subplots_adjust(left=0.13, right=0.95, bottom=0.19, top=0.93, hspace=0.3)
f1.subplots_adjust(left=0.13, right=0.95, bottom=0.19, top=0.93, hspace=0.3)
# f1.set_tight_layout(True)
# f2.set_tight_layout(True)
o2_dataList = ""
h2o_dataList = ""

## set initial recording variable to false (changes to true when you click 'start recording')
recording = False

## set start_time (this is reset whenever start/stop_recording is clicked)
start_time = datetime.now()
global start_timee
start_timee = start_time.strftime("%m_%d_%y_%I.%M.%S")
global start_timeez
start_timeez = start_time.strftime("%m/%d/%y @ %I:%M %p")

##assign global cycle counts and set to plot the next data grab##
global cycleO2, cycleH2O
cycleH2O = 14
cycleO2 = 14

## set initial plot min/max to 0/10 (this is adjust based on data being plotted)
o2data_max = 10
o2data_min = 0
h2odata_max = 10
h2odata_min = 0


####First Toplevel frame to appear is Splash. RPiReader initializes after splash####
class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent, bg='grey25')
        # w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        # self.geometry("%dx%d%+d%+d" % (1920, 1080, 0, 0))
        self.attributes('-type', 'splash')
        self.geometry("%dx%d%+d%+d" % (1920, 1080, -2, 30))
        self.title("  Trace Gas View  ")

        self.myIcon = ImageTk.PhotoImage(file=f'{root_path}/TGViewClean.png')
        self.iconphoto(True, self.myIcon)

        ####### REPLACED the time, date, and logo image with a splash screen image #######
        splashXField = 550
        splashYField = 180
        splashXPadding = 25
        splashYPadding = 170

        ### Splash Logo
        self.gambar = Image.open(f'{root_path}/SplashScreen2021.png')
        self.imgSplash = ImageTk.PhotoImage(self.gambar)
        self.img = Label(self, image=self.imgSplash, bg="grey25")
        self.img.image = self.imgSplash
        # self.img.place(x=splashXField+splashXPadding*4,y=splashYField+splashYPadding)
        self.img.place(x=0, y=0)

        ### Splash Title - COMMENTED OUT 9/4/2020
        # label1 = tk.Label(self, text="Trace Gas View", font=("Helvetica", 69, 'bold'))
        # label1.place(x=splashXField+splashXPadding,y=splashYField)
        # label1.config(bg="grey25", fg='white')

        ### Current time and date display for Splash Screen - COMMENTED OUT 9/4/2020
        # label3 = tk.Label(self, text=start_timeez, font=("Helvetica", 58, 'bold'))
        # label3.place(x=splashXField,y=splashYField+splashYPadding*4.2)
        # label3.config(bg="grey25", fg='white')
        self.update()


# RPiReader class unpacks and shows pages. Also holds the window title and icon. Any new pages need to be added to self.frames{}
####But first the splash screen shows and runs through serial checks before splash screen is destroyed
class RPiReader(tk.Tk):
    def __init__(self, *args, **kwargs):  # args are variables. kwargs are keyboard args (dictionarys and such)

        tk.Tk.__init__(self, *args, **kwargs)
        # self.overrideredirect(True)
        self.geometry("%dx%d%+d%+d" % (1920, 1080, 0, 65))
        self.wm_attributes('-type', 'splash')
        self.withdraw()

        ####Display splash screen first while startup sequence continues
        splash = Splash(self)

        self.myIcon = ImageTk.PhotoImage(file=f'{root_path}/TGViewClean.png')
        self.iconphoto(True, self.myIcon)
        tk.Tk.wm_title(self, "  Trace Gas View  ")

        ####Check to see if TGView is already open (prevent startup if it is)
        p = os.popen("ps aux | grep 'TGView.py' | cut -c 43-44")
        p = p.read()
        # print(p)
        if "4" in p or "3" in p or "2" in p:
            fuckitup('start')
            time.sleep(10)
            sys.exit()

        ####Check to see which serial port sounds like a meeco and which sounds like a deltaf
        def serial_checker():
            global deltafConnected
            global meecoConnected
            global comPortOxygen
            # #await asyncio.sleep(0.9)
            time.sleep(0.9)
            try:
                comPortOxygen = '/dev/ttyUSB1'
                testComOxygen = get_O2(comPortOxygen=comPortOxygen)
                deltafConnected = True

                if 'e' in testComOxygen:
                    time.sleep(0.2)
                    try:
                        testComOxygen = get_O2(comPortOxygen)
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
                testComMoisture = raw_to_ppb(get_h20(comPortMoist))
                comPortMoist = '/dev/ttyUSB0'
                meecoConnected = True
            except:
                comPortMoist = '/dev/ttyUSB1'
                meecoConnected = False

            #         print("meeco not connected")
            # #await asyncio.sleep(1)
            time.sleep(1)

        serial_checker()
        # loop = asyncio.new_event_loop()
        # loop.run_until_complete(serial_checker())
        # loop.close()

        ## adjust time for splash screen to stay open
        time.sleep(0.4)

        ## destroy splash and bring up StartPage
        splash.destroy()
        self.deiconify()
        container = tk.Frame(self, bg='black')

        w = 1920
        h = 1080

        # This gets the current screen width and height
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        # Calculate the x and y coordinates based on the current screen size
        sx = (ws / 2) - (w / 2)
        sy = (hs / 2) - (h / 2)

        # CHANGED VALUES AFTER "w, h," TO REMOVE WHITE BAR ON LEFT SIDE
        # self.overrideredirect(True)
        # self.geometry("%dx%d%+d%+d" % (1920,1080,-2,30))

        # self.wm_attributes('-type', 'splash')
        # self.wm_geometry('1920x1020+0+0')
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, AnalyzerFieldsScreen):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# StartPage appears first. contains


class StartPage(tk.Frame):
    recording = False

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=1920, height=1080)
        # self.overrideredirect(True)
        # self.geometry('200x200')

        ##StartPage Title
        label1 = tk.Label(self, text="Trace Gas View", font=LARGEST_FONT)
        pax = 420
        pay = 120
        label1.place(x=635, y=10)
        label1.config(bg="grey25", fg='white')
        # label1 = tk.Label(self, text="by QAM", font=LARGE_FONT)
        # label1.place(x=900,y=110)
        # label1.config(bg="grey25", fg=QAM_GREEN)

        ### Button icons
        aboutIcon = ImageTk.PhotoImage(file=f"{root_path}/info.png", master=self)
        beginIcon = ImageTk.PhotoImage(file=f"{root_path}/plot1.png", master=self)
        saveIcon = ImageTk.PhotoImage(file=f"{root_path}/download.png", master=self)
        modifyIcon = ImageTk.PhotoImage(file=f"{root_path}/edit.png", master=self)
        settingsIcon = ImageTk.PhotoImage(file=f"{root_path}/settings.png", master=self)

        ## Start page QAM logo
        QAMstart = Image.open(f'{root_path}/QAM.gif')
        imgStart = ImageTk.PhotoImage(QAMstart, master=self)
        imggg = tk.Label(self, image=imgStart, borderwidth=0, highlightthickness=0)
        imggg.image = imgStart
        imggg.place(x=155, y=20)

        ## Open button icons
        # modifyImg = Image.open('./QAM.gif')

        ## TGView background color
        self.configure(background="grey25")

        ## place holder for testing status messages. Warns user when analyzer is disconnected
        global testingStatusMessageMeeco
        testingStatusMessageMeeco = StringVar(value="")
        global testingStatusMessageDeltaf
        testingStatusMessageDeltaf = StringVar(value="")

        deltafStatusMessageXfield = 120
        meecoStatusMessageXfield = 1380
        statusMessageYfield = 145
        label = tk.Label(self, textvariable=testingStatusMessageDeltaf, font=("Lato", 26, 'bold'))
        label.config(bg="grey25", fg="firebrick1")
        label.place(x=deltafStatusMessageXfield, y=statusMessageYfield)

        label = tk.Label(self, textvariable=testingStatusMessageMeeco, font=("Lato", 26, 'bold'))
        label.config(bg="grey25", fg="firebrick1")
        label.place(x=meecoStatusMessageXfield, y=statusMessageYfield)

        ## read Header_default.csv for test parameters
        with open(f'{root_path}/Header_default.csv', newline='') as t:
            headreader = csv.reader(t)
            global header_list
            header_list = []
            for row in headreader:
                header_list.append(row[0])
        global title
        global client
        global location
        global building
        global tool_id
        global test_gas
        global source_gas
        global technician
        global system_flow
        global comments
        global deltaf_serial
        global deltaf_cal
        global deltaf_flow
        global deltaf_spec
        global tracer_serial
        global tracer_cal
        global tracer_flow
        global tracer_spec
        title = header_list[0]
        client = header_list[1]
        location = ""
        building = ""
        tool_id = ""
        test_gas = ""
        source_gas = ""
        technician = ""
        system_flow = ""
        comments = ""
        # location = header_list[2] #### don't collect the data that the user has to input every time
        # building = header_list[3]
        # tool_id = header_list[4]
        # test_gas = header_list[5]
        # source_gas = header_list[6]
        # technician = header_list[7]
        # system_flow = header_list[8]
        # comments = header_list[9]
        deltaf_serial = header_list[10]
        deltaf_cal = header_list[11]
        deltaf_flow = header_list[12]
        deltaf_spec = header_list[13]
        tracer_serial = header_list[14]
        tracer_cal = header_list[15]
        tracer_flow = header_list[16]
        tracer_spec = header_list[17]
        ### create initial path (this is only used if the user never starts test)
        global pathstart
        pathstart = f'{root_path}/TGView/' + str(client) + "_" + str(location) + "_" + str(title) + "_" + start_timee

        ### var2 determines which analyzer is talking
        global var2
        var2 = StringVar()
        ### default when the program starts is "both"
        var2.set('radBoth')

        def h2o_selected():
            print(var2.get())

        def o2_selected():
            print(var2.get())

        def both_selected():
            print(var2.get())

        ### radio button placement
        s1 = ttk.Style()
        s1.configure("both.TRadiobutton", font=('Century Gothic', 21, 'bold'), background="#404040",
                     foreground=QAM_GREEN, indicatoron=0, relief=FLAT)
        s1.configure("h2o.TRadiobutton", font=('Century Gothic', 21, 'bold'), background="#404040",
                     foreground="#00BFFF", indicatoron=0, relief=FLAT)
        s1.configure("o2.TRadiobutton", font=('Century Gothic', 21, 'bold'), background="#404040", foreground="#00CD66",
                     indicatoron=0, relief=FLAT)
        radioFont = ('Century Gothic', 21, 'bold')
        pax = 620
        pay = 460
        padx = 220
        rad_both = tk.Radiobutton(self, text="O2 & H2O", width=11, font=radioFont, variable=var2, selectcolor=QAM_GREEN,
                                  activebackground=QAM_GREEN, background="grey35", \
                                  highlightbackground=QAM_GREEN, activeforeground="white", foreground="white",
                                  indicatoron=0, value="radBoth", relief=FLAT, command=both_selected).place(
            x=padx + pax, y=130)  # (x=padx*2+pax,y=200+pay)
        rad_o2 = tk.Radiobutton(self, text="O2", width=11, font=radioFont, variable=var2, selectcolor="#00CD66",
                                activebackground="#00CD66", background="grey35", \
                                highlightbackground="#00CD66", activeforeground="white", foreground="white",
                                indicatoron=0, value="radO2", relief=FLAT, command=o2_selected).place(x=pax,
                                                                                                      y=130)  # (x=pax,y=200+pay)
        rad_h2o = tk.Radiobutton(self, text="H2O", width=11, font=radioFont, variable=var2, selectcolor="#00BFFF",
                                 activebackground="#00BFFF", background="grey35", \
                                 highlightbackground="#00BFFF", activeforeground="white", foreground="white",
                                 indicatoron=0, value="radH2O", relief=FLAT, command=h2o_selected).place(
            x=padx * 2 + pax, y=130)  # (x=padx+pax,y=200+pay)

        #### StartPage Graph placement (these are just .png copies of plots created in PageOne)
        pax = 60
        pay = 140
        graphXfield = 130
        graphXpad = 860
        global img_o2
        try:
            gambar = Image.open(f'{root_path}/TGView/graphO2.png')
        except:
            gambar = Image.open(f'{root_path}/graph1.png')
        imgSplash = ImageTk.PhotoImage(gambar)
        img_o2 = Label(self, image=imgSplash, bg="grey25")
        img_o2.image = imgSplash
        img_o2.place(x=20, y=200)
        #
        global img_h2o
        try:
            gambar2 = Image.open(f'{root_path}/TGView/graphH2O.png')
        except:
            gambar2 = Image.open(f'{root_path}/graph1.png')
        imgSplash2 = ImageTk.PhotoImage(gambar2)
        img_h2o = Label(self, image=imgSplash2, bg="grey25")
        img_h2o.image = imgSplash2
        img_h2o.place(x=970, y=200)

        ### button placement parameters
        pax += 150
        pay += 555
        pady = 80
        padx = 20
        mx = 22.8
        m = 2.4

        ### StartPage buttons
        button1 = tk.Button(self, text="X", compound="left", activebackground="#c98256", bg="grey35",
                            highlightbackground="#A26239", highlightthickness=7, relief="flat",
                            activeforeground="white", fg="White", font=('calibri', 40, 'bold'), borderwidth='1',
                            command=close_program)  # command=lambda: controller.show_frame(AnalyzerFieldsScreen) or equipment_controls
        button1.place(width=105, height=105, x=1785, y=30)  # (x=padx+pax,y=pay+26)
        # button1.image = aboutIcon (image=aboutIcon,)

        button1 = tk.Button(self, text="Modify Report", image=modifyIcon, compound="left", padx=40,
                            activebackground="orange", bg="grey35", highlightbackground="orange", highlightthickness=2,
                            relief=FLAT, activeforeground="white", fg="White", font=('calibri', 32, 'bold'),
                            borderwidth='1', command=manage_pdf)
        button1.place(width=445, height=105, x=970, y=pady * m + pay)  # (x=padx+pax,y=pady*m+pay)
        button1.image = modifyIcon

        button1 = tk.Button(self, text="About", image=aboutIcon, compound="left", padx=30, activebackground=QAM_GREEN,
                            bg="grey35", highlightbackground="#678277", highlightthickness=7, relief="flat",
                            activeforeground="white", fg="White", font=('calibri', 40, 'bold'), borderwidth='1',
                            command=about_window)  # command=lambda: controller.show_frame(AnalyzerFieldsScreen) or equipment_controls
        button1.place(width=300, height=105, x=1450, y=30)  # (x=padx+pax,y=pay+26)
        button1.image = aboutIcon

        button1 = tk.Button(self, text="Save Graph/s", image=saveIcon, compound="left", padx=55,
                            activebackground="#00CD66", bg="grey35", highlightbackground="#00CD66",
                            highlightthickness=2, relief="flat", activeforeground="white", fg="White",
                            font=('calibri', 32, 'bold'), borderwidth='1', command=stop_recording)
        button1.place(width=445, height=105, x=495, y=pady * m + pay)  # (x=padx*mx+pax,y=pady+pay)
        button1.image = saveIcon

        button1 = tk.Button(self, text="Change Settings", image=settingsIcon, compound="left", padx=35,
                            activebackground="#2FA4FF", bg="grey35", highlightbackground="#2FA4FF",
                            highlightthickness=2, relief="flat", activeforeground="white", fg="White",
                            font=('calibri', 32, 'bold'), borderwidth='1',
                            command=equipment_controls)  ## command=lambda: controller.show_frame(AnalyzerFieldsScreen)  borderwidth = '1',relief="flat",    #command=equipment_controls
        button1.place(width=445, height=105, x=1445, y=pady * m + pay)  # (x=padx*mx+pax,y=pady*m+pay)
        button1.image = settingsIcon

        def startTest_andshowPageOne():
            controller.show_frame(PageOne)
            confirm_fields(start_stop='start')

        # Start test and show PageOne
        button1 = tk.Button(self, text="Begin Testing", activebackground="firebrick1", image=beginIcon, compound="left",
                            padx=55, bg="grey35", highlightbackground="firebrick1", highlightthickness=2, relief="flat",
                            activeforeground="white", fg="White", font=('calibri', 32, 'bold'), borderwidth='1',
                            command=startTest_andshowPageOne)
        button1.place(width=445, height=105, x=20,
                      y=pady * m + pay)  # y=pady+pay x=20+pax      #old wxh width = 19, height = 2,
        button1.image = beginIcon

        ###### StartPage Current Data Readings
        pax = 400
        pay = 600
        padx = 200
        pady = 60
        xfield = 800

        # Show Current O2 Reading
        global labelO2
        o2_position = AdjustFigure.o2_axis()
        labelO2 = tk.Label(self, text="Current O2:", font=SMALL_FONT)
        labelO2.place(x=o2_position['label_x'], y=o2_position['label_y'])
        labelO2.config(bg="grey35", fg="white")
        #
        global currento2
        currento2 = StringVar(value=0)
        # fg="#00CD66"
        global labelO2_value
        labelO2_value = tk.Label(self, textvariable=currento2, width=6, bg="grey35", fg="#60D500",
                                 font=('calibri', 20, 'bold'))
        labelO2_value.place(x=o2_position['value_x'], y=o2_position['value_y'])

        # Show Current H2O Reading
        global labelH2O, labelH2O_value
        h2o_position = AdjustFigure.ho2_axis()
        labelH2O = tk.Label(self, text="Current H2O:", font=SMALL_FONT)
        labelH2O.place(x=h2o_position['label_x'], y=h2o_position['label_y'])
        labelH2O.config(bg="grey35", fg="white")

        global currenth2o
        currenth2o = StringVar(value=0)
        if int(currenth2o.get()) < 0:
            currenth2o = 0
        labelH2O_value = tk.Label(self, textvariable=currenth2o, width=6, bg="grey35", fg="#00BFFF",
                                  font=('calibri', 20, 'bold'))
        labelH2O_value.place(x=h2o_position['value_x'], y=h2o_position['value_y'])


##### Global Methods #####
def fuckitup(how):
    error_time = datetime.now()
    error_file = "error entry " + str(error_time.strftime("%m_%d_%y_%I.%M.%S"))
    pathE = '/home/pi/Desktop/ErrorLog/'
    with open(os.path.join(pathE, error_file) + '.csv', 'w+', newline='') as o:
        writer1 = csv.writer(o, escapechar=' ', quoting=csv.QUOTE_NONE)

        writer1.writerow([str(error_file)])
        if how == "start":
            writer1.writerow(['DO NOT OPEN MULTIPLE INSTANCES OF TGVIEW'])
            writer1.writerow(['CHECK REMOTE DESKTOP FOR RUNNING TEST'])
        else:
            if meecoConnected == True and deltafConnected == False:
                writer1.writerow(['DELTAF WAS DISCONNECTED DURING TESTING'])
                writer1.writerow(['LIST DETAILS OF FAILURE BELOW FOR REVIEW'])
            elif meecoConnected == False and deltafConnected == True:
                writer1.writerow(['MEECO WAS DISCONNECTED DURING TESTING'])
                writer1.writerow(['LIST DETAILS OF FAILURE BELOW FOR REVIEW'])
            elif meecoConnected == False and deltafConnected == False:
                writer1.writerow(['BOTH ANALYZERS STOPPED COMMUNICATING DURING TESTING'])
                writer1.writerow(['LIST DETAILS OF FAILURE BELOW FOR REVIEW'])
        o.flush()

    os.popen("mousepad " + "'" + os.path.join(pathE, error_file) + ".csv'")
    time.sleep(0.5)

    def fuckit():
        sys.exit()

    ######### error message should show error and close out program #######
    fuck = Toplevel()
    fuck.title("Error")
    # Width and height for the Tk root window
    w = 500
    h = 180
    # This gets the current screen width and height
    ws = fuck.winfo_screenwidth()
    hs = fuck.winfo_screenheight()
    # Calculate the x and y coordinates based on the current screen size
    sx = (ws / 2) - (w / 2)
    sy = (hs / 2) - (h / 2)
    # Open the root window in the middle of the screen
    fuck.geometry('%dx%d+%d+%d' % (w, h, sx, sy))
    fuck.resizable(False, False)
    fuck.config(bg="Grey25")
    msg = Message(fuck, text="Error has been logged.\nPlease restart TGView.", width=500, bg="grey25", fg="grey85",
                  font=LARGE_FONT)
    msg.pack()
    button = Button(fuck, text="EXIT", command=fuckit, width=20, height=2, bg="firebrick1", fg="white",
                    activebackground="firebrick2", activeforeground="white", highlightbackground="firebrick1",
                    relief=FLAT)
    button['font'] = LARGER_FONT
    button.pack()


### valindates input from user (used for writing int/float numbers to meeco... equipment controls)
def validate_input(new_input):
    valid_chars = " -_.()qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789"
    if all(c in valid_chars for c in new_input) == True and len(new_input) < 21:
        # print("okay")
        return True
    else:
        # print("FUCK")
        return False


def limit_character(new_input):
    if len(new_input) < 21:
        return True
    else:
        return False


def limit_comment(new_input):
    if len(new_input) < 60:
        return True
    else:
        return False


# see above
def retreive_input(inputs):
    inputValue = inputs.get("1.0", "end-1c")
    return inputValue


###### Close TG View
def close_program():
    sys.exit()


###### About TG View Window
# Displays relevant info such as the current version/build number
def about_window():
    # CURRENT VERSION/BUILD NUMBER
    # Adjust this when changes are made
    global version_num
    version_num = "v1.8.0"

    aboutFont = "lato"

    paddx = 15
    paddy = 15
    topA = Toplevel()
    # topA.attributes('-type', 'Dock')
    topA.title("Program Infomation")
    topA.configure(background="grey25")
    # Width and height for the Tk root window
    w = 720
    h = 465
    # This gets the current screen width and height
    ws = topA.winfo_screenwidth()
    hs = topA.winfo_screenheight()
    # Calculate the x and y coordinates based on the current screen size
    sx = (ws / 2) - (w / 2)
    sy = (hs / 2) - (h / 2)
    # Open the root window in the middle of the screen
    # topA.overrideredirect(True)
    topA.geometry('%dx%d+%d+%d' % (w, h, sx, sy))
    paddy = 5

    ## Button image
    likeIcon = ImageTk.PhotoImage(file=f"{root_path}/like.png", master=topA)

    ### Dispaly the time that the program was opened to ensure testing validity
    label4 = tk.Label(topA, text="Application opened:", bg="grey25", fg='orange', font=(aboutFont, 40, 'bold'))
    label4.place(relx=.5, rely=.12, anchor="center")

    label4 = tk.Label(topA, text=start_timeez, bg="grey25", fg='white', font=(aboutFont, 40, 'bold'))
    label4.place(relx=.5, rely=.26, anchor="center")

    ##### equipment controls title
    label1 = tk.Label(topA, text="Build Number:", bg="grey25", fg=QAM_GREEN, font=(aboutFont, 40, 'bold'))
    label1.place(relx=.5, rely=.43, anchor="center")

    label2 = tk.Label(topA, text=version_num, bg="grey25", fg="white", font=(aboutFont, 40, 'bold'))
    label2.place(relx=.5, rely=.56, anchor="center")

    label3 = tk.Label(topA, text="Developed by Joel Taylor and Joshua Hoover", bg="grey25", fg="white",
                      font=(aboutFont, 14))
    label3.place(relx=.5, rely=.95, anchor="center")

    # QAM dark green: #678277
    button1 = tk.Button(topA, text="Got it!", image=likeIcon, compound="left", padx=40, activebackground="#678277",
                        bg="grey35", highlightbackground="#678277", highlightthickness=2, relief="flat",
                        activeforeground="white", fg="White", font=(aboutFont, 37, 'bold'), borderwidth='1',
                        command=topA.destroy)
    button1.place(width=305, height=95, relx=.5, rely=.8, anchor="center")
    button1.image = likeIcon


###### meeco controls
# reads raw cell value, current upper/lower band limits, and current mode (service/inert)
# writes upper/lowerband limites and mode (service/inert)
def equipment_controls():
    paddx = 15
    paddy = 15
    top5 = Toplevel()
    top5.title("Equipment Controls")
    # top5.geometry("1000x500")
    top5.configure(background="grey25")
    # Width and height for the Tk root window
    w = 960
    h = 620
    # This gets the current screen width and height
    ws = top5.winfo_screenwidth()
    hs = top5.winfo_screenheight()
    # Calculate the x and y coordinates based on the current screen size
    sx = (ws / 2) - (w / 2)
    sy = (hs / 2) - (h / 2)
    # Open the root window in the middle of the screen
    top5.geometry('%dx%d+%d+%d' % (w, h, sx, sy))
    paddy = 5

    ##### equipment controls title
    label1 = tk.Label(top5, text="Meeco Tracer 2", bg="grey25", fg=QAM_GREEN, font=LARGEST_FONT)
    label1.place(x=130, y=paddy)

    ###Show/Change Current Meeco Mode

    currentMode = StringVar()
    meecoMode = int(write_serial_int(False, 0))  #### comment out for random data###
    # meecoMode = 0
    if meecoMode == 1:
        currentMode.set('Inert')
    if meecoMode == 0:
        currentMode.set('Service')
    currentUpper = StringVar()
    currentLower = StringVar()
    currentUpper.set(round(float(raw_to_ppb(read_serial_float(15))), 1))  #### comment out for random data###
    # time.sleep(0.02)
    currentLower.set(round(float(raw_to_ppb(read_serial_float(16))), 1))  #### comment out for random data###
    global currentRaw

    modeXfield = 255
    modeXpad = 260
    modeXbuttonPad = 158
    i = 0.3

    bandXfield = 10
    bandXpad1 = 265
    bandXpad2 = 345
    paddy -= 30
    label1 = tk.Label(top5, text="Current Mode:", bg="grey25", fg="grey85", font=LARGE_FONT)
    label1.place(x=modeXfield, y=160 + paddy)

    label14 = tk.Label(top5, textvariable=currentMode, width=6, bg="grey25", fg="grey85", font=('calibri', 26, 'bold'))
    label14.place(x=modeXfield + modeXpad, y=168 + paddy)

    def change_to_service():
        write_serial_int(True, 0)
        currentMode.set("Service")

    def change_to_inert():
        write_serial_int(True, 1)
        currentMode.set("Inert")

    button1 = tk.Button(top5, text="Service", bg="grey35", activebackground="#2fa4ff", fg="White",
                        activeforeground="white", highlightbackground="#2fa4ff", highlightthickness=2, relief=FLAT,
                        font=SMALL_FONT, width=8, command=change_to_service)
    button1.place(x=320, y=220 + paddy)  # (x=modeXfield+modeXpad*i,y=220+paddy)

    button1 = tk.Button(top5, text="Inert", bg="grey35", activebackground="#00cd66", fg="White",
                        activeforeground="white", highlightbackground="#00cd66", highlightthickness=2, relief=FLAT,
                        font=SMALL_FONT, width=8, command=change_to_inert)
    button1.place(x=480, y=220 + paddy)  # (x=modeXfield+modeXpad*i+modeXbuttonPad,y=220+paddy)
    paddy += 30
    label19 = tk.Label(top5, text=' ', width=800, bg='grey85', fg='grey85', font=('calibri', 1, 'bold'))
    label19.place(x=60, y=300 + paddy)

    paddy += 175
    i = 1
    bandXfield -= 330
    label14 = tk.Label(top5, text="Current Raw Cell Value:", bg="grey25", fg="grey85", font=('calibri', 20, 'bold'))
    label14.place(x=bandXfield + bandXpad1 + bandXpad2, y=160 + paddy * i)
    bandXfield += 275
    label14 = tk.Label(top5, textvariable=currentRaw, bg="grey25", fg="grey85", font=('calibri', 20, 'bold'))
    label14.place(x=bandXfield + bandXpad1 + bandXpad2, y=160 + paddy * i)
    bandXfield += 95
    paddy += 60
    label14 = tk.Label(top5, text="Upper Band:", width=20, bg="grey25", fg="white", font=SMALL_FONT)
    label14.place(x=bandXfield, y=160 + paddy)

    label14 = tk.Label(top5, text="Lower Band:", width=20, bg="grey25", fg="white", font=SMALL_FONT)
    label14.place(x=bandXfield + bandXpad2, y=160 + paddy)
    paddy += 10
    upper_band = DoubleVar(value=currentUpper.get())
    textbox = ttk.Entry(top5, width=10, textvariable=upper_band)
    textbox.place(x=bandXfield + bandXpad1, y=160 + paddy)

    lower_band = DoubleVar(value=currentLower.get())
    textbox = ttk.Entry(top5, width=10, textvariable=lower_band)
    textbox.place(x=bandXfield + bandXpad1 + bandXpad2, y=160 + paddy)
    paddy += 60
    button1 = tk.Button(top5, text="Set New Bands", bg="grey35", activebackground="orange", fg="White",
                        activeforeground="white", highlightbackground="orange", highlightthickness=2, relief=FLAT,
                        font=LARGE_FONT, borderwidth='1', width=12,
                        command=lambda: write_upperandlower(upper_band.get(), lower_band.get()))
    button1.place(x=185, y=160 + paddy)
    button1 = tk.Button(top5, text="Save/Exit", bg="grey35", activebackground="firebrick1", fg="White",
                        activeforeground="white", highlightbackground="firebrick1", highlightthickness=2, relief=FLAT,
                        font=LARGE_FONT, borderwidth='1', width=12, command=top5.destroy)
    button1.place(x=485, y=160 + paddy)


class AnalyzerFieldsScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="Stored Parameters", font=LARGEST_FONT)
        label1.place(x=575, y=30)
        label1.config(bg="grey25", fg="#7fa6a3")

        self.configure(background="grey25")

        # REMOVED THE OLD, FUZZY, QAM LOGO 10/23/2020
        # self.gambar = Image.open('./qam_logo_transparent(2).png')
        # self.imgSplash = ImageTk.PhotoImage(self.gambar)
        # self.img = Label(self, image=self.imgSplash, bg="grey25")
        # self.img.image = self.imgSplash
        # self.img.place(x=750, y=750)

        def update_fields():
            global header_list
            # header_list[0] = self.title.get()
            header_list[1] = self.client.get()
            # header_list[2] = self.location.get()     #location=system
            header_list[3] = self.building.get()  # building=facility
            # header_list[4] = self.tool_id.get()
            # header_list[5] = self.test_gas.get()
            # header_list[6] = self.source_gas.get()      #source_gas=source gas id
            # header_list[7] = self.technician.get()
            # header_list[8] = self.system_flow.get()
            header_list[10] = self.deltaf_serial.get()
            header_list[11] = self.deltaf_cal.get()
            header_list[12] = self.deltaf_flow.get()
            header_list[13] = self.deltaf_spec.get()
            header_list[14] = self.tracer_serial.get()
            header_list[15] = self.tracer_cal.get()
            header_list[16] = self.tracer_flow.get()
            header_list[17] = self.tracer_spec.get()
            with open(f'{root_path}/Header_default.csv', 'w+', newline='') as d:
                writer4 = csv.writer(d)
                for row in header_list:
                    writer4.writerow([row])
                d.close()

        # dashIcon = ImageTk.PhotoImage(file = r"./dashboard.png")
        # button1 = tk.Button(self, text="Back", font=LARGE_FONT, fg="white", activeforeground="white", bg="#678176", activebackground="#81a6a3", padx=25, command=lambda: controller.show_frame(StartPage))
        # button1.place(x=20,y=20)

        def back_and_update_fields():
            controller.show_frame(StartPage)

            update_fields()

        savecIcon = ImageTk.PhotoImage(file=f"{root_path}/SaveC.png", master=self)

        button1 = tk.Button(self, text="Save Changes", image=savecIcon, compound="left", padx=40, bg="grey35",
                            activebackground="#678277", fg="White", activeforeground="white",
                            highlightbackground=QAM_GREEN, highlightthickness=2, relief=FLAT, font=LARGER_FONT,
                            command=back_and_update_fields)
        button1.place(height=125, width=750, x=575, y=790)
        button1.image = savecIcon

        with open(f'{root_path}/Header_default.csv', newline='') as t:
            headreader = csv.reader(t)
            global header_list
            header_list = []
            for row in headreader:
                header_list.append(row[0])

        paddx = 590
        paddy = 85
        i = 1

        ####Document fields (title, client, etc)
        '''
        # title entry
        label3 = tk.Label(self, text="Test Point ID:", font=SMALL_FONT)
        label3.place(x=15+paddx,y=50+paddy*i)
        label3.config(bg="grey25",fg="white")

        global title
        self.title = StringVar(self, value=header_list[0])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.title)
        self.textbox.place(x=15+paddx,y=85+paddy*i)
        title = self.title
        i=i+1
        '''

        # client entry
        label4 = tk.Label(self, text="Client:", font=SMALL_FONT)
        label4.place(x=15 + paddx, y=90 + paddy * i)
        label4.config(bg="grey25", fg="white")

        global client
        self.client = StringVar(self, value=header_list[1])
        self.textbox = ttk.Entry(self, width=20, textvariable=self.client, font=SMALLER_FONT)
        self.textbox.place(x=15 + paddx, y=130 + paddy * i)
        reg = self.register(validate_input)
        self.textbox.config(validate='key', validatecommand=(reg, '%P'))
        client = self.client
        # i=i+1

        '''
        # location entry
        label4 = tk.Label(self, text="Location:", font=SMALL_FONT)
        label4.place(x=15+paddx,y=50+paddy*i)
        label4.config(bg="grey25",fg="white")

        global location
        self.location = StringVar(self, value=header_list[2])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.location)
        self.textbox.place(x=15+paddx,y=85+paddy*i)
        location = self.location
        i=i+1
        '''

        # building entry
        label4 = tk.Label(self, text="Facility:", font=SMALL_FONT)
        label4.place(x=420 + paddx, y=90 + paddy * i)
        label4.config(bg="grey25", fg="white")

        global building
        self.building = StringVar(self, value=header_list[3])
        self.textbox = ttk.Entry(self, width=20, textvariable=self.building, font=SMALLER_FONT)
        self.textbox.place(x=420 + paddx, y=130 + paddy * i)
        reg = self.register(limit_character)
        self.textbox.config(validate='key', validatecommand=(reg, '%P'))
        building = self.building
        i = i + 1

        '''
        # tool_id entry
        label4 = tk.Label(self, text="Tool ID:", font=SMALL_FONT)
        label4.place(x=15+paddx,y=50+paddy*i)
        label4.config(bg="grey25",fg="white")

        global tool_id
        self.tool_id = StringVar(self, value=header_list[4])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.tool_id)
        self.textbox.place(x=15+paddx,y=85+paddy*i)
        tool_id = self.tool_id
        i=i+1

        # test gas entry
        label5 = tk.Label(self, text="Test Gas:", font=SMALL_FONT)
        label5.place(x=15+paddx,y=50+paddy*i)
        label5.config(bg="grey25",fg="white")

        global test_gas
        self.test_gas = StringVar(self, value=header_list[5])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.test_gas)
        self.textbox.place(x=15+paddx,y=85+paddy*i)
        test_gas = self.test_gas
        i=i+1

        # source gas entry
        label6 = tk.Label(self, text="Source Gas (PPB):", font=SMALL_FONT)
        label6.place(x=15+paddx,y=50+paddy*i)
        label6.config(bg="grey25",fg="white")

        global source_gas
        self.source_gas = StringVar(self, value=header_list[6])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.source_gas)
        self.textbox.place(x=15+paddx,y=85+paddy*i)
        source_gas = self.source_gas
        i=i+1

        # technician entry
        label7 = tk.Label(self, text="Technician:", font=SMALL_FONT)
        label7.place(x=15+paddx,y=50+paddy*i)
        label7.config(bg="grey25",fg="white")

        global technician
        self.technician = StringVar(self, value=header_list[7])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.technician)
        self.textbox.place(x=15+paddx,y=85+paddy*i)
        technician = self.technician
        i=i+1

        # system flow entry
        label8 = tk.Label(self, text="System Flow:", font=SMALL_FONT)
        label8.place(x=15+paddx,y=50+paddy*i)
        label8.config(bg="grey25",fg="white")

        global system_flow
        self.system_flow = StringVar(self, value=header_list[8])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.system_flow)
        self.textbox.place(x=15+paddx,y=85+paddy*i)
        system_flow = self.system_flow
        i=i+1

        #comments entry
        label9 = tk.Label(self, text="Comments:", font=SMALL_FONT)
        label9.place(x=15+paddx,y=50+paddy*i)
        label9.config(bg="grey25",fg="white")

        global comments
        self.comments = StringVar(self, value=header_list[9])
        self.textbox = ttk.Entry(self,width=40, textvariable = self.comments)
        self.textbox.place(x=15+paddx,y=85+paddy*i, height=100,width=400)
        comments = self.comments
        '''

        ### analyser info entries
        ## delta f info entry
        # deltaf serial number entry
        i = 0
        xfield = 15
        label10 = tk.Label(self, text="Oxygen Analyzer", font=LARGE_FONT)
        label10.place(x=xfield + paddx, y=310 + paddy * i)
        label10.config(bg="grey25", fg="#7fa6a3")

        label10 = tk.Label(self, text="Serial Number:", font=SMALL_FONT)
        label10.place(x=xfield + paddx, y=360 + paddy * i)
        label10.config(bg="grey25", fg="white")

        global deltaf_serial
        self.deltaf_serial = StringVar(self, value=header_list[10])
        self.textbox = ttk.Entry(self, width=20, textvariable=self.deltaf_serial, font=SMALLER_FONT)
        self.textbox.place(x=xfield + paddx, y=400 + paddy * i)
        deltaf_serial = self.deltaf_serial
        i = i + 1

        # deltaf calibration date entry
        label11 = tk.Label(self, text="Calibration Due:", font=SMALL_FONT)
        label11.place(x=xfield + paddx, y=360 + paddy * i)
        label11.config(bg="grey25", fg="white")

        global deltaf_cal
        self.deltaf_cal = StringVar(self, value=header_list[11])
        self.textbox = ttk.Entry(self, width=20, textvariable=self.deltaf_cal, font=SMALLER_FONT)
        self.textbox.place(x=xfield + paddx, y=400 + paddy * i)
        deltaf_cal = self.deltaf_cal
        i = i + 1

        # instrument flow entry
        label12 = tk.Label(self, text="Flow (LPM):", font=SMALL_FONT)
        label12.place(x=xfield + paddx, y=360 + paddy * i)
        label12.config(bg="grey25", fg="white")

        global deltaf_flow
        self.deltaf_flow = StringVar(self, value=header_list[12])
        self.textbox = ttk.Entry(self, width=20, textvariable=self.deltaf_flow, font=SMALLER_FONT)
        self.textbox.place(x=xfield + paddx, y=400 + paddy * i)
        deltaf_flow = self.deltaf_flow
        i = i + 1

        # instrument specification
        label13 = tk.Label(self, text="Specification (PPB):", font=SMALL_FONT)
        label13.place(x=xfield + paddx, y=360 + paddy * i)
        label13.config(bg="grey25", fg="white")

        global deltaf_spec
        self.deltaf_spec = StringVar(self, value=header_list[13])
        self.textbox = ttk.Entry(self, width=20, textvariable=self.deltaf_spec, font=SMALLER_FONT)
        self.textbox.place(x=xfield + paddx, y=400 + paddy * i)
        deltaf_spec = self.deltaf_spec

        ## tracer2 info entry
        # tracer2 serial number entry
        i = 0
        xfield = 420
        label10 = tk.Label(self, text="Moisture Analyzer", font=LARGE_FONT)
        label10.place(x=xfield + paddx - 10, y=310 + paddy * i)
        label10.config(bg="grey25", fg="#7fa6a3")

        label10 = tk.Label(self, text="Serial Number:", font=SMALL_FONT)
        label10.place(x=xfield + paddx, y=360 + paddy * i)
        label10.config(bg="grey25", fg="white")

        global tracer_serial
        self.tracer_serial = StringVar(self, value=header_list[14])
        self.textbox = ttk.Entry(self, width=20, textvariable=self.tracer_serial, font=SMALLER_FONT)
        self.textbox.place(x=xfield + paddx, y=400 + paddy * i)
        tracer_serial = self.tracer_serial
        i = i + 1

        # tracer2 calibration date entry
        label11 = tk.Label(self, text="Calibration Due:", font=SMALL_FONT)
        label11.place(x=xfield + paddx, y=360 + paddy * i)
        label11.config(bg="grey25", fg="white")

        global tracer_cal
        self.tracer_cal = StringVar(self, value=header_list[15])
        self.textbox = ttk.Entry(self, width=20, textvariable=self.tracer_cal, font=SMALLER_FONT)
        self.textbox.place(x=xfield + paddx, y=400 + paddy * i)
        tracer_cal = self.tracer_cal
        i = i + 1

        # instrument flow entry
        label12 = tk.Label(self, text="Flow (LPM):", font=SMALL_FONT)
        label12.place(x=xfield + paddx, y=360 + paddy * i)
        label12.config(bg="grey25", fg="white")

        global tracer_flow
        self.tracer_flow = StringVar(self, value=header_list[16])
        self.textbox = ttk.Entry(self, width=20, textvariable=self.tracer_flow, font=SMALLER_FONT)
        self.textbox.place(x=xfield + paddx, y=400 + paddy * i)
        tracer_flow = self.tracer_flow
        i = i + 1

        # instrument specification
        label13 = tk.Label(self, text="Specification (PPB):", font=SMALL_FONT)
        label13.place(x=xfield + paddx, y=360 + paddy * i)
        label13.config(bg="grey25", fg="white")

        global tracer_spec
        self.tracer_spec = StringVar(self, value=header_list[17])
        self.textbox = ttk.Entry(self, width=20, textvariable=self.tracer_spec, font=SMALLER_FONT)
        self.textbox.place(x=xfield + paddx, y=400 + paddy * i)
        tracer_spec = self.tracer_spec


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global currentRaw
        currentRaw = StringVar()
        if deltafConnected == True and meecoConnected == True:
            testingStatusMessageMeeco.set('')
            testingStatusMessageDeltaf.set('')
        elif deltafConnected == True and meecoConnected == False:
            testingStatusMessageMeeco.set("Check Tracer 2 Connection")
            testingStatusMessageDeltaf.set('')
        elif deltafConnected == False and meecoConnected == True:
            testingStatusMessageDeltaf.set("Check DeltaF Connection")
            testingStatusMessageMeeco.set("")
        else:
            testingStatusMessageMeeco.set("Check Tracer 2 Connection")
            testingStatusMessageDeltaf.set("Check DeltaF Connection")

        label = tk.Label(self, textvariable=testingStatusMessageDeltaf, font=("Helvetica", 38, 'bold'), wraplength=500,
                         justify="center")
        label.config(bg="grey25", fg="firebrick1")
        label.place(x=50, y=825)  # (x=50,y=60)

        label = tk.Label(self, textvariable=testingStatusMessageMeeco, font=("Helvetica", 38, 'bold'), wraplength=500,
                         justify="center")
        label.config(bg="grey25", fg="firebrick1")
        label.place(x=1520, y=825)  # (x=1220,y=60)

        self.configure(background="grey25")
        global start_timet
        start_timet = StringVar(value='0')
        start_timet.set(start_time.strftime("%I:%M %p"))

        global start_timeRec
        start_timeRec = StringVar(value='0')
        start_timeRec.set(start_time.strftime("%I:%M %p"))

        global start_dateRec
        start_dateRec = StringVar(value='0')
        start_dateRec.set(start_time.strftime("%-m/%-d/%y"))

        global directory
        directory = dir_TGView
        padx = 300
        pady = 120
        graphXfield = 10  # 110
        graphYfield = 80  # 125
        graphPad = 970  # 900

        # Setting up the main figure and canvas for the new, dark graph
        # f3 = plt.figure(figsize=(10.1,6), dpi=100, facecolor=(0.40,0.51,0.46))
        # darkH2O = f3.add_subplot(211, facecolor=(0.25,0.25,0.25))
        # darkO2 = f3.add_subplot(212, facecolor=(0.25,0.25,0.25))
        # f1 = plt.figure(figsize=(10.1,6), dpi=100, facecolor=(0.40,0.51,0.46))
        # a1 = f1.add_subplot(211,facecolor=(0.25,0.25,0.25)

        global canvas1
        # Oxygen DeltaF Graph
        canvas1 = FigureCanvasTkAgg(f1, self)
        canvas1.draw()
        canvas1.get_tk_widget().place(x=graphXfield, y=graphYfield)  # .place(x=graphXfield,y=graphYfield)

        # Moisture Tracer Graph
        canvas2 = FigureCanvasTkAgg(f2, self)
        canvas2.draw()
        canvas2.get_tk_widget().place(x=graphPad, y=graphYfield)  # .place(x=graphXfield+graphPad,y=graphYfield)

        def onpick3(event):
            global xdata, ydata, point, ind, line
            line = event.artist

            xdata, ydata = line.get_data()
            ind = event.ind
            point = np.array([xdata[ind], ydata[ind]]).T
            # print('on pick line:', point)

        f2.canvas.mpl_connect('pick_event', onpick3)

        #### REMOVED ON 2/24/21
        # toolbarFrame = Frame(master=self)
        # toolbarFrame.place(x=graphXfield,y=graphYfield)
        # toolbar = NavigationToolbar2Tk(canvas1,toolbarFrame)
        # toolbar.update()

        # toolbarFrame2 = Frame(master=self)
        # toolbarFrame2.place(x=graphXfield+graphPad-10,y=graphYfield)
        # toolbar2 = NavigationToolbar2Tk(canvas2,toolbarFrame2)
        # toolbar2.update()
        # canvas1.get_tk_widget().place(x=5+padx-20,y=50+pady)

        # toolbar = NavigationToolbar2Tk(canvas2,self)
        # toolbar.update()
        # canvas2._tkcanvas.grid(row=3,column=2)

        global stopTest_andshowStartPage

        def stopTest_andshowStartPage():
            controller.show_frame(StartPage)
            if 'o2Valuelist' in globals() or 'h2oValuelist' in globals():
                self.stop()

        padx = 630
        pady = 835

        # added the stop icon to be used in the Stop recording button
        stopIcon = ImageTk.PhotoImage(file=f"{root_path}/stop1.png", master=self)

        # Stop Recording Button => starts the stop() function
        self.button3 = tk.Button(self, text="Stop Recording Test", activebackground="firebrick1", image=stopIcon,
                                 compound="left", padx=30, bg="grey35", highlightbackground="firebrick1",
                                 highlightthickness=2, relief=FLAT, activeforeground="white", fg="White",
                                 font=('calibri', 32, 'bold'), borderwidth='1',
                                 command=stop_confirm)  # command=stopTest_andshowStartPage
        self.button3.place(width=930, height=95, x=970, y=pady)
        self.button3.image = stopIcon

        # added the settings icon to be used in the Equipment controls button
        settingsIcon = ImageTk.PhotoImage(file=f"{root_path}/settings.png", master=self)

        self.button1 = tk.Button(self, text="Equipment Controls", image=settingsIcon, compound="left", padx=35,
                                 activebackground="#2FA4FF", bg="grey35", highlightbackground="#2FA4FF",
                                 highlightthickness=2, relief=FLAT, activeforeground="white", fg="White",
                                 font=('calibri', 32, 'bold'), borderwidth='1', command=equipment_controls)
        # self.button1.place(width=500,height=95,x=450,y=pady)
        self.button1.place(width=930, height=95, x=20, y=pady)
        self.button1.image = settingsIcon

        global rec_bg
        rec_bg = "#1CCA3C"
        global label68
        label68 = tk.Label(self, text="RECORDING", bg=rec_bg, fg="white", width=113, height=2,
                           font=('Century Gothic', 18, 'bold'))
        label68.place(x=0, y=0)

        global label69
        label69 = tk.Label(self, bg=rec_bg, width=115, height=2, font=('Century Gothic', 18, 'bold'))
        label69.place(x=0, y=950)

        '''
        self.gambar = Image.open('qam_logo_transparent(200).png')
        self.imgSplash = ImageTk.PhotoImage(self.gambar)
        self.img = Label(self, image=self.imgSplash, bg="grey25")
        self.img.image = self.imgSplash
        self.img.place(x=875+padx, y=5+pady)
        '''

        ##### TESTING SCREEN DATA
        padx = 755
        pady = 685
        padyy = 715
        testingPadX = 200
        m = 0
        multiplier = 2.3
        # Start Time Display
        label13 = tk.Label(self, text="Start Time:", font=SMALL_FONT)
        label13.place(x=padx + testingPadX * m, y=pady)
        label13.config(bg="grey35", fg="white")

        label14 = tk.Label(self, textvariable=start_timet, bg="grey35", fg="#FFA500", font=('lato', 20, 'bold'))
        label14.place(x=5 + padx + testingPadX * m, y=padyy)

        # Start Date Display
        label13 = tk.Label(self, text="Start Date:", font=SMALL_FONT)
        label13.place(x=215 + padx + testingPadX * m, y=pady)
        label13.config(bg="grey35", fg="white")

        label14 = tk.Label(self, textvariable=start_dateRec, bg="grey35", fg="#FFA500", font=('lato', 20, 'bold'))
        label14.place(x=220 + padx + testingPadX * m, y=padyy)

        m += multiplier
        pady = 755
        padx = -75
        # # current o2
        # label13 = tk.Label(self, text="Current O2:", font=SMALL_FONT)
        # label13.place(x=padx + testingPadX * m + 10, y=pady)
        # label13.config(bg="grey35", fg="white")
        #
        # label14 = tk.Label(self, textvariable=currento2, bg="grey35", fg="#60D500", font=('lato', 20, 'bold'))
        # label14.place(x=165 + padx + testingPadX * m + 10, y=pady)
        # m += multiplier
        # m += 2.2
        # # current h2o
        # label13 = tk.Label(self, text="Current H2O:", font=SMALL_FONT)
        # label13.place(x=padx + testingPadX * m + 70, y=pady)
        # label13.config(bg="grey35", fg="white")
        #
        # label14 = tk.Label(self, textvariable=currenth2o, bg="grey35", fg="#2FA4FF", font=('lato', 20, 'bold'))
        # label14.place(x=200 + padx + testingPadX * m + 70, y=pady)

    def idle_on_off(self, start_stopper):
        if start_stopper == 'start':
            self.label15.configure(text="RECORDING", bg="orange")  # bg="#1CCA3C"
            self.label16.configure(bg="orange")  # "#1CCA3C"
        else:
            self.label15.configure(text="IDLE", bg="IndianRed")
            self.label16.configure(bg="IndianRed")

    def choose_directory(self):
        global directory
        directory = filedialog.askdirectory()

    ### Stop Recording Function: changes 'recording' to False. appends header.csv with stoptime and test info. rewrites filepath to match stoptime
    def stop(self):

        # self.button3.config(state=DISABLED)
        # self.button2.config(state=NORMAL)

        global a1, a2
        a1.cla()
        a2.cla()
        global h2odata_max, h2odata_min
        del h2odata_max
        del h2odata_min
        global o2data_max, o2data_min
        del o2data_max
        del o2data_min
        ## recording variable dictates whether analytical data is currently being written to .csv
        global recording
        recording = False

        global stop_time
        stop_time = datetime.now()
        global stop_timee
        stop_timee = stop_time.strftime("%H:%M  %m/%d/%y")
        global stop_timeet
        stop_timeet = stop_time.strftime("%m_%d_%y_%H.%M.%S")

        global time_elapsed
        time_elapsed = stop_time - start_time
        time_elapsed = time_elapsed_string(time_elapsed)

        if var2.get() != 'radH2O':
            global o2MeanValue
            o2MeanValue = str(round(mean(o2Valuelist), 1))
            global o2MeanValueVar
            o2MeanValueVar = StringVar(value=o2MeanValue)
            global o2MaxValue
            o2MaxValue = str(max(o2Valuelist))
            global o2MaxValueVar
            o2MaxValueVar = StringVar(value=o2MaxValue)
            global o2FinalValue
            o2FinalValue = str(o2Valuelist[-1])
            global o2FinalValueVar
            o2FinalValueVar = StringVar(value=o2FinalValue)

        if var2.get() != 'radO2':
            global h2oMeanValue
            h2oMeanValue = str(round(mean(h2oValuelist), 1))
            global h2oMeanValueVar
            h2oMeanValueVar = StringVar(value=h2oMeanValue)
            global h2oMaxValue
            h2oMaxValue = str(max(h2oValuelist))
            global h2oMaxValueVar
            h2oMaxValueVar = StringVar(value=h2oMaxValue)
            global h2oFinalValue
            h2oFinalValue = str(h2oValuelist[-1])
            global h2oFinalValueVar
            h2oFinalValueVar = StringVar(value=h2oFinalValue)

        global path
        directory = dir_TGView
        path = directory + '/' + str(header_list[3]) + "_" + str(header_list[4]) + "_" + str(
            header_list[2]) + "_" + str(header_list[0]) + "_" + start_timee
        global pathF
        os.rename(pathF, path)
        pathF = path
        self.headerFileTitle = "Header"
        # path = directory + '/' + str(title.get())
        with open(os.path.join(pathF, self.headerFileTitle) + '.csv', 'a', newline='') as c:
            writer3 = csv.writer(c)
            writer3.writerow([stop_time])
            if var2.get() != 'radH2O':
                writer3.writerow([o2MeanValue])
                writer3.writerow([o2MaxValue])
                writer3.writerow([o2FinalValue])
            if var2.get() != 'radO2':
                writer3.writerow([h2oMeanValue])
                writer3.writerow([h2oMaxValue])
                writer3.writerow([h2oFinalValue])
            c.close()

        with open(f'{root_path}/Header_default.csv', 'w+', newline='') as d:
            writer4 = csv.writer(d)
            for row in header_list:
                writer4.writerow([row])
            d.close()
        # if o2test_passing == True and h2otest_passing == True:
        #        pathG = os.path.join(os.path.dirname(pathF),"P_"+os.path.basename(pathF))
        # else:
        #        pathG = os.path.join(os.path.dirname(pathF),"F_"+os.path.basename(pathF))
        # os.rename(pathF,pathG)
        # pathF = pathG
        confirm_fields(start_stop='stop')


#### STOP CONFIRMATION WINDOW
def stop_confirm():
    params = {
        "text_yes": "Are you sure you want to stop the test?",
        "title": "Please Confirm",
        "command_yes": stopTest_andshowStartPage
    }

    confirm_window = PopupWindow(params)


#### DELETE CONFIRMATION WINDOW
def delete_confirm():
    params = {
        "text_yes": "Are you sure you want to delete this report?\n(This will delete the folder and all testing data)",
        "title": "Please Confirm",
        "command_yes": delete_test
    }

    confirm_delete = PopupWindow(params)

    # confirmFont = "lato"
    #
    # paddx = 15
    # paddy = 15
    # global top46
    # top46 = Toplevel()
    # # topA.attributes('-type', 'Dock')
    # top46.title("Please Confirm")
    # top46.configure(background="grey25")
    # # Width and height for the Tk root window
    # w = 720
    # h = 465
    # # This gets the current screen width and height
    # ws = top46.winfo_screenwidth()
    # hs = top46.winfo_screenheight()
    # # Calculate the x and y coordinates based on the current screen size
    # sx = (ws / 2) - (w / 2)
    # sy = (hs / 2) - (h / 2)
    # # Open the root window in the middle of the screen
    # # topA.overrideredirect(True)
    # top46.geometry('%dx%d+%d+%d' % (w, h, sx, sy))
    # paddy = 5
    #
    # ##### Ask the question
    # label4 = tk.Label(top46, text="Are you sure you want to delete this report?", bg="grey25", fg='white',
    #                   font=(confirmFont, 40, 'bold'), wraplength=550)
    # label4.place(relx=.5, rely=.27, anchor="center")
    #
    # ##### equipment controls title
    # label1 = tk.Label(top46, text="(This will delete the folder and all testing data)", bg="grey25", fg='orange',
    #                   font=(confirmFont, 17, 'bold'))
    # label1.place(relx=.5, rely=.52, anchor="center")
    #
    # # label2 = tk.Label(top45, text=version_num,bg="grey25", fg = "white", font=(confirmFont,40,'bold'))
    # # label2.place(relx=.5, rely=.56, anchor="center")
    #
    # ## Button image
    # # likeIcon = ImageTk.PhotoImage(file = r"./like.png", master=top45)
    #
    # # YES button
    # button1 = tk.Button(top46, text="Yes", compound="left", padx=30, activebackground="#678277", bg="grey35",
    #                     highlightbackground="#678277", highlightthickness=2, relief="flat", activeforeground="white",
    #                     fg="White", font=(confirmFont, 37, 'bold'), borderwidth='1', command=delete_test)
    # button1.place(width=270, height=95, relx=.3, rely=.77, anchor="center")
    #
    # # NO button
    # button2 = tk.Button(top46, text="No", compound="left", padx=30, activebackground="IndianRed", bg="grey35",
    #                     highlightbackground="IndianRed", highlightthickness=2, relief="flat", activeforeground="white",
    #                     fg="White", font=(confirmFont, 37, 'bold'), borderwidth='1', command=top46.destroy)
    # button2.place(width=270, height=95, relx=.7, rely=.77, anchor="center")


def confirm_fields(start_stop):
    global startt_stopp
    startt_stopp = start_stop
    top4 = Toplevel()
    top4.title("Test Parameters")
    # Width and height for the Tk root window
    w = 1460
    h = 1000
    # This gets the current screen width and height
    ws = top4.winfo_screenwidth()
    hs = top4.winfo_screenheight()
    # Calculate the x and y coordinates based on the current screen size
    sx = (ws / 2) - (w / 2)
    sy = (hs / 2) - (h / 2)
    # Open the root window in the middle of the screen
    top4.geometry('%dx%d+%d+%d' % (w, h, sx, sy))

    if start_stop == 'start':
        label1 = tk.Label(top4, text="Enter Test Parameters", font=LARGEST_FONT)
        label1.place(x=210, y=30)
        label1.config(bg="grey25", fg=QAM_GREEN)
    if start_stop == 'stop' or start_stop == 'manage':
        label1 = tk.Label(top4, text="Verify Report Information", font=LARGEST_FONT)
        label1.place(x=110, y=10)
        label1.config(bg="grey25", fg=QAM_GREEN)
    # fg="#7fa6a3"

    top4.configure(background="grey25")

    global pathF

    # --------------------------------------------------------------------------------#
    #                                  COMMANDS                                      #
    # --------------------------------------------------------------------------------#

    # --------------------------------------#
    #    Start Recording Test Button       #
    # --------------------------------------#
    def record(self=top4):

        global recording
        red_green = 'green'
        on_off = "Recording"

        global start_time
        start_time = datetime.now()
        global start_timee
        start_timee = start_time.strftime("%m_%d_%y_%H.%M.%S")
        global start_timea
        start_timea = start_time.strftime("%H:%M  %m/%d/%y")

        global start_timet
        # start_timet.set(start_time.strftime("%I:%M %p  %-m/%-d/%y"))
        start_timet.set(start_time.strftime("%I:%M %p"))

        ##### global variable resets #######
        global o2_dataList
        global h2o_dataList
        global a1, a2
        global cycleO2, cycleH2O
        global h2odata_max, h2odata_min
        del h2odata_max
        del h2odata_min
        global o2data_max, o2data_min
        del o2data_max
        del o2data_min
        cycleH2O = 14
        cycleO2 = 14
        o2_dataList = ''
        h2o_dataList = ''
        a1.cla()
        a2.cla()

        headerFileTitle = "Header"
        path = directory + '/' + str(building.get()) + "_" + str(tool_id.get()) + "_" + str(location.get()) + "_" + str(
            title.get()) + "_" + start_timee
        i = 0

        os.mkdir(path)
        global pathF
        pathF = str(path)

        header_list[0] = title.get()
        header_list[1] = client.get()
        header_list[2] = location.get()
        header_list[3] = building.get()
        header_list[4] = tool_id.get()
        header_list[5] = test_gas.get()
        header_list[6] = source_gas.get()
        header_list[7] = technician.get()
        header_list[8] = system_flow.get()
        header_list[9] = retreive_input(top4.textbox5)
        top4.textbox5.insert(INSERT, header_list[9])
        header_list[10] = deltaf_serial.get()
        header_list[11] = deltaf_cal.get()
        header_list[12] = deltaf_flow.get()
        header_list[13] = deltaf_spec.get()
        header_list[14] = tracer_serial.get()
        header_list[15] = tracer_cal.get()
        header_list[16] = tracer_flow.get()
        header_list[17] = tracer_spec.get()

        with open(os.path.join(path, headerFileTitle) + '.csv', 'w+', newline='') as c:
            writer3 = csv.writer(c)
            for row in header_list:
                writer3.writerow([row])
            writer3.writerow([start_time])
            c.flush()

        with open(f'{root_path}/Header_default.csv', 'w+', newline='') as d:
            writer4 = csv.writer(d)
            for row in header_list:
                writer4.writerow([row])
            d.close()

        top4.destroy()

        recording = True
        # --------------------------------------#
        #           Delete Test Button         #
        # --------------------------------------#

    ### deletes test results (entire folder tree)
    global delete_test

    def delete_test():

        ### Global Variable Resets ###
        # Graph clear#
        global a1, a2
        a1.clear()
        a2.clear()

        # Min / Max data clear#
        try:
            global h2odata_max, h2odata_min
            del h2odata_max
            del h2odata_min
            global o2data_max, o2data_min
            del o2data_max
            del o2data_min
        except NameError as e:
            print(e)
            pass

        # plot the next data grab#
        global cycleO2, cycleH2O
        cycleH2O = 14
        cycleO2 = 14

        # graph data reset#
        global o2_dataList, h2o_dataList
        o2_dataList = ''
        h2o_dataList = ''

        # start time reset#
        global start_time
        start_time = datetime.now()

        # delete entire test folder#
        if start_stop == 'start' or start_stop == 'stop':
            global pathF
            shutil.rmtree(pathF)  # "pathF" path is created from new test

        elif start_stop == 'manage':
            ### variable resets ###
            try:
                global newStartTime
                del newStartTime
                print("deleted newStartTime")
            except:
                print("no newStartTime to delete")
                pass
            try:
                global oldStartTimeRH2O
                del oldStartTimeRH2O
                print("deleted oldStartTimeRH2O")
            except:
                print("no oldStartTimeRH2O to delete")
                pass
            try:
                global newStopTime
                del newStopTime
            except:
                print("no newStartTime to delete")
                pass
            try:
                global oldStopTimeRH2O
                del oldStopTimeRH2O
                print("deleted oldStopTimeRH2O")
            except:
                print("no newStartTime to delete")
                pass
            try:
                global newStartTimeO2
                del newStartTimeO2
                print("deleted newStartTimeO2")
            except:
                print("no newStartTimeO2 to delete")
                pass

            try:
                global oldStartTimeO2
                del oldStartTimeO2
                print("deleted oldStartTimeO2")
            except:
                print("no oldStartTimeO2 to delete")
                pass
            try:
                global newStopTimeO2
                del newStopTimeO2
                print("deleted newStopTimeO2")
            except:
                print("no newStopTimeO2 to delete")
                pass

            try:
                global oldStopTimeO2
                del oldStopTimeO2
                print("deleted oldStopTimeO2")
            except:
                print("no oldStopTimeO2 to delete")
                pass
            try:
                global o2bAvgEdit
                del o2bAvgEdit
                print("deleted o2bAvgEdit")
            except:
                print("no o2bAvgEdit to delete")
                pass
            try:
                global o2bAvgUnedit
                del o2bAvgUnedit
                print("deleted o2bAvgUnedit")
            except:
                print("no o2bAvgUnedit to delete")
                pass
            try:
                global o2bMaxEdit
                del o2bMaxEdit
                print("deleted o2bMaxEdit")
            except:
                print("no o2bMaxEdit to delete")
                pass
            try:
                global o2bMaxUnedit
                del o2bMaxUnedit
                print("deleted o2bMaxUnedit")
            except:
                print("no o2bMaxUnedit to delete")
                pass
            try:
                global o2bFinalEdit
                del o2bFinalEdit
                print("deleted o2bFinalEdit")
            except:
                print("no o2bFinalEdit to delete")
                pass
            try:
                global o2bFinalUnedit
                del o2bFinalUnedit
                print("deleted o2bFinalUnedit")
            except:
                print("no newStartTime to delete")
                pass
            try:
                global h2obAvgEdit
                del h2obAvgEdit
                print("deleted h2obAvgEdit")
            except:
                print("no h2obAvgEdit to delete")
                pass
            try:
                global h2obAvgUnedit
                del h2obAvgUnedit
                print("deleted h2obAvgUnedit")
            except:
                print("no h2obAvgUnedit to delete")
                pass
            try:
                global h2obFinalEdit
                del h2obFinalEdit
                print("deleted h2obFinalEdit")
            except:
                print("no h2obFinalEdit to delete")
                pass
            try:
                global h2obFinalUnedit
                del h2obFinalUnedit
                print("deleted h2obFinalUnedit")
            except:
                print("no h2obFinalUnedit to delete")
                pass
            shutil.rmtree(folder)  # "folder" path is selected by user
            top.destroy()

        top46.destroy()
        top4.destroy()
        '''                             ### possible "are you sure" window for delete test button ####
            result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
            if result == 'yes':

                shutil.rmtree(pathF)
                top4.destroy()
            else:
                top4.destroy()
            '''

        # --------------------------------------#
        #       Generate PDF Button            #
        # --------------------------------------#

    def update_and_generatePDF():

        # update header.csv with textboxes in confirm_fields()#
        update_fields()

        # generate PDF from selected header.csv, o2.csv, and/or h2o.csv#
        generatePDF()

        # graph data reset#
        global o2_dataList, h2o_dataList
        o2_dataList = ''
        h2o_dataList = ''

        # start time reset#
        global start_time
        start_time = datetime.now()

        # plot the next data grab#
        global cycleO2, cycleH2O
        cycleH2O = 14
        cycleO2 = 14

        # --------------------------------------#
        #       Updates header.csv             #
        # --------------------------------------#

    def update_fields():

        i = 0

        os.chdir(dir_TGView)

        #### get new header_list from fields in confirm_fields
        global header_list
        header_list = []
        header_list.append(title.get())
        header_list.append(client.get())
        header_list.append(location.get())
        header_list.append(building.get())
        header_list.append(tool_id.get())
        header_list.append(test_gas.get())
        header_list.append(source_gas.get())
        header_list.append(technician.get())
        header_list.append(system_flow.get())
        if start_stop == 'start':
            header_list.append(comments.get())
        if start_stop == 'stop' or start_stop == 'manage':
            if top4.comments.get() == '':
                top4.textbox5.insert(INSERT, top4.comments.get())
            comments = retreive_input(top4.textbox5)
            header_list.append(comments)
        header_list.append(deltaf_serial.get())
        header_list.append(deltaf_cal.get())
        header_list.append(deltaf_flow.get())
        header_list.append(deltaf_spec.get())
        header_list.append(tracer_serial.get())
        header_list.append(tracer_cal.get())
        header_list.append(tracer_flow.get())
        header_list.append(tracer_spec.get())

        global path
        directory = dir_TGView
        if start_stop == 'stop':
            path = directory + '/' + str(header_list[3]) + "_" + str(header_list[4]) + "_" + str(
                header_list[2]) + "_" + str(header_list[0]) + "_" + start_timee
            global pathF
            os.rename(pathF, path)
            pathF = path

        if start_stop == 'manage':
            pathF = folder

        ### adjust Header_default with new field names
        with open(f'{root_path}/Header_default.csv', 'w+', newline='') as d:
            writer4 = csv.writer(d)
            for row in header_list:
                writer4.writerow([row])
            d.close()

        ### adjust newly created header file with new field names (overwrites old header file)
        with open(os.path.join(pathF, 'Header.csv'), 'w+', newline='') as c:
            writer3 = csv.writer(c)
            for row in header_list:
                writer3.writerow([row])
            if start_stop == 'manage':
                if H2OcsvFound == True and O2csvFound == False:
                    try:
                        newStartTime
                    except:
                        newStartTime = oldStartTimeRH2O
                    writer3.writerow([newStartTime])
                    try:
                        newStopTime
                    except:
                        newStopTime = oldStopTimeRH2O
                    writer3.writerow([newStopTime])
                elif H2OcsvFound == False and O2csvFound == True:
                    try:
                        newStartTimeO2
                    except:
                        newStartTimeO2 = oldStartTimeRO2
                    writer3.writerow([newStartTimeO2])
                    try:
                        newStopTimeO2
                    except:
                        newStopTimeO2 = oldStopTimeRO2
                    writer3.writerow([newStopTimeO2])
                elif H2OcsvFound == True and H2OcsvFound == True:
                    try:
                        newStartTime
                    except:
                        newStartTime = min(oldStartTimeRO2, oldStartTimeRH2O)
                    writer3.writerow([newStartTime])
                    try:
                        newStopTime
                    except:
                        newStopTime = min(oldStopTimeRO2, oldStopTimeRH2O)
                    writer3.writerow([newStopTime])

                if H2OcsvFound == True and O2csvFound == True:
                    try:
                        o2bAvgEdit
                    except:
                        o2bAvgEdit = o2bAvgUnedit
                    writer3.writerow([o2bAvgEdit])
                    try:
                        o2bMaxEdit
                    except:
                        o2bMaxEdit = o2bMaxUnedit
                    writer3.writerow([o2bMaxEdit])
                    try:
                        o2bFinalEdit
                    except:
                        o2bFinalEdit = o2bFinalUnedit
                    writer3.writerow([o2bFinalEdit])
                    try:
                        h2obAvgEdit
                    except:
                        h2obAvgEdit = h2obAvgUnedit
                    writer3.writerow([h2obAvgEdit])
                    try:
                        h2obMaxEdit
                    except:
                        h2obMaxEdit = h2obMaxUnedit
                    writer3.writerow([h2obMaxEdit])
                    try:
                        h2obFinalEdit
                    except:
                        h2obFinalEdit = h2obFinalUnedit
                    writer3.writerow([h2obFinalEdit])
                elif H2OcsvFound == True and O2csvFound == False:
                    try:
                        h2obAvgEdit
                    except:
                        h2obAvgEdit = h2obAvgUnedit
                    writer3.writerow([h2obAvgEdit])
                    try:
                        h2obMaxEdit
                    except:
                        h2obMaxEdit = h2obMaxUnedit
                    writer3.writerow([h2obMaxEdit])
                    try:
                        h2obFinalEdit
                    except:
                        h2obFinalEdit = h2obFinalUnedit
                    writer3.writerow([h2obFinalEdit])
                elif H2OcsvFound == False and O2csvFound == True:
                    try:
                        o2bAvgEdit
                    except:
                        o2bAvgEdit = o2bAvgUnedit
                    writer3.writerow([o2bAvgEdit])
                    try:
                        o2bMaxEdit
                    except:
                        o2bMaxEdit = o2bMaxUnedit
                    writer3.writerow([o2bMaxEdit])
                    try:
                        o2bFinalEdit
                    except:
                        o2bFinalEdit = o2bFinalUnedit
                    writer3.writerow([o2bFinalEdit])

            if start_stop == 'stop':
                writer3.writerow([start_time])
                writer3.writerow([stop_time])
                if var2.get() != 'radH2O':
                    writer3.writerow([o2MeanValue])
                    writer3.writerow([o2MaxValue])
                    writer3.writerow([o2FinalValue])
                if var2.get() != 'radO2':
                    writer3.writerow([h2oMeanValue])
                    writer3.writerow([h2oMaxValue])
                    writer3.writerow([h2oFinalValue])
            c.flush()
            c.close()

            # --------------------------------------#
            # Threads Progressbar with PDFexport   #
            # --------------------------------------#

    def generatePDF():

        s1 = ttk.Style()
        # s1.theme_use('clam')
        TROUGH_COLOR = 'grey85'
        BAR_COLOR = '#209736'
        s1.configure('red.Horizontal.TProgressbar', troughcolor=TROUGH_COLOR, bordercolor=TROUGH_COLOR,
                     background=BAR_COLOR, lightcolor=BAR_COLOR, darkcolor=BAR_COLOR)
        global progress
        progress = Progressbar(top4, style='red.Horizontal.TProgressbar', orient=HORIZONTAL, length=1420,
                               mode='determinate', maximum=100, value=5)
        progress.place(x=20, y=870, height=105)

        def bar():
            progress['value'] = 10
            top4.update_idletasks()
            time.sleep(0.4)
            # 0.4
            progress['value'] = 20
            top4.update_idletasks()
            time.sleep(0.4)
            # 2.9
            progress['value'] = 30
            top4.update_idletasks()
            time.sleep(0.4)
            # 0.2
            progress['value'] = 40
            top4.update_idletasks()
            time.sleep(0.4)
            # 2.2
            progress['value'] = 50
            top4.update_idletasks()
            time.sleep(0.4)
            # 0.2
            progress['value'] = 60
            top4.update_idletasks()
            if start_stop == 'start' or start_stop == 'stop':
                if var2.get() == 'radBoth':
                    exportBoth(startscreen=False)
                elif var2.get() == 'radO2':
                    exportO2(startscreen=False)
                elif var2.get() == 'radH2O':
                    exportH2O(startscreen=False)
            if start_stop == 'manage':
                if O2csvFound == True and H2OcsvFound == True:
                    exportBoth(startscreen=True)
                elif O2csvFound == False and H2OcsvFound == True:
                    exportH2O(startscreen=True)
                elif O2csvFound == True and H2OcsvFound == False:
                    exportO2(startscreen=True)
            progress['value'] = 70
            top4.update_idletasks()
            time.sleep(0.1)
            progress['value'] = 80
            top4.update_idletasks()
            time.sleep(0.1)
            progress['value'] = 90
            top4.update_idletasks()
            time.sleep(0.1)
            progress['value'] = 100
            top4.update_idletasks()
            time.sleep(0.1)

        bar()

        top4.destroy()

    ### BUTTONS ###
    xfield = 400
    yfield = -45
    paddx = 195
    paddy = 80
    i = 8

    ###### Non-Radio Buttons
    # if start_stop=='start':
    #    button1 = tk.Button(top4, text="Save Changes", font=LARGE_FONT, fg="white", activeforeground="white", bg="#678176", activebackground="#81a6a3", padx=25, command=top4.destroy)
    #    button1.place(x=5,y=5)
    if start_stop == 'stop' or start_stop == 'manage':
        # BUTTON ICON
        reportIcon = ImageTk.PhotoImage(file=f"{root_path}/report.png", master=top4)

        button2 = tk.Button(top4, text="Generate PDF Report", image=reportIcon, compound="left", padx=35,
                            font=LARGE_FONT, bg="grey35", activebackground="orange", fg="White",
                            activeforeground="white", highlightbackground="orange", highlightthickness=2, relief=FLAT,
                            command=update_and_generatePDF)
        button2.place(width=515, height=105, x=205, y=870)
        button2.image = reportIcon

        # button4 = tk.Button(top4, text="Generate Failed Report",bg="grey15",fg="grey75",font=LARGE_FONT, command=update_and_generateFailedPDF)
        # button4.place(x=5,y=65)

        deleteIcon = ImageTk.PhotoImage(file=f"{root_path}/delete.png", master=top4)

        button3 = tk.Button(top4, text="Delete This Report", image=deleteIcon, compound="left", padx=50, bg="grey35",
                            activebackground="firebrick1", fg="White", activeforeground="white",
                            highlightbackground="firebrick1", highlightthickness=2, relief=FLAT, font=LARGE_FONT,
                            command=delete_confirm)
        button3.place(width=515, height=105, x=745, y=870)
        button3.image = deleteIcon

    if start_stop == 'start':
        startIcon = ImageTk.PhotoImage(file=f"{root_path}/confirm1.png", master=top4)

        button3 = tk.Button(top4, text="Start Recording", image=startIcon, compound="left", padx=40, bg="grey35",
                            activebackground="#1CCA3C", fg="White", activeforeground="white",
                            highlightbackground="#1CCA3C", highlightthickness=2, relief=FLAT, font=LARGER_FONT,
                            command=record)
        # button3.place(x=1300,y=895)
        button3.place(height=200, width=655, x=xfield + paddx, y=50 + paddy * i)
        button3.image = startIcon

    global header_list
    if start_stop == 'start' or start_stop == 'stop':
        with open(f'{root_path}/Header_default.csv', newline='') as t:
            headreader = csv.reader(t)
            header_list = []
            for row in headreader:
                header_list.append(row[0])
    else:
        with open(dualHeaderPath, newline='') as t:
            headreader = csv.reader(t)
            header_list = []
            for row in headreader:
                header_list.append(row[0])
    xfield = 400
    yfield = -45
    paddx = 200
    paddy = 80
    if start_stop == 'stop' or start_stop == 'manage':
        Ly = 50
        Ty = 85
    if start_stop == 'start':
        Ly = 100
        Ty = 135
    i = 1

    ####Document fields (title, client, etc)
    # client entry    header_list[1]
    label4 = tk.Label(top4, text="Client:", font=SMALL_FONT)
    label4.place(x=15 + paddx, y=Ly + paddy * i)
    label4.config(bg="grey25", fg="white")

    global client
    top4.client = StringVar(top4, value=header_list[1])
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.client, font=SMALLER_FONT)
    top4.textbox.place(x=15 + paddx, y=Ty + paddy * i)
    reg = top4.register(validate_input)
    top4.textbox.config(validate='key', validatecommand=(reg, '%P'))
    client = top4.client
    i = i + 1

    # facility entry   (header_list[3] = building)
    label4 = tk.Label(top4, text="Facility:", font=SMALL_FONT)
    label4.place(x=15 + paddx, y=Ly + paddy * i)
    label4.config(bg="grey25", fg="white")

    global building
    top4.building = StringVar(top4, value=header_list[3])
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.building, font=SMALLER_FONT)
    top4.textbox.place(x=15 + paddx, y=Ty + paddy * i)
    reg = top4.register(limit_character)
    top4.textbox.config(validate='key', validatecommand=(reg, '%P'))
    building = top4.building
    i = i + 1

    # tool_id entry
    label4 = tk.Label(top4, text="Tool ID / Equipment:", font=SMALL_FONT)
    label4.place(x=15 + paddx, y=Ly + paddy * i)
    label4.config(bg="grey25", fg="white")

    global tool_id
    if start_stop == 'stop' or start_stop == 'manage':
        top4.tool_id = StringVar(top4, value=header_list[4])
    if start_stop == 'start':
        top4.tool_id = StringVar(top4)
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.tool_id, font=SMALLER_FONT)
    top4.textbox.place(x=15 + paddx, y=Ty + paddy * i)
    reg = top4.register(validate_input)
    top4.textbox.config(validate='key', validatecommand=(reg, '%P'))
    tool_id = top4.tool_id
    i = i + 1

    # system entry   (header_list[2] = 'location' = SYSTEM)
    label4 = tk.Label(top4, text="System:", font=SMALL_FONT)
    label4.place(x=15 + paddx, y=Ly + paddy * i)
    label4.config(bg="grey25", fg="white")

    global location
    if start_stop == 'stop' or start_stop == 'manage':
        top4.location = StringVar(top4, value=header_list[2])
    if start_stop == 'start':
        top4.location = StringVar(top4)
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.location, font=SMALLER_FONT)
    top4.textbox.place(x=15 + paddx, y=Ty + paddy * i)
    reg = top4.register(limit_character)
    top4.textbox.config(validate='key', validatecommand=(reg, '%P'))
    location = top4.location
    i = i + 1

    # source ID entry      variable = source_gas
    label6 = tk.Label(top4, text="Source ID:", font=SMALL_FONT)
    label6.place(x=15 + paddx, y=Ly + paddy * i)
    label6.config(bg="grey25", fg="white")

    global source_gas
    if start_stop == 'stop' or start_stop == 'manage':
        top4.source_gas = StringVar(top4, value=header_list[6])
    if start_stop == 'start':
        top4.source_gas = StringVar(top4)
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.source_gas, font=SMALLER_FONT)
    top4.textbox.place(x=15 + paddx, y=Ty + paddy * i)
    reg = top4.register(limit_character)
    top4.textbox.config(validate='key', validatecommand=(reg, '%P'))
    source_gas = top4.source_gas
    i = i + 1

    # Test Point ID entry      variable = title
    label3 = tk.Label(top4, text="Test Point ID:", font=SMALL_FONT)
    label3.place(x=15 + paddx, y=Ly + paddy * i)
    label3.config(bg="grey25", fg="white")

    global title
    if start_stop == 'stop' or start_stop == 'manage':
        top4.title = StringVar(top4, value=header_list[0])
    if start_stop == 'start':
        top4.title = StringVar(top4)

    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.title, font=SMALLER_FONT)
    top4.textbox.place(x=15 + paddx, y=Ty + paddy * i)
    reg = top4.register(validate_input)
    top4.textbox.config(validate='key', validatecommand=(reg, '%P'))
    title = top4.title
    i = i + 1

    # test gas entry
    label5 = tk.Label(top4, text="Test Gas:", font=SMALL_FONT)
    label5.place(x=15 + paddx, y=Ly + paddy * i)
    label5.config(bg="grey25", fg="white")

    global test_gas
    if start_stop == 'start':
        top4.test_gas = StringVar(top4)
    if start_stop == 'stop' or start_stop == 'manage':
        top4.test_gas = StringVar(top4)
        top4.test_gas.set(header_list[5])  # sets default dropdown to header_default
    w = OptionMenu(top4, top4.test_gas, 'Nitrogen', 'Argon', 'Hydrogen', 'Oxygen', 'Helium', 'CDA',
                   'Other')  # list of test_gas dropdown options
    w.config(font=SMALLER_FONT, width=17)
    menu = top4.nametowidget(w.menuname)
    menu.config(font=SMALLER_FONT)
    w.place(x=15 + paddx, y=Ty + paddy * i)
    test_gas = top4.test_gas
    i = i + 1

    # technician entry
    label7 = tk.Label(top4, text="Technician:", font=SMALL_FONT)
    label7.place(x=15 + paddx, y=Ly + paddy * i)
    label7.config(bg="grey25", fg="white")

    global technician
    if start_stop == 'stop' or start_stop == 'manage':
        top4.technician = StringVar(top4, value=header_list[7])
    if start_stop == 'start':
        top4.technician = StringVar(top4)
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.technician, font=SMALLER_FONT)
    top4.textbox.place(x=15 + paddx, y=Ty + paddy * i)
    reg = top4.register(limit_character)
    top4.textbox.config(validate='key', validatecommand=(reg, '%P'))
    technician = top4.technician
    i = i + 1

    # test flow entry
    label8 = tk.Label(top4, text="Test Flow Rate (SCFH):", font=SMALL_FONT)
    label8.place(x=15 + paddx, y=Ly + paddy * i)
    label8.config(bg="grey25", fg="white")

    top4.system_flow = StringVar(top4, value=header_list[8])
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.system_flow, font=SMALLER_FONT)
    top4.textbox.place(x=15 + paddx, y=Ty + paddy * i)
    system_flow = top4.system_flow
    i = i + 1

    # comments entry
    i = 6

    label9 = tk.Label(top4, text="Comments:", font=SMALL_FONT)
    # COMMENTED OUT 10/8/2020
    # label9.place(x=15+paddx,y=52+paddy*i)
    label9.place(x=xfield + paddx, y=Ly + paddy * i)
    label9.config(bg="grey25", fg="white")

    global comments

    top4.textbox5 = Text(top4, width=20, height=4, wrap='word', font=SMALLER_FONT)
    if start_stop == 'stop' or start_stop == 'manage':
        top4.comments = StringVar(top4, value=header_list[9])
        top4.textbox5.insert(INSERT, top4.comments.get())
    if start_stop == 'start':
        top4.comments = StringVar(top4)
        top4.textbox5.insert(INSERT, top4.comments.get())
    # COMMENTED OUT 10/8/2020
    # top4.textbox5.place(x=15+paddx,y=90+paddy*i, height=85,width=700)
    top4.textbox5.place(x=xfield + paddx, y=Ty + paddy * i, height=35,
                        width=650)  ##adjusted height 10/16/20 for new layout

    # comments = retreive_input(top4.textbox5)
    comments = top4.comments

    ### analyser info entries
    ## delta f info entry
    # deltaf serial number entry
    i = 0
    xfield = 400
    yfield = -45

    if start_stop == 'stop' or start_stop == 'manage':  ##adjusted 10/16/20 for new layout
        # Label Y value
        Ly = 170
        # Textbox Y value
        Ty = 205
    elif start_stop == 'start':
        # Label Y value
        Ly = 220
        # Textbox Y value
        Ty = 255

    label10 = tk.Label(top4, text="Oxygen Analyzer:", font=SMALL_FONT)
    label10.place(x=xfield + paddx, y=Ly + paddy * i + yfield)
    label10.config(bg="grey25", fg="white")

    top4.deltaf_name = StringVar(top4, value="Servomex")
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.deltaf_name, font=SMALLER_FONT, state='readonly')
    top4.textbox.place(x=xfield + paddx, y=Ty + paddy * i + yfield)
    i = i + 1

    label10 = tk.Label(top4, text="Serial Number:", font=SMALL_FONT)
    label10.place(x=xfield + paddx, y=Ly + paddy * i + yfield)
    label10.config(bg="grey25", fg="white")

    global deltaf_serial
    top4.deltaf_serial = StringVar(top4, value=header_list[10])
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.deltaf_serial, font=SMALLER_FONT)
    top4.textbox.place(x=xfield + paddx, y=Ty + paddy * i + yfield)
    deltaf_serial = top4.deltaf_serial
    i = i + 1

    # deltaf calibration date entry
    label11 = tk.Label(top4, text="Calibration Due:", font=SMALL_FONT)
    label11.place(x=xfield + paddx, y=Ly + paddy * i + yfield)
    label11.config(bg="grey25", fg="white")

    global deltaf_cal
    top4.deltaf_cal = StringVar(top4, value=header_list[11])
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.deltaf_cal, font=SMALLER_FONT)
    top4.textbox.place(x=xfield + paddx, y=Ty + paddy * i + yfield)
    deltaf_cal = top4.deltaf_cal
    i = i + 1

    '''
        top4.deltaflow_units = StringVar(top4)
        top4.deltaflow_units.set('scfh') #sets default dropdown to header_default
        x = OptionMenu(top4, top4.deltaflow_units, 'slpm', 'scfh', 'sccm')       #list of test_gas dropdown options
        x.config(font=SMALLERR_FONT)
        menu = top4.nametowidget(w.menuname)
        menu.config(font=SMALLERR_FONT)
        x.place(x=xfield+paddx+220,y=208+paddy*i+yfield)
        deltaflow_units = top4.deltaflow_units
        '''
    # instrument flow entry
    label12 = tk.Label(top4, text="Flow Rate (SCFH):", font=SMALL_FONT)
    label12.place(x=xfield + paddx, y=Ly + paddy * i + yfield)
    label12.config(bg="grey25", fg="white")

    top4.deltaf_flow = StringVar(top4, value=header_list[12])
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.deltaf_flow, font=SMALLER_FONT)
    top4.textbox.place(x=xfield + paddx, y=Ty + paddy * i + yfield)
    deltaf_flow = top4.deltaf_flow
    i = i + 1

    # instrument specification
    label13 = tk.Label(top4, text="Specification (PPB):", font=SMALL_FONT)
    label13.place(x=xfield + paddx, y=Ly + paddy * i + yfield)
    label13.config(bg="grey25", fg="white")

    global deltaf_spec
    top4.deltaf_spec = StringVar(top4, value=header_list[13])
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.deltaf_spec, font=SMALLER_FONT)
    top4.textbox.place(x=xfield + paddx, y=Ty + paddy * i + yfield)
    deltaf_spec = top4.deltaf_spec

    ## tracer2 info entry
    # tracer2 serial number entry
    i = 0
    xfield = 770
    label10 = tk.Label(top4, text="Moisture Analyzer:", font=SMALL_FONT)
    label10.place(x=xfield + paddx, y=Ly + paddy * i + yfield)
    label10.config(bg="grey25", fg="white")

    top4.meeco_name = StringVar(top4, value="Tracer 2")
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.meeco_name, font=SMALLER_FONT, state='readonly')
    top4.textbox.place(x=xfield + paddx, y=Ty + paddy * i + yfield)
    i = i + 1

    label10 = tk.Label(top4, text="Serial Number:", font=SMALL_FONT)
    label10.place(x=xfield + paddx, y=Ly + paddy * i + yfield)
    label10.config(bg="grey25", fg="white")

    global tracer_serial
    top4.tracer_serial = StringVar(top4, value=header_list[14])
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.tracer_serial, font=SMALLER_FONT)
    top4.textbox.place(x=xfield + paddx, y=Ty + paddy * i + yfield)
    tracer_serial = top4.tracer_serial
    i = i + 1

    # tracer2 calibration date entry
    label11 = tk.Label(top4, text="Calibration Due:", font=SMALL_FONT)
    label11.place(x=xfield + paddx, y=Ly + paddy * i + yfield)
    label11.config(bg="grey25", fg="white")

    global tracer_cal
    top4.tracer_cal = StringVar(top4, value=header_list[15])
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.tracer_cal, font=SMALLER_FONT)
    top4.textbox.place(x=xfield + paddx, y=Ty + paddy * i + yfield)
    tracer_cal = top4.tracer_cal
    i = i + 1

    '''
        top4.tracerflow_units = StringVar(top4)
        top4.tracerflow_units.set('scfh') #sets default dropdown to header_default
        x = OptionMenu(top4, top4.tracerflow_units, 'slpm', 'scfh', 'sccm')       #list of test_gas dropdown options
        x.config(font=SMALLERR_FONT)
        menu = top4.nametowidget(w.menuname)
        menu.config(font=SMALLERR_FONT)
        x.place(x=xfield+paddx+220,y=208+paddy*i+yfield)
        tracerflow_units = top4.tracerflow_units.get()
        '''
    # instrument flow entry
    label12 = tk.Label(top4, text="Flow Rate (SCFH):", font=SMALL_FONT)
    label12.place(x=xfield + paddx, y=Ly + paddy * i + yfield)
    label12.config(bg="grey25", fg="white")

    top4.tracer_flow = StringVar(top4, value=header_list[16])
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.tracer_flow, font=SMALLER_FONT)
    top4.textbox.place(x=xfield + paddx, y=Ty + paddy * i + yfield)
    tracer_flow = top4.tracer_flow
    i = i + 1

    # instrument specification
    label13 = tk.Label(top4, text="Specification (PPB):", font=SMALL_FONT)
    label13.place(x=xfield + paddx, y=Ly + paddy * i + yfield)
    label13.config(bg="grey25", fg="white")

    global tracer_spec
    top4.tracer_spec = StringVar(top4, value=header_list[17])
    top4.textbox = ttk.Entry(top4, width=20, textvariable=top4.tracer_spec, font=SMALLER_FONT)
    top4.textbox.place(x=xfield + paddx, y=Ty + paddy * i + yfield)
    tracer_spec = top4.tracer_spec
    i = i + 1

    global o2MeanValueVar
    global o2FinalValueVar
    global time_elapsed
    global O2csvFound, H2OcsvFound, BothcsvFound
    global time_elapsedO2
    global oldStopTimeRO2
    global oldStartTimeRO2
    global time_elapsedO2
    global oldStopTimeRH2O
    global oldStartTimeRH2O
    if start_stop == 'stop':
        yfield += 180  # adjusted 10/16/20
        paddy -= 10  # for new test parameters layout

        if var2.get() != 'radO2':
            # Mean Moisture Value
            label13 = tk.Label(top4, text="Moisture Average (PPB):", font=SMALL_FONT)
            label13.place(x=xfield + paddx, y=125 + paddy * i + yfield)
            label13.config(bg="grey25", fg="white")

            try:
                h2obAvgEdit
            except NameError:
                h2obAvgEdit_exists = False
            else:
                h2obAvgEdit_exists = True

            if h2obAvgEdit_exists == False and start_stop == 'manage':
                try:
                    header_list[21]
                except:
                    h2oMeanValueVar = StringVar(value=h2obAvgUnedit)
                else:
                    h2oMeanValueVar = StringVar(value=header_list[21])
                label14 = tk.Label(top4, textvariable=h2oMeanValueVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                i = i + 1.05
            if h2obAvgEdit_exists == False and start_stop == 'stop':
                h2oMeanValueVar = StringVar(value=h2oMeanValue)
                label14 = tk.Label(top4, textvariable=h2oMeanValueVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                i = i + 1.05
            if h2obAvgEdit_exists == True:
                h2obAvgEditVar = StringVar(value=h2obAvgEdit)
                label14 = tk.Label(top4, textvariable=h2obAvgEditVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                i = i + 1.05

            # Final Moisture Value
            label13 = tk.Label(top4, text="Moisture Final (PPB):", font=SMALL_FONT)
            label13.place(x=xfield + paddx, y=130 + paddy * i + yfield)
            label13.config(bg="grey25", fg="white")

            try:
                h2obFinalEdit
            except NameError:
                h2obFinalEdit_exists = False
            else:
                h2obFinalEdit_exists = True
            if h2obFinalEdit_exists == False and start_stop == 'manage':
                try:
                    header_list[23]
                except:
                    h2oFinalValueVar = StringVar(value=h2obFinalUnedit)
                else:
                    h2oFinalValueVar = StringVar(value=header_list[23])
                label14 = tk.Label(top4, textvariable=h2oFinalValueVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=165 + paddy * i + yfield)
                i = i - 1.05
            if h2obFinalEdit_exists == False and start_stop == 'stop':
                h2oFinalValueVar = StringVar(value=h2oFinalValue)
                label14 = tk.Label(top4, textvariable=h2oFinalValueVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=165 + paddy * i + yfield)
                i = i - 1.05
            if h2obFinalEdit_exists == True:
                h2obFinalEditVar = StringVar(value=h2obFinalEdit)
                label14 = tk.Label(top4, textvariable=h2obFinalEditVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=165 + paddy * i + yfield)
                i = i - 1.05
        if var2.get() != 'radH2O':
            xfield = 400
            # i=6
            # Mean Oxygen Value
            label13 = tk.Label(top4, text="Oxygen Average (PPB):", font=SMALL_FONT)
            label13.place(x=xfield + paddx, y=125 + paddy * i + yfield)
            label13.config(bg="grey25", fg="white")

            try:
                o2bAvgEdit
            except NameError:
                o2bAvgEdit_exists = False
            else:
                o2bAvgEdit_exists = True

            if o2bAvgEdit_exists == False and start_stop == 'manage':
                try:
                    header_list[18]
                except:
                    o2bAvgEditVar = StringVar(value=o2bAvgUnedit)
                else:
                    o2bAvgEditVar = StringVar(value=header_list[18])
                label14 = tk.Label(top4, textvariable=o2bAvgEditVar, width=17, bg="grey35", fg="white", font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                i = i + 1.05
            if o2bAvgEdit_exists == False and start_stop == 'stop':
                global o2MeanValueVar
                label14 = tk.Label(top4, textvariable=o2MeanValueVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                i = i + 1.05
            if o2bAvgEdit_exists == True:
                o2bAvgEditVar = StringVar(value=o2bAvgEdit)
                label14 = tk.Label(top4, textvariable=o2bAvgEditVar, width=17, bg="grey35", fg="white", font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                i = i + 1.05

            # Final Oxygen Value
            label13 = tk.Label(top4, text="Oxygen Final (PPB):", font=SMALL_FONT)
            label13.place(x=xfield + paddx, y=130 + paddy * i + yfield)
            label13.config(bg="grey25", fg="white")

            try:
                o2bFinalEdit
            except NameError:
                o2bFinalEdit_exists = False
            else:
                o2bFinalEdit_exists = True

            if o2bFinalEdit_exists == False and start_stop == 'manage':
                try:
                    header_list[20]
                except:
                    o2bFinalEditVar = StringVar(value=o2bFinalUnedit)
                else:
                    o2bFinalEditVar = StringVar(value=header_list[20])
                label14 = tk.Label(top4, textvariable=o2bFinalEditVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=165 + paddy * i + yfield)
                i += 1
            if o2bFinalEdit_exists == False and start_stop == 'stop':
                global o2FinalValueVar
                label14 = tk.Label(top4, textvariable=o2FinalValueVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=165 + paddy * i + yfield)
                i += 1
            if o2bFinalEdit_exists == True:
                o2bFinalEditVar = StringVar(value=o2bFinalEdit)
                label14 = tk.Label(top4, textvariable=o2bFinalEditVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=165 + paddy * i + yfield)
                i += 1

        if start_stop == 'stop' or start_stop == 'start':
            if var2.get() == 'radO2':
                O2csvFound = True
                H2OcsvFound = False
            elif var2.get() == 'radH2O':
                H2OcsvFound = True
                O2csvFound = False
            elif var2.get() == 'radBoth':
                H2OcsvFound = True
                O2csvFound = True
                BothcsvFound = True
        if O2csvFound == True:
            ### Test Duration - O2
            global time_elapsedO2
            if start_stop == 'manage':
                try:
                    O2xbReset[-1]
                except:
                    global oldStopTimeRO2
                    global oldStartTimeRO2
                    time_elapseMinO2 = oldStopTimeRO2.minute - oldStartTimeRO2.minute
                    time_elapseHourO2 = oldStopTimeRO2.hour - oldStartTimeRO2.hour
                else:
                    time_elapseMinO2 = O2xbReset[-1] - O2xbReset[0]
                if time_elapseMinO2 > 60:
                    time_elapseHourO2, time_elapseMinO2 = divmod(time_elapseMinO2, 60)
                    global time_elapsedO2
                    time_elapsedO2 = str(round(time_elapseHourO2, 1)) + " hours " + str(
                        round(time_elapseMinO2, 1)) + " minutes"
                else:
                    time_elapsedO2 = str(round(time_elapseMinO2, 1)) + " minutes"

            label13 = tk.Label(top4, text="Test Duration:", font=SMALL_FONT)
            label13.place(x=xfield + paddx, y=140 + paddy * i + yfield)
            label13.config(bg="grey25", fg="white")

            if start_stop == 'start' or start_stop == 'stop':
                global time_elapsed
                if var2.get() != 'radH2O':
                    time_elapsedvar = StringVar(value=time_elapsed)
            if start_stop == 'manage':
                global newTime_durationO2
                try:
                    newTime_durationO2
                except:
                    time_elapsedvar = StringVar(value=time_elapsedO2)
                    print(time_elapsedO2)
                else:

                    time_elapsedvar = StringVar(value=newTime_durationO2)
            label14 = tk.Label(top4, textvariable=time_elapsedvar, width=17, bg="grey35", fg="white", font=SMALL_FONT)
            label14.place(x=xfield + paddx, y=175 + paddy * i + yfield)

        if var2.get() != 'radO2':
            ### Test Duration - H2O

            if start_stop == 'manage':
                try:
                    H2OxbReset[-1]
                except:
                    global oldStopTimeRH2O
                    global oldStartTimeRH2O
                    time_elapseMin = oldStopTimeRH2O.minute - oldStartTimeRH2O.minute
                    time_elapseHour = oldStopTimeRH2O.hour - oldStartTimeRH2O.hour
                else:
                    time_elapseMin = H2OxbReset[-1] - H2OxbReset[0]
                if time_elapseMin > 60:
                    time_elapseHour, time_elapseMin = divmod(time_elapseMin, 60)
                    time_elapsed = str(round(time_elapseHour, 1)) + " hours " + str(
                        round(time_elapseMin, 1)) + " minutes"
                else:
                    time_elapsed = str(round(time_elapseMin, 1)) + " minutes"

            xfield = 770
            if var2.get() == 'radH2O':
                i += 2.05
            label13 = tk.Label(top4, text="Test Duration:", font=SMALL_FONT)
            label13.place(x=xfield + paddx, y=140 + paddy * i + yfield)
            label13.config(bg="grey25", fg="white")

            if start_stop == 'start' or start_stop == 'stop':
                time_elapsedvar = StringVar(value=time_elapsed)
            if start_stop == 'manage':
                try:
                    newTime_durationH2O
                except:
                    time_elapsedvar = StringVar(value=time_elapsed)
                else:
                    time_elapsedvar = StringVar(value=newTime_durationH2O)
            label14 = tk.Label(top4, textvariable=time_elapsedvar, width=17, bg="grey35", fg="white", font=SMALL_FONT)
            label14.place(x=xfield + paddx, y=175 + paddy * i + yfield)
            i = i + 1
    elif start_stop == 'manage':
        yfield += 180  # adjusted 10/16/20
        paddy -= 10  # for new test parameters layout
        ### H2O Average and Final
        if H2OcsvFound == True:
            # Mean Moisture Value
            label13 = tk.Label(top4, text="Moisture Average (PPB):", font=SMALL_FONT)
            label13.place(x=xfield + paddx, y=125 + paddy * i + yfield)
            label13.config(bg="grey25", fg="white")

            try:
                h2obAvgEdit
            except NameError:
                h2obAvgEdit_exists = False
            else:
                h2obAvgEdit_exists = True

            if h2obAvgEdit_exists == False and start_stop == 'manage':
                try:
                    if O2csvFound == True:
                        header_list[23]
                    if O2csvFound == False:
                        header_list[20]
                except:
                    h2oMeanValueVar = StringVar(value=h2obAvgUnedit)
                else:
                    if O2csvFound == True:
                        h2oMeanValueVar = StringVar(value=header_list[23])
                    if O2csvFound == False:
                        h2oMeanValueVar = StringVar(value=header_list[20])
                label14 = tk.Label(top4, textvariable=h2oMeanValueVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                i = i + 1.05
            if h2obAvgEdit_exists == False and start_stop == 'stop':
                h2oMeanValueVar = StringVar(value=h2oMeanValue)
                label14 = tk.Label(top4, textvariable=h2oMeanValueVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                i = i + 1.05
            if h2obAvgEdit_exists == True:
                h2obAvgEditVar = StringVar(value=h2obAvgEdit)
                label14 = tk.Label(top4, textvariable=h2obAvgEditVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                i = i + 1.05

            # Final Moisture Value
            label13 = tk.Label(top4, text="Moisture Final (PPB):", font=SMALL_FONT)
            label13.place(x=xfield + paddx, y=130 + paddy * i + yfield)
            label13.config(bg="grey25", fg="white")

            try:
                h2obFinalEdit
            except NameError:
                h2obFinalEdit_exists = False
            else:
                h2obFinalEdit_exists = True
            if h2obFinalEdit_exists == False and start_stop == 'manage':
                try:
                    if O2csvFound == True:
                        header_list[25]
                    if O2csvFound == False:
                        header_list[22]
                except:
                    h2oFinalValueVar = StringVar(value=h2obFinalUnedit)
                else:
                    if O2csvFound == True:
                        h2oFinalValueVar = StringVar(value=header_list[25])
                    if O2csvFound == False:
                        h2oFinalValueVar = StringVar(value=header_list[22])
                label14 = tk.Label(top4, textvariable=h2oFinalValueVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=165 + paddy * i + yfield)
                i = i - 1.05
            if h2obFinalEdit_exists == False and start_stop == 'stop':
                h2oFinalValueVar = StringVar(value=h2oFinalValue)
                label14 = tk.Label(top4, textvariable=h2oFinalValueVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=165 + paddy * i + yfield)
                i = i - 1.05
            if h2obFinalEdit_exists == True:
                h2obFinalEditVar = StringVar(value=h2obFinalEdit)
                label14 = tk.Label(top4, textvariable=h2obFinalEditVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=165 + paddy * i + yfield)
                i = i - 1.05
        ### O2 Average and Final
        if O2csvFound == True:
            xfield = 400

            # Mean Oxygen Value
            label13 = tk.Label(top4, text="Oxygen Average (PPB):", font=SMALL_FONT)
            label13.place(x=xfield + paddx, y=125 + paddy * i + yfield)
            label13.config(bg="grey25", fg="white")

            try:
                o2bAvgEdit
            except NameError:
                o2bAvgEdit_exists = False
            else:
                o2bAvgEdit_exists = True

            if o2bAvgEdit_exists == False and start_stop == 'manage':

                try:
                    if H2OcsvFound == True:
                        header_list[20]
                    elif H2OcsvFound == False:
                        header_list[20]
                except:
                    o2bAvgEditVar = StringVar(value=o2bAvgUnedit)
                else:
                    if H2OcsvFound == True:
                        o2bAvgEditVar = StringVar(value=header_list[20])
                    elif H2OcsvFound == False:
                        o2bAvgEditVar = StringVar(value=header_list[20])
                label14 = tk.Label(top4, textvariable=o2bAvgEditVar, width=17, bg="grey35", fg="white", font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                i = i + 1.05
            if o2bAvgEdit_exists == False and start_stop == 'stop':
                label14 = tk.Label(top4, textvariable=o2MeanValueVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                i = i + 1.05
            if o2bAvgEdit_exists == True:
                o2bAvgEditVar = StringVar(value=o2bAvgEdit)
                label14 = tk.Label(top4, textvariable=o2bAvgEditVar, width=17, bg="grey35", fg="white", font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                i = i + 1.05

            # Final Oxygen Value
            label13 = tk.Label(top4, text="Oxygen Final (PPB):", font=SMALL_FONT)
            label13.place(x=xfield + paddx, y=130 + paddy * i + yfield)
            label13.config(bg="grey25", fg="white")

            try:
                o2bFinalEdit
            except NameError:
                o2bFinalEdit_exists = False
            else:
                o2bFinalEdit_exists = True

            if o2bFinalEdit_exists == False and start_stop == 'manage':
                try:
                    if H2OcsvFound == True:
                        header_list[22]
                    if H2OcsvFound == False:
                        header_list[22]
                except:
                    o2bFinalEditVar = StringVar(value=o2bFinalUnedit)
                else:
                    if H2OcsvFound == True:
                        o2bFinalEditVar = StringVar(value=header_list[22])
                    if H2OcsvFound == False:
                        o2bFinalEditVar = StringVar(value=header_list[22])
                label14 = tk.Label(top4, textvariable=o2bFinalEditVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=165 + paddy * i + yfield)
                i += 1
            if o2bFinalEdit_exists == False and start_stop == 'stop':
                label14 = tk.Label(top4, textvariable=o2FinalValueVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=165 + paddy * i + yfield)
                i += 1
            if o2bFinalEdit_exists == True:
                o2bFinalEditVar = StringVar(value=o2bFinalEdit)
                label14 = tk.Label(top4, textvariable=o2bFinalEditVar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
                label14.place(x=xfield + paddx, y=165 + paddy * i + yfield)
                i += 1

        try:
            print("O2, H2O, Both")
            print(O2csvFound, H2OcsvFound, BothcsvFound)
        except:
            pass

        ### Test Duration - O2
        if O2csvFound == True:

            if start_stop == 'manage':
                try:
                    O2xbReset[-1]
                except:
                    time_elapseO2 = oldStopTimeRO2 - oldStartTimeRO2
                    time_elapseSecO2 = time_elapseO2.total_seconds()
                    time_elapseMinO2, time_elapseSecO2 = divmod(time_elapseSecO2, 60)
                    time_elapseHourO2, time_elapseMinO2 = divmod(time_elapseMinO2, 60)
                    time_elapseDayO2, time_elapseHourO2 = divmod(time_elapseHourO2, 24)
                else:
                    time_elapseMinO2 = O2xbReset[-1] - O2xbReset[0]
                    time_elapseHourO2, time_elapseMinO2 = divmod(time_elapseMinO2, 60)
                    time_elapseDayO2, time_elapseHourO2 = divmod(time_elapseHourO2, 24)
                    print("day=" + str(time_elapseDayO2) + " hour=" + str(time_elapseHourO2) + " minute=" + str(
                        time_elapseMinO2))

                if int(time_elapseDayO2) > 0:
                    time_elapsedO2 = str(int(time_elapseDayO2)) + " days " + str(int(time_elapseHourO2)) + " hours "
                    print(time_elapsedO2)
                elif int(time_elapseDayO2) < 1 and int(time_elapseHourO2) > 0:
                    time_elapsedO2 = str(int(time_elapseHourO2)) + " hours " + str(int(time_elapseMinO2)) + " minutes"
                elif int(time_elapseDayO2) < 1 and int(time_elapseHourO2) < 1:
                    time_elapsedO2 = str(int(time_elapseMinO2)) + " minutes"
                    print(time_elapsedO2)

            label13 = tk.Label(top4, text="Test Duration:", font=SMALL_FONT)
            label13.place(x=xfield + paddx, y=140 + paddy * i + yfield)
            label13.config(bg="grey25", fg="white")

            if start_stop == 'start' or start_stop == 'stop':
                if var2.get() != 'radH2O':
                    time_elapsedvar = StringVar(value=time_elapsedO2)
            if start_stop == 'manage':
                try:
                    newTime_durationO2
                except:
                    time_elapsedvar = StringVar(value=time_elapsedO2)
                    print(time_elapsedO2)
                else:

                    time_elapsedvar = StringVar(value=newTime_durationO2)
            label14 = tk.Label(top4, textvariable=time_elapsedvar, bg="grey35", fg="white", font=SMALL_FONT, width=17)
            label14.place(x=xfield + paddx, y=175 + paddy * i + yfield)

        ### Test Duration - H2O
        if H2OcsvFound == True:

            try:
                H2OxbReset[-1]

            except:
                time_elapseH2O = oldStopTimeRH2O - oldStartTimeRH2O
                time_elapseSecH2O = time_elapseH2O.total_seconds()
                time_elapseMinH2O, time_elapseSecH2O = divmod(time_elapseSecH2O, 60)
                time_elapseHourH2O, time_elapseMinH2O = divmod(time_elapseMinH2O, 60)
                time_elapseDayH2O, time_elapseHourH2O = divmod(time_elapseHourH2O, 24)
                print("day=" + str(time_elapseDayH2O) + " hour=" + str(time_elapseHourH2O) + " minute=" + str(
                    time_elapseMinH2O))
            else:
                time_elapseMinH2O = H2OxbReset[-1] - H2OxbReset[0]
                time_elapseHourH2O, time_elapseMinH2O = divmod(time_elapseMinH2O, 60)
                time_elapseDayH2O, time_elapseHourH2O = divmod(time_elapseHourH2O, 24)
                print("day=" + str(time_elapseDayH2O) + " hour=" + str(time_elapseHourH2O) + " minute=" + str(
                    time_elapseMinH2O))
            global time_elapsedH2O
            if int(time_elapseDayH2O) > 0:
                time_elapsedH2O = str(int(time_elapseDayH2O)) + " days " + str(int(time_elapseHourH2O)) + " hours "
                print("H2O time is " + str(time_elapsedH2O))
            elif int(time_elapseDayH2O) < 1 and int(time_elapseHourH2O) > 0:
                time_elapsedH2O = str(int(time_elapseHourH2O)) + " hours " + str(int(time_elapseMinH2O)) + " minutes"
                print("H2O time is " + str(time_elapsedH2O))
            elif int(time_elapseDayH2O) < 1 and int(time_elapseHourH2O) < 1:
                time_elapsedH2O = str(int(time_elapseMinH2O)) + " minutes"
                print("H2O time is " + str(time_elapsedH2O))

            xfield = 770
            # i+=2.05
            label13 = tk.Label(top4, text="Test Duration:", font=SMALL_FONT)
            label13.place(x=xfield + paddx, y=140 + paddy * i + yfield)
            label13.config(bg="grey25", fg="white")

            if start_stop == 'start' or start_stop == 'stop':
                time_elapsedvar = StringVar(value=time_elapsedH2O)
            if start_stop == 'manage':
                try:
                    newTime_durationH2O
                except:
                    time_elapsedvar = StringVar(value=time_elapsedH2O)
                else:
                    time_elapsedvar = StringVar(value=newTime_durationH2O)
            label14 = tk.Label(top4, textvariable=time_elapsedvar, bg="grey35", fg="white", font=SMALL_FONT, width=17)
            label14.place(x=xfield + paddx, y=175 + paddy * i + yfield)
            i = i + 1


def plot_axes_o2(x_list, y_list, axe):
    marker_style = '.'
    o2x_max = max(x_list)
    if o2data_min < 0:
        axe.set_ylim(o2data_min - 10, o2data_max + 10)
    else:
        axe.set_ylim(0 - 1, o2data_max + 10)
    axe.set_xlim([0, max(1, o2x_max)])
    axe.plot(x_list, y_list, color='#60D500', marker=marker_style, linewidth=1)

    # COMMENTED OUT 10/8/2020
    # if isinstance(title, str) and isinstance(tool_id, str):
    # a1.set_title(title+" "+tool_id, fontsize=28, pad=20)
    # else:
    # a1.set_title(title.get()+" "+tool_id.get(), fontsize=28, pad=20)
    axe.set_xlabel('Time (minutes)', color='w')
    axe.set_ylabel('Oxygen (PPB)', color='w')
    axe.tick_params(colors='w')


def plot_axes_h2o(x_list, y_list, axe):
    marker_style = '.'
    h2ox_max_val = max(x_list)
    axe.set_xlim([0, max(1, h2ox_max_val)])
    if h2odata_min < 0:
        axe.set_ylim(h2odata_min - 10, h2ox_max_val + 10)
    else:
        axe.set_ylim(0 - 1, h2odata_max + 10)
    axe.plot(x_list, y_list, color='#2FA4FF', marker=marker_style, picker=5, linewidth=1)

    # COMMENTED OUT 10/8/2020
    # if isinstance(title, str) and isinstance(tool_id, str):
    # a2.set_title(title+" "+tool_id, fontsize=28, pad=20)
    # else:
    # a2.set_title(title.get()+" "+tool_id.get(), fontsize=28, pad=20)
    axe.set_xlabel('Time (minutes)', color="w")
    axe.set_ylabel('Moisture (PPB)', color="w")
    axe.tick_params(colors='w')

    try:
        pointerx, pointery = int(xdata[ind]), float(ydata[ind])
        pointer = 'Minute: ' + str(pointerx) + '  Moisture: ' + str(pointery)
        axe.annotate(pointer, xy=(xdata[ind], ydata[ind]), xytext=(0, -15), fontsize='x-large')
        axe.annotate('', xy=(xdata[ind], ydata[ind]), xytext=(xdata[ind], ydata[ind] + 10),
                     arrowprops={'arrowstyle': '->', 'lw': 4, 'color': '#2FA4FF'}, )

    except Exception as e:
        # print(e)
        pass


def replace_images():
    place_info_img = img_o2.place_info()
    place_info_img3 = img_h2o.place_info()
    o2_position = AdjustFigure.o2_axis()
    h2o_position = AdjustFigure.ho2_axis()
    ext_position = AdjustFigure.image_ext_axis()
    if var2.get() == 'radBoth':
        if place_info_img.get('x') != o2_position['img_x']:  # need to replace
            img_o2.place(x=o2_position['img_x'], y=o2_position['img_y'])
            labelO2.place(x=o2_position['label_x'], y=o2_position['label_y'])
            labelO2_value.place(x=o2_position['value_x'], y=o2_position['value_y'])

        if place_info_img3.get('x') != h2o_position['img_x']:
            img_h2o.place(x=h2o_position['img_x'], y=h2o_position['img_y'])
            labelH2O.place(x=h2o_position['label_x'], y=h2o_position['label_y'])
            labelH2O_value.place(x=h2o_position['value_x'], y=h2o_position['value_y'])
    elif var2.get() == 'radH2O':
        if place_info_img3.get('x') != ext_position['img_x']:
            img_h2o.place(x=ext_position['img_x'], y=ext_position['img_y'])
            labelH2O.place(x=ext_position['label_x'], y=ext_position['label_y'])
            labelH2O_value.place(x=ext_position['value_x'], y=ext_position['value_y'])
            img_o2.place_forget()
            labelO2.place_forget()
            labelO2_value.place_forget()
    elif var2.get() == 'radO2':
        if place_info_img.get('x') != ext_position['img_x']:
            img_o2.place(x=ext_position['img_x'], y=ext_position['img_y'])
            img_h2o.place_forget()
            labelO2.place(x=ext_position['label_x'], y=ext_position['label_y'])
            labelO2_value.place(x=ext_position['value_x'], y=ext_position['value_y'])
            labelH2O.place_forget()
            labelH2O_value.place_forget()


def animateh2o(i):
    global currentMode
    global currentUpper
    global currentLower
    global h2o

    #### data gathering for h2o graph
    global xdata, ydata, point, ind, line

    def h2odataGrab():
        global meecoConnected
        global cycleH2O
        demo_mode = False
        if meecoConnected == True and var2.get() != 'radO2':
            attempts = 0
            while attempts < 6:
                try:

                    h2o = raw_to_ppb(get_h20(comPortMoist))  #### comment out for random data###
                    # await asyncio.sleep(0.02)
                    # time.sleep(0.02)
                    h2o = round(float(h2o), 1)
                    # currentRaw.set(round(float(raw_to_ppb(read_serial_float(0))), 1)) #### comment out for random data###
                    meecoConnected = True
                    if h2o < 0:
                        h2o = 0
                    currenth2o.set(h2o)
                    # dontPutThisHere
                    break
                except Exception as e:
                    attempts += 1
                    # await asyncio.sleep(0.02)
                    # time.sleep(0.02)

                    print(e)

                    ##DEMO MODE
                    h2o = random.random() * 100
                    h2o = round(float(h2o), 1)
                    meecoConnected = True
                    if h2o < 0:
                        h2o = 0
                    currenth2o.set(h2o)
                    demo_mode = True
                    break
                    #####################
                    currenth2o.set("N/A")
                    h2o = -20
                    if recording == True and meecoConnected == False and cycleH2O == 14:
                        print(
                            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nMEECO WAS DISCONNECTED DURING TESTING. PLEASE RESTART TGVIEW\n\n\n\n\n")
                        fuckitup('disconnect')
                        break
        elif meecoConnected == False and var2.get() != 'radO2':
            attempts = 0
            while attempts < 6:
                try:

                    h2o = raw_to_ppb(get_h20(comPortMoist))  #### comment out for random data###
                    h2o = round(float(h2o), 1)
                    meecoConnected = True
                    print(h2o)
                    if h2o < 0:
                        h2o = 0
                    currenth2o.set(h2o)
                    # dontPutThisHere
                    break
                except Exception as e:
                    attempts += 1
                    # await asyncio.sleep(0.02)
                    print(e)

                    ##DEMO MODE
                    h2o = random.random() * 100
                    h2o = round(float(h2o), 1)
                    meecoConnected = True
                    if h2o < 0:
                        h2o = 0
                    currenth2o.set(h2o)
                    demo_mode = True
                    break
                    #####################

                    meecoConnected = False
                    currenth2o.set("N/A")
                    h2o = -20

                    if recording == True and meecoConnected == False and cycleH2O == 14:
                        print(
                            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nMEECO WAS DISCONNECTED DURING TESTING. PLEASE RESTART TGVIEW\n\n\n\n\n")
                        fuckitup('disconnect')
                        break
        elif var2.get() == 'radO2':
            currenth2o.set('N/A')
            h2o = 9999

        if h2o < 0:
            h2o = 0
        if meecoConnected == True:
            # print('h2o is working')
            if not demo_mode:
                testingStatusMessageMeeco.set("")
            else:
                testingStatusMessageMeeco.set("Demo Mode")
        if meecoConnected == False:
            # print('h2o is fucked')
            testingStatusMessageMeeco.set("Check Tracer 2 Connection")

        global h2odata_max
        global h2odata_min

        try:
            h2odata_max
        except:
            h2odata_max = h2o
        else:
            if h2odata_max < h2o:
                h2odata_max = h2o

        try:
            h2odata_min
        except:
            h2odata_min = h2o
        else:
            if h2odata_min > h2o:
                h2odata_min = h2o

        party_time = False
        #### IP grabber ####
        f = os.popen('ifconfig wlan0 | grep "inet 192" | cut -c 14-27')
        current_ip = f.read()
        # print(current_ip)
        global title
        global label69
        global label68
        global rec_bg
        if isinstance(title, str):
            if title == 'party time':
                party_time = True
                if rec_bg == '#1CCA3C':
                    rec_bg = 'red'
                    label69.configure(bg=rec_bg)
                    label68.configure(bg=rec_bg)
                elif rec_bg == 'red':
                    rec_bg = '#1CCA3C'
                    label69.configure(bg=rec_bg)
                    label68.configure(bg=rec_bg)
        else:
            if title.get() == 'party time':
                party_time = True
                if rec_bg == '#1CCA3C':
                    rec_bg = 'red'
                    label69.configure(bg=rec_bg)
                    label68.configure(bg=rec_bg)
                elif rec_bg == 'red':
                    rec_bg = '#1CCA3C'
                    label69.configure(bg=rec_bg)
                    label68.configure(bg=rec_bg)

        cycleH2O += 1
        if cycleH2O == 15:
            cycleH2O = 1
            ## create a datetime stamp
            h2otime = datetime.now() - start_time

            ## create data lists of x and y values
            global h2o_dataList
            global h2odataList
            h2o_dataList = h2o_dataList + '\n' + str(round((h2otime.total_seconds()) / 60, 0)) + ',' + str(h2o)
            # print("meeco "+str(round((h2otime.total_seconds())/60,5)))
            # print("meeco "+str(round((h2otime.total_seconds())/60,0)))

            #### meecoDrift is how much the interval is drifting from 1 minute ######
            global intervalH2O
            meecoDrift = round((h2otime.total_seconds()) / 60, 5) - round((h2otime.total_seconds()) / 60, 0)
            if round((h2otime.total_seconds()) / 60, 0) != 0.0:

                if meecoDrift > 0:
                    intervalH2O -= math.sqrt(meecoDrift) * 400
                else:
                    intervalH2O += math.sqrt(meecoDrift * (-1)) * 400

            if intervalH2O < 2000:
                intervalH2O = 2000
            elif intervalH2O > 4000:
                intervalH2O = 4000
            if party_time == False:
                ani2.event_source.interval = int(intervalH2O)
            elif party_time == True:
                ani2.event_source.interval = int(10)

            print("animateh2o " + str(round((h2otime.total_seconds()) / 60, 5)) + " " + str(
                round((h2otime.total_seconds()) / 60, 0)) + " " + str(ani2.event_source.interval))
            # print(" meeco interval = " + str(ani2.event_source.interval))

            h2odataList = h2o_dataList.split('\n')
            h2odataList.pop(0)
            initial_h2otick = h2odataList[0].split(',')
            h2odataList[0] = "0," + initial_h2otick[1]
            global h2oxList
            global h2oyList
            h2oxList = []
            h2oyList = []
            global x2
            global y2
            for eachLine in h2odataList:
                if len(str(eachLine)) > 1:
                    x2, y2 = eachLine.split(',')
                    h2oxList.append(float(x2))
                    h2oyList.append(float(y2))

        ###active graphing

        global tool_id
        a2.clear()
        a2.ticklabel_format(useOffset=False)
        markerStyle = '.'
        if var2.get() == 'radO2':
            a2.plot(range(10), range(10), color='red', marker="")
            a2.plot(range(10), [9, 8, 7, 6, 5, 4, 3, 2, 1, 0], color='red', marker="")
            a2.set_title("No Data Recieved", fontsize=32, pad=20)
            a2.set_xlabel('Time (minutes)')
            a2.set_ylabel('N/A')
        if var2.get() == 'radBoth':
            h2oxMax = max(h2oxList)
            a2.set_xlim([0, max(1, h2oxMax)])
            if h2odata_min < 0:
                a2.set_ylim(h2odata_min - 10, h2odata_max + 10)
            else:
                a2.set_ylim(0 - 1, h2odata_max + 10)
            a2.plot(h2oxList, h2oyList, color='#2FA4FF', marker='.', picker=5, linewidth=1)

            # COMMENTED OUT 10/8/2020
            # if isinstance(title, str) and isinstance(tool_id, str):
            # a2.set_title(tool_id+" "+title, fontsize=28, pad=20)
            # else:
            # a2.set_title(tool_id.get()+" "+title.get(), fontsize=28, pad=20)

            a2.set_xlabel("Time (minutes)", color="w")
            a2.set_ylabel("Moisture (PPB)", color="w")
            a2.tick_params(colors='w')
            try:
                pointerx, pointery = int(xdata[ind]), float(ydata[ind])
                pointer = 'Minute: ' + str(pointerx) + '  Moisture: ' + str(pointery)
                a2.annotate(pointer, xy=(xdata[ind], ydata[ind]), xytext=(0, -15), fontsize='x-large')
                a2.annotate('', xy=(xdata[ind], ydata[ind]), xytext=(xdata[ind], ydata[ind] + 10),
                            arrowprops={'arrowstyle': '->', 'lw': 4, 'color': '#2FA4FF'}, )
            except Exception as e:
                # print(e)
                pass

        if var2.get() == 'radH2O':
            plot_axes_h2o(h2oxList, h2oyList, a2)

        h2ofileTitle = "H2O"

        if recording == True and var2.get() != 'radO2':
            global h2oValuelist
            h2oValuelist = []
            with open(os.path.join(pathF, h2ofileTitle) + '.csv', 'w+', newline='') as h:
                writer2 = csv.writer(h, escapechar=' ', quoting=csv.QUOTE_NONE)
                for eachLine in h2odataList:
                    writer2.writerow([eachLine])
                    everyLine = eachLine.split(",")
                    h2oValuelist.append(float(everyLine[1]))

                h.flush()
        try:
            figure_conf = AdjustFigure.default_figure_conf()
            fig_width, fig_height = f2.get_size_inches()
            if var2.get() == 'radH2O':
                figure_conf = AdjustFigure.ext_figure_conf()
            if fig_width != figure_conf['w']:
                f2.set_size_inches(figure_conf['w'], figure_conf['h'])

            f2.savefig('graphH2O.png', facecolor=f2.get_facecolor(), edgecolor="none")
            global img_h2o

            # imgh = Image.open('graphH2O.png')
            # wpercent = (basewidth / float(imgh.size[0]))
            # hsize = int((float(imgh.size[1]) * float(wpercent) * .92))  # 0.84
            # imgh = imgh.resize((basewidth, hsize), Image.ANTIALIAS)
            #
            # imgh.save('graphH2O.png')
            img4 = ImageTk.PhotoImage(Image.open('graphH2O.png'))
            img_h2o.configure(image=img4)
            img_h2o.image = img4
            replace_images()

        except FileNotFoundError:
            pass

    h2odataGrab()
    # loop = asyncio.new_event_loop()
    # loop.create_task(h2odataGrab())
    # loop.close()


def animateo2(i):  #### animation function. despite the name it actually animates both o2 and h2o.
    #  it also functions to save csv files if the variable 'recording' is set to TRUE

    # try:

    def o2dataGrab():
        #### data gathering for o2 graph
        global deltafConnected
        global cycleO2
        demo_mode = False
        o2 = 0
        if deltafConnected == True and var2.get() != 'radH2O':
            attempts = 0
            while attempts < 15:

                try:
                    # await asyncio.sleep(0.02)
                    # time.sleep(0.02)
                    # print('..... attempting with ' + comPortOxygen + '.....')
                    o2 = get_O2(comPortOxygen)  #### comment out for random data###

                    if 'e' in o2:
                        currento2.set('N/A')
                        o2 = round(float(o2), 1)
                        deltafConnected = False
                    else:
                        o2 = round(float(o2), 1)
                        currento2.set(o2)
                        deltafConnected = True

                    attempts = 15

                    # dontPutThisHere
                    break
                except:
                    # await asyncio.sleep(0.02)
                    # time.sleep(0.02)
                    attempts += 1
                    if attempts > 14:
                        ## DEMO MODE
                        o2 = str(random.random() * 100)
                        o2 = round(float(o2), 1)
                        currento2.set(o2)
                        deltafConnected = True
                        attempts = 15
                        print('attempt FAILED for O2')
                        demo_mode = True
                        break
                        ##############

                        o2 = 9999
                        deltafConnected = False
                        print('attempt FAILED for O2')
                        currento2.set('N/A')
                        if recording == True and deltafConnected == False and cycleO2 == 14:
                            print(
                                "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nDELTAF WAS DISCONNECTED DURING TESTING. PLEASE RESTART TGVIEW\n\n\n\n\n")
                            fuckitup('disconnect')
                            break

        elif not deltafConnected and var2.get() != 'radH2O':
            attempts = 0
            while attempts < 3:
                try:
                    # await asyncio.sleep(0.02)
                    # time.sleep(0.02)
                    # print('..... attempting with ' + comPortOxygen + '.....')
                    o2 = get_O2(comPortOxygen)  #### comment out for random data###

                    # print(o2)
                    if 'e' in o2:
                        currento2.set('N/A')
                        o2 = round(float(o2), 1)
                        deltafConnected = False
                    else:
                        o2 = round(float(o2), 1)
                        currento2.set(o2)
                        deltafConnected = True

                    attempts = 3
                    # dontPutThisHere
                    break
                except:

                    attempts += 1
                    # await asyncio.sleep(0.02)
                    # time.sleep(0.02)
                    if attempts > 1:
                        ## DEMO MODE
                        o2 = str(random.random() * 100)
                        o2 = round(float(o2), 1)
                        currento2.set(o2)
                        deltafConnected = True
                        attempts = 15
                        demo_mode = True
                        break
                        #########################

                        o2 = 9999
                        deltafConnected = False
                        print('attempt FAILED for O2')
                        currento2.set('N/A')
                        if recording == True and deltafConnected == False and cycleO2 == 14:
                            print(
                                "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nDELTAF WAS DISCONNECTED DURING TESTING. PLEASE RESTART TGVIEW\n\n\n\n\n")
                            fuckitup('disconnect')
                            break
        elif var2.get() == 'radH2O':
            currento2.set('N/A')
            o2 = 9999
        if deltafConnected == True:
            if not demo_mode:
                # print('o2 is working')
                testingStatusMessageDeltaf.set("")
            else:
                testingStatusMessageDeltaf.set("Demo Mode")
        else:
            # print('o2 is fucked')
            testingStatusMessageDeltaf.set("Check DeltaF Connection")
        global o2data_max
        global o2data_min

        if abs(o2data_max - o2) > 1000:
            return
        if abs(o2data_min - o2) > 1000:
            return

        if o2data_max < o2:
            o2data_max = o2

        if o2data_min > o2:
            o2data_min = o2

        cycleO2 += 1
        if cycleO2 == 15:
            cycleO2 = 1

            o2time = datetime.now() - start_time
            global o2_dataList
            global o2dataList
            o2_dataList = o2_dataList + '\n' + str(round((o2time.total_seconds()) / 60, 0)) + ',' + str(o2)
            # print("deltaf "+str(round((o2time.total_seconds())/60,5)))
            # print("deltaf "+str(round((o2time.total_seconds())/60,0)))

            #### deltaDrift is how much the interval is drifting from 1 minute ######
            deltaDrift = round((o2time.total_seconds()) / 60, 5) - round((o2time.total_seconds()) / 60, 0)

            ############################
            global intervalO2
            if round((o2time.total_seconds()) / 60, 0) != 0.0:

                if deltaDrift > 0:
                    intervalO2 -= math.sqrt(deltaDrift) * 400
                else:
                    intervalO2 += math.sqrt(deltaDrift * (-1)) * 400

            if intervalO2 < 2000:
                intervalO2 = 2000
            elif intervalO2 > 4000:
                intervalO2 = 4000

            ani1.event_source.interval = int(intervalO2)
            ############################

            # print(" deltaf drift = " + str(deltaDrift))
            # print(" deltaf interval = " + str(ani1.event_source.interval))
            # print(str(round((o2time.total_seconds())/60,5))+" "+str(round((o2time.total_seconds())/60,0))+" "+str(ani1.event_source.interval))

            o2dataList = o2_dataList.split('\n')
            o2dataList.pop(0)
            initial_tick = o2dataList[0].split(',')
            # print(initial_tick[1])
            o2dataList[0] = "0," + initial_tick[1]
            global o2xList
            global o2yList
            o2xList = []
            o2yList = []
            global x1
            global y1
            for eachLine in o2dataList:
                if len(str(eachLine)) > 1:
                    x1, y1 = eachLine.split(',')
                    o2xList.append(float(x1))
                    o2yList.append(float(y1))

            ###active graphing
            global title
            global tool_id
            a1.clear()
            a1.ticklabel_format(useOffset=False)
            markerStyle = '.'
            if var2.get() == 'radO2':
                plot_axes_o2(o2xList, o2yList, a1)
                # o2xMax = max(o2xList)
                # if o2data_min < 0:
                #     a1.set_ylim(o2data_min - 10, o2data_max + 10)
                # else:
                #     a1.set_ylim(0 - 1, o2data_max + 10)
                # a1.set_xlim([0, max(1, o2xMax)])
                # a1.plot(o2xList, o2yList, color='#60D500', marker=markerStyle, linewidth=1)
                #
                # # COMMENTED OUT 10/8/2020
                # # if isinstance(title, str) and isinstance(tool_id, str):
                # # a1.set_title(title+" "+tool_id, fontsize=28, pad=20)
                # # else:
                # # a1.set_title(title.get()+" "+tool_id.get(), fontsize=28, pad=20)
                #
                # a1.set_xlabel('Time (minutes)', color='w')
                # a1.set_ylabel('Oxygen (PPB)', color='w')
                # a1.tick_params(colors='w')

            if var2.get() == 'radBoth':
                dataRangeo2 = o2data_max - o2data_min
                o2xMax = max(o2xList)
                if o2data_min < 0:
                    a1.set_ylim(o2data_min - 10, o2data_max + 10)
                else:
                    a1.set_ylim(0 - 1, o2data_max + 10)
                a1.set_xlim([0, max(1, o2xMax)])
                a1.plot(o2xList, o2yList, color='#60D500', marker=markerStyle, linewidth=1)

                # COMMENTED OUT 10/8/2020
                # if isinstance(title, str) and isinstance(tool_id, str):
                # a1.set_title(tool_id+" "+title, fontsize=28, pad=20)
                # else:
                # a1.set_title(tool_id.get()+" "+title.get(), fontsize=28, pad=20)

                a1.set_xlabel("Time (minutes)", color='w')
                a1.set_ylabel("Oxygen (PPB)", color='w')
                a1.tick_params(colors='w')

            if var2.get() == 'radH2O':
                a1.plot(range(10), range(10), color='red', marker="")
                a1.plot(range(10), [9, 8, 7, 6, 5, 4, 3, 2, 1, 0], color='red', marker="")
                a1.set_title("No Data Recieved", fontsize=32, pad=20, color='w')
                a1.set_xlabel('Time (minutes)')
                a1.set_ylabel("N/A")

            o2fileTitle = "O2"

            if recording == True and var2.get() != 'radH2O':
                global o2Valuelist
                o2Valuelist = []
                with open(os.path.join(pathF, o2fileTitle) + '.csv', 'w+', newline='') as o:
                    writer1 = csv.writer(o, escapechar=' ', quoting=csv.QUOTE_NONE)
                    for eachLine in o2dataList:
                        writer1.writerow([eachLine])
                        everyLine = eachLine.split(",")
                        o2Valuelist.append(float(everyLine[1]))
                    # print(o2Valuelist)

                    o.flush()
        try:
            figure_conf = AdjustFigure.default_figure_conf()
            fig_width, fig_height = f1.get_size_inches()
            if var2.get() == 'radO2':
                figure_conf = AdjustFigure.ext_figure_conf()

            if fig_width != figure_conf['w']:
                f1.set_size_inches(figure_conf['w'], figure_conf['h'])
            # basewidth = figure_conf['w']*figure_conf['dpi']

            f1.savefig('graphO2.png', facecolor=f1.get_facecolor(), edgecolor="none")
            # imgg = Image.open('graphO2.png')
            # wpercent = (basewidth / float(imgg.size[0]))
            # hsize = int((float(imgg.size[1]) * float(wpercent) * 0.92))  # 0.84
            # imgg = imgg.resize((basewidth, hsize), Image.ANTIALIAS)
            # imgg.save('graphO2.png')
            img2 = ImageTk.PhotoImage(Image.open('graphO2.png'))
            img_o2.configure(image=img2)
            img_o2.image = img2
            replace_images()
        except FileNotFoundError:
            pass

    o2dataGrab()
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(o2dataGrab())
    # loop.close()


def stop_recording():
    # global testflow_units
    # testflow_units='scfh'
    global stop_time
    global stop_timeet
    global stop_timee
    stop_time = datetime.now()
    stop_timee = stop_time.strftime("%m_%d_%y_%H.%M.%S")
    stop_timeet = stop_time.strftime("%m_%d_%y_%H.%M.%S")

    global time_elapsed
    time_elapsed = stop_time - start_time
    time_elapsed = time_elapsed_string(time_elapsed)

    with open(f'{root_path}/Header_default.csv', newline='') as t:
        headreader = csv.reader(t)
        global header_list
        header_list = []
        for row in headreader:
            header_list.append(row[0])
    directory = dir_TGView
    path = directory + '/' + str(header_list[3]) + "_" + str(header_list[4]) + "_" + str(header_list[2]) + "_" + str(
        header_list[0]) + "_" + stop_timeet
    global pathF
    os.mkdir(path)
    pathF = path
    with open(os.path.join(path, 'Header') + '.csv', 'w+', newline='') as c:
        writer3 = csv.writer(c)
        writer3.writerow([header_list[0]])
        writer3.writerow([header_list[1]])
        writer3.writerow([header_list[2]])
        writer3.writerow([header_list[3]])
        writer3.writerow([header_list[4]])
        writer3.writerow([header_list[5]])
        writer3.writerow([header_list[6]])
        writer3.writerow([header_list[7]])
        writer3.writerow([header_list[8]])
        writer3.writerow([header_list[9]])
        writer3.writerow([header_list[10]])
        writer3.writerow([header_list[11]])
        writer3.writerow([header_list[12]])
        writer3.writerow([header_list[13]])
        writer3.writerow([header_list[14]])
        writer3.writerow([header_list[15]])
        writer3.writerow([header_list[16]])
        c.flush()

    global o2Valuelist
    o2fileTitle = "O2"
    o2Valuelist = []
    with open(os.path.join(path, o2fileTitle) + '.csv', 'w+', newline='') as o:
        writer1 = csv.writer(o, escapechar=' ', quoting=csv.QUOTE_NONE)
        for eachLine in o2dataList:
            writer1.writerow([eachLine])
            everyLine = eachLine.split(",")
            o2Valuelist.append(float(everyLine[1]))

        o.flush()
    global h2oValuelist
    h2ofileTitle = "H2O"
    h2oValuelist = []
    with open(os.path.join(path, h2ofileTitle) + '.csv', 'w+', newline='') as h:
        writer2 = csv.writer(h, escapechar=' ', quoting=csv.QUOTE_NONE)
        for eachLine in h2odataList:
            writer2.writerow([eachLine])
            everyLine = eachLine.split(",")
            h2oValuelist.append(float(everyLine[1]))

    global o2MeanValue
    o2MeanValue = str(round(mean(o2Valuelist), 1))
    global o2MeanValueVar
    o2MeanValueVar = StringVar(value=o2MeanValue)
    global o2MaxValue
    o2MaxValue = str(max(o2Valuelist))
    global o2MaxValueVar
    o2MaxValueVar = StringVar(value=o2MaxValue)
    global o2FinalValue
    o2FinalValue = str(o2Valuelist[-1])
    global o2FinalValueVar
    o2FinalValueVar = StringVar(value=o2FinalValue)

    global h2oMeanValue
    h2oMeanValue = str(round(mean(h2oValuelist), 1))
    global h2oMeanValueVar
    h2oMeanValueVar = StringVar(value=h2oMeanValue)
    global h2oMaxValue
    h2oMaxValue = str(max(h2oValuelist))
    global h2oMaxValueVar
    h2oMaxValueVar = StringVar(value=h2oMaxValue)
    global h2oFinalValue
    h2oFinalValue = str(h2oValuelist[-1])
    global h2oFinalValueVar
    h2oFinalValueVar = StringVar(value=h2oFinalValue)

    global start_timea
    start_timea = start_time.strftime("%H:%M  %m/%d/%y")
    stop_timee = stop_time.strftime("%H:%M  %m/%d/%y")

    confirm_fields(start_stop="stop")


def exportH2O(startscreen):
    if startscreen == True:  ## creating pdf from startscreen

        tracerflow_units = 'scfh'
        deltaflow_units = 'scfh'
        # O2xbReset = o2xList
        # O2yb = o2yList
        # H2OxbReset = h2oxList
        # H2Oyb = h2oyList
        global H2Oyb
        global H2OxbReset
        global xx1, yy1

        try:
            H2Oyb
        except:
            H2Oyb = yy1
        try:
            H2OxbReset
        except:
            H2OxbReset = xx1
        h2obAvgEdit = str(round(mean(H2Oyb), 1))
        h2obMaxEdit = str(round(max(H2Oyb), 1))
        h2obFinalEdit = str(round(H2Oyb[-1], 1))

        # H2OxbReset = xx1
        # O2xbReset = xx2

        with open(f'{root_path}/Header_default.csv', newline='') as t:
            headreader = csv.reader(t)
            headerdata = []
            for row in headreader:
                headerdata.append(row[0])
    if startscreen == False:  ## creating pdf from startscreen

        H2OxbReset = h2oxList
        H2Oyb = h2oyList

        h2obAvgEdit = str(round(mean(H2Oyb), 1))
        h2obMaxEdit = str(round(max(H2Oyb), 1))
        h2obFinalEdit = str(round(H2Oyb[-1], 1))

        with open(f'{root_path}/Header_default.csv', newline='') as t:
            headreader = csv.reader(t)
            headerdata = []
            for row in headreader:
                headerdata.append(row[0])

    timestart = datetime.now()

    # print("first")
    # print(datetime.now()-timestart)

    # Export H2O graph as PNG to attach to the PDF
    figH2O = plt.figure(figsize=(11.25, 6))
    plt.clf()
    plt.plot(H2OxbReset, H2Oyb, color='royalblue', marker='o', linewidth=2)
    plt.margins(0.01, 0.05)
    plt.title('Meeco Moisture Analyzer', fontsize=18, pad=15)
    plt.xlabel('Time in Minutes', fontsize=14)
    plt.ylabel('PPB', fontsize=14)
    plt.grid(True)
    plt.ticklabel_format(useOffset=False)
    h2oxMax = max(H2OxbReset)
    plt.xlim(0, h2oxMax)
    if min(H2Oyb) < 0:
        plt.ylim(min(H2Oyb) - 10, max(H2Oyb) + 10)
    else:
        plt.ylim(0 - 1, max(H2Oyb) + 10)
    figH2O.savefig("PDFpltH2O.png", facecolor=figH2O.get_facecolor(), edgecolor="none")
    # plt.close()
    # top.destroy()
    # print("second")
    # print(datetime.now()-timestart)

    # Create the first page of the PDF (H2O)
    pdf = FPDF()
    pdf.set_font("Arial", size=12)

    pdf.add_page()
    pdf.image("PDFpltH2O.png", x=0, y=35, w=217, h=116)
    pdf.image(f'{root_path}/QAM-Letter12.gif', x=10, y=10, w=120,
              h=24)  # ------- ADJUST THE FILEPATH BASED ON WHERE THE IMAGE IS LOCATED
    # pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=10, y=11, w=52, h=20)
    # pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=80, y=7, w=50, h=20)
    # pdf.image('//Mac/Home/Downloads/QAMletter1.jpg', x=135, y=10, w=65, h=21)

    # print("third")
    # print(datetime.now()-timestart)

    # ADDING HEADER INFO TO THE PDF REPORT
    # Spacing block
    pdf.cell(190, 143, ln=2)

    fieldBoxHeight = 7
    leftFieldBoxWidth = 45
    rightFieldBoxWidth = 40
    leftColumnSpacing = 40
    rightColumnSpacing = 50

    # First (and only) block
    # pdf.cell(95,8, ln=2)
    pdf.cell(leftColumnSpacing, 7, 'Client:', align='R', ln=0)
    pdf.set_font("Arial", size=11)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[1]), border=1, ln=0)
    pdf.set_font("Arial", size=12)
    pdf.cell(rightColumnSpacing, 7, 'Moisture Analyzer:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, 'Tracer 2', border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Facility:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[3]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Serial Number:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(header_list[14]), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Tool / Equipment ID:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[4]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Calibration Due:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(header_list[15]), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'System:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[2]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Instrument Flow (SCFH):', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(header_list[16]), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Source ID:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[6]), border=1, ln=0)

    pdf.cell(rightColumnSpacing, 7, 'Start Time / Date:', align='R', ln=0)
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(start_time.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    if startt_stopp == 'manage':
        global newStartTime
        try:
            newStartTime
            print(newStartTime)
        except:
            newStartTime = oldStartTimeRH2O

        else:
            pass
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(newStartTime.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    pdf.cell(190, 2, ln=1)

    pdf.cell(leftColumnSpacing, 7, 'Test Point ID:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[0]), border=1, ln=0)

    pdf.cell(rightColumnSpacing, 7, 'Stop Time / Date:', align='R', ln=0)
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(stop_time.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    if startt_stopp == 'manage':
        global newStopTime
        try:
            newStopTime

        except:
            newStopTime = oldStopTimeRH2O
        else:
            pass
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(newStopTime.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    pdf.cell(190, 2, ln=1)

    pdf.cell(leftColumnSpacing, 7, 'Test Gas:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[5]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Test Duration:', align='R', ln=0)
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(time_elapsed), border=1, ln=1)
    if startt_stopp == 'manage':
        try:
            newTime_durationH2O
        except:
            global time_elapsedH2O
            newTime_durationH2O = time_elapsedH2O
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(newTime_durationH2O), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Test Flow (SCFH):', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[8]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Average (PPB):', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, h2obAvgEdit, border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Technician:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[7]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Final (PPB):', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, h2obFinalEdit, border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(135, 7, 'Specification (PPB):', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(header_list[17]), border=1, ln=1)

    # Second block (comments  --> splits into seperate lines after 80 characters)
    print(header_list[9])
    line = str('\n'.join(textwrap.wrap(header_list[9], 80)))
    print(line)
    pdf.cell(190, 12, ln=1)
    pdf.cell(25, 7, 'Comments:', align='R', ln=0)
    pdf.multi_cell(160, 7, line, border=1)

    # print("fourth")
    # print(datetime.now()-timestart)

    # This saves the PDF file to the current working folder
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdfname = str(header_list[3]) + "_" + str(header_list[4]) + "_" + str(header_list[2]) + "_" + str(
            header_list[0]) + "_" + stop_timeet + ".pdf"
        global pathF
    if startt_stopp == 'manage':
        pdfname = str(header_list[3]) + "_" + str(header_list[4]) + "_" + str(header_list[2]) + "_" + str(
            header_list[0]) + "_" + str(newStopTime.strftime("%m_%d_%y_%I.%M.%S")) + ".pdf"
        pathF = folder

    pdfpath = pathF + '/' + pdfname
    pdf.output(pdfpath)
    pdf = FPDF(orientation='P', unit='in')
    os.chdir(dir_TGView)
    # print("evince " + pdfpath)
    os.popen("evince " + "'" + pdfpath + "'")


def exportO2(startscreen):
    if startscreen == True:  ## creating pdf from startscreen

        global O2yb
        global O2xbReset
        global xx2, yy2

        try:
            O2yb
        except:
            O2yb = yy2
        try:
            O2xbReset
        except:
            O2xbReset = xx2

        o2bAvgEdit = str(round(mean(O2yb), 1))
        o2bMaxEdit = str(round(max(O2yb), 1))
        o2bFinalEdit = str(round(O2yb[-1], 1))

        # H2OxbReset = xx1
        # O2xbReset = xx2

        with open(f'{root_path}/Header_default.csv', newline='') as t:
            headreader = csv.reader(t)
            headerdata = []
            for row in headreader:
                headerdata.append(row[0])
    if startscreen == False:  ## creating pdf from startscreen

        O2xbReset = o2xList
        O2yb = o2yList

        o2bAvgEdit = str(round(mean(O2yb), 1))
        o2bMaxEdit = str(round(max(O2yb), 1))
        o2bFinalEdit = str(round(O2yb[-1], 1))

        with open(f'{root_path}/Header_default.csv', newline='') as t:
            headreader = csv.reader(t)
            headerdata = []
            for row in headreader:
                headerdata.append(row[0])

    timestart = datetime.now()
    # Export as O2 graph as PNG to attach to the PDF
    figO2 = plt.figure(figsize=(11.25, 6))
    plt.clf()
    plt.plot(O2xbReset, O2yb, color='forestgreen', marker='o', linewidth=2)
    plt.margins(0.01, 0.05)
    plt.title('Oxygen Test Report', fontproperties=font0, fontsize=28, pad=15)
    plt.xlabel('Time in Minutes', fontsize=14)
    plt.ylabel('PPB', fontsize=14)
    plt.grid(True)
    plt.ticklabel_format(useOffset=False)
    o2xMax = max(O2xbReset)
    plt.xlim(0, o2xMax)
    if min(O2yb) < 0:
        plt.ylim(min(O2yb) - 10, max(O2yb) + 10)
    else:
        plt.ylim(0 - 1, max(O2yb) + 10)
    figO2.savefig("PDFpltO2.png", facecolor=figO2.get_facecolor(), edgecolor="none")
    # plt.close()

    # print("first")
    # print(datetime.now()-timestart)

    # Create the first page of the PDF (O2)
    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()
    pdf.image("PDFpltO2.png", x=0, y=35, w=217, h=116)
    pdf.image(f'{root_path}/QAM-Letter12.gif', x=10, y=10, w=120,
              h=24)  # ------- ADJUST THE FILEPATH BASED ON WHERE THE IMAGE IS LOCATED
    # pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=10, y=11, w=52, h=20)
    # pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=80, y=7, w=50, h=20)
    # pdf.image('//Mac/Home/Downloads/QAMletter1.jpg', x=135, y=10, w=65, h=21)

    # print("third")
    # print(datetime.now()-timestart)

    # ADDING HEADER INFO TO THE PDF REPORT
    # Spacing block
    pdf.cell(190, 143, ln=2)

    fieldBoxHeight = 7
    leftFieldBoxWidth = 45
    rightFieldBoxWidth = 40
    leftColumnSpacing = 40
    rightColumnSpacing = 50

    # First (and only) block
    # pdf.cell(95,8, ln=2)
    pdf.cell(leftColumnSpacing, 7, 'Client:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[1]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Oxygen Analyzer:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, 'Delta F', border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Facility:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[3]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Serial Number:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(header_list[10]), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Tool / Equipment ID:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[4]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Calibration Due:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(header_list[11]), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'System:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[2]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Instrument Flow (SCFH):', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth / 2, fieldBoxHeight, str(header_list[12]), border=1, ln=0)
    pdf.cell(rightColumnSpacing / 2.5, 7, 'SCFH', align='R', ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Source ID:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[6]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Start Time / Date:', align='R', ln=0)
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(start_time.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    if startt_stopp == 'manage':
        global newStartTimeO2
        try:

            newStartTimeO2

        except:
            newStartTimeO2 = oldStartTimeRO2
        else:
            pass
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(newStartTimeO2.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Test Point ID:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[0]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Stop Time / Date:', align='R', ln=0)
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(stop_time.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    if startt_stopp == 'manage':
        global newStopTimeO2
        try:
            newStopTimeO2

        except:
            newStopTimeO2 = oldStopTimeRO2
        else:
            pass

        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(newStopTimeO2.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Test Gas:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[5]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Test Duration:', align='R', ln=0)
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(time_elapsed), border=1, ln=1)
    if startt_stopp == 'manage':
        global newTime_durationO2
        try:
            newTime_durationO2
        except:
            global time_elapsedO2
            newTime_durationO2 = time_elapsedO2
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(newTime_durationO2), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Test Flow:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth / 2, fieldBoxHeight, str(header_list[8]), border=1, ln=0)
    pdf.cell(leftColumnSpacing / 2.5, 7, 'SCFH', align='R', ln=0)
    pdf.cell(rightColumnSpacing + 13, 7, 'Average:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth / 2, fieldBoxHeight, o2bAvgEdit, border=1, ln=0)
    pdf.cell(rightColumnSpacing / 3, 7, 'PPB', align='R', ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Technician:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[7]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Final:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth / 2, fieldBoxHeight, o2bFinalEdit, border=1, ln=0)
    pdf.cell(rightColumnSpacing / 3, 7, 'PPB', align='R', ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(134, 7, 'Specification:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth / 2, fieldBoxHeight, str(header_list[13]), border=1, ln=0)
    pdf.cell(rightColumnSpacing / 3, 7, 'PPB', align='R', ln=1)

    # Second block (comments  --> splits into seperate lines after 80 characters)
    # print(header_list[9])
    line = str('\n'.join(textwrap.wrap(header_list[9], 80)))
    # print(line)
    pdf.cell(190, 12, ln=1)
    pdf.cell(25, 7, 'Comments:', align='R', ln=0)
    pdf.multi_cell(160, 7, line, border=1)

    # This saves the PDF file to the current working folder
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdfname = str(header_list[3]) + "_" + str(header_list[4]) + "_" + str(header_list[2]) + "_" + str(
            header_list[0]) + "_" + stop_timeet + ".pdf"
        global pathF
    if startt_stopp == 'manage':
        pdfname = str(header_list[3]) + "_" + str(header_list[4]) + "_" + str(header_list[2]) + "_" + str(
            header_list[0]) + "_" + str(newStopTimeO2.strftime("%m_%d_%y_%I.%M.%S")) + ".pdf"
        pathF = folder

    pdfpath = pathF + '/' + pdfname
    pdf.output(pdfpath)
    pdf = FPDF(orientation='P', unit='in')
    os.chdir(dir_TGView)
    # print("evince " + pdfpath)
    os.popen("evince " + "'" + pdfpath + "'")
    '''
    # Export as PNG to attach to the PDF
    fig = plt.figure(figsize=(11.25,6))
    plt.clf()
    plt.plot(O2xReset, O2y, color='forestgreen', marker='o', linewidth=2)
    plt.margins(0.01,0.05)
    plt.title('Delta F Oxygen Analyzer', fontsize=18, pad=14)
    plt.xlabel('Time in Minutes', fontsize=14)
    plt.ylabel('PPB', fontsize=14)
    plt.grid(True)
    fig.savefig("PDFpltO2.png")
    plt.close()
    top.destroy()

    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()
    pdf.image("PDFpltO2.png", x=-5, y=26, w=217, h=116)
    pdf.image('./Logo/QPDFH.png', x=10, y=10, w=186, h=20)     #------- ADJUST THE FILEPATH BASED ON WHERE THE IMAGE IS LOCATED
    #pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=10, y=1, w=55, h=20)
    #pdf.image('//Mac/Home/Downloads/QAMletter1.jpg', x=135, y=10, w=65, h=21)

    # ADDING HEADER INFO TO THE PDF REPORT
    # Spacing block
    pdf.cell(190,132,ln=2)
    # First block (client, location, serial #)
    pdf.cell(4,10,ln=0)
    pdf.cell(116,7,'Client:', align='L', ln=0)
    pdf.cell(35,7,'Calibration Due:', align='L', ln=1)
    pdf.cell(4,10,ln=0)
    pdf.cell(95,7,str(headerdata[2]),border=1,ln=0)
    pdf.cell(21,7,ln=0)
    pdf.cell(65,7,str(headerdata[9]),border=1,ln=1) #------- ADJUST "headerH2O" TO "hheaderlist" IN FINAL BUILD
    pdf.cell(4,10,ln=0)
    #pdf.cell(116,7,'Location:', align='L', ln=0)
    pdf.cell(35,7,'Specification:', align='L', ln=1)
    pdf.cell(4,10,ln=0)
    pdf.cell(95,7,str(headerdata[1]),border=1,ln=0)
    pdf.cell(21,7,ln=0)
    pdf.cell(65,7,str(headerdata[11]),border=1,ln=1)
    pdf.cell(4,10,ln=0)
    pdf.cell(116,7,'Instrument Serial #:', align='L', ln=0)
    pdf.cell(35,7,'Instrument Flow:', align='L', ln=1)
    pdf.cell(4,10,ln=0)
    pdf.cell(95,7,str(headerdata[8]),border=1,ln=0)
    pdf.cell(21,7,ln=0)
    pdf.cell(65,7,str(headerdata[10])+' SLPM',border=1,ln=1)

    # Second block (calibration date, spec., flow)
    pdf.cell(95,11, ln=2)
    pdf.cell(30,7, 'Test Gas:', align='R',ln=0)
    pdf.cell(60,7,str(headerdata[3]),border=1,ln=0)
    pdf.cell(40,7, 'Start Time:', align='R',ln=0)
    pdf.cell(55,7,str(headerdata[16]),border=1,ln=1)
    pdf.cell(190,2,ln=1)
    #pdf.cell(30,7, 'Source Gas (PPB):', align='R',ln=0)
    #pdf.cell(60,7,str(headerdata[4]),border=1,ln=0)
    pdf.cell(40,7, 'Stop Time:', align='R',ln=0)
    pdf.cell(55,7,str(headerdata[17]),border=1,ln=1)
    pdf.cell(190,2,ln=1)
    pdf.cell(30,7,'Test Point ID:', align='R', ln=0)
    pdf.cell(60,7,str(headerdata[0]),border=1,ln=0)
    pdf.cell(40,7, 'Maximum:', align='R',ln=0)
    pdf.cell(55,7,o2MaxEdit + ' PPB',border=1,ln=1)
    pdf.cell(190,2,ln=1)
    pdf.cell(30,7, 'Technician:', align='R', ln=0)
    pdf.cell(60,7,str(headerdata[5]),border=1,ln=0)
    pdf.cell(40,7, 'Average:', align='R',ln=0)
    pdf.cell(55,7,o2AvgEdit + ' PPB',border=1,ln=1)
    pdf.cell(190,2,ln=1)
    pdf.cell(30,7, 'System Flow:', align='R', ln=0)
    pdf.cell(60,7,str(headerdata[6])+' SLPM',border=1,ln=0)
    pdf.cell(40,7, 'Final:', align='R',ln=0)
    pdf.cell(55,7,o2FinalEdit + ' PPB',border=1,ln=1)

    # Third block (comments and approval)
    pdf.cell(195,12,ln=2)
    pdf.cell(25,14, 'Comments:', align='R',ln=0)
    pdf.cell(160,14,str(headerdata[7]),border=1,ln=1)
    pdf.cell(190,2,ln=1)
    pdf.cell(25,10, 'Approval:', align='R',ln=0)
    pdf.cell(160,10,border=1,ln=1)


    # This saves the PDF file to the current working folder
    EditedFilenameO2 = "FinalReport(O2).pdf"
    pdf.output(EditedFilenameO2)     #-------(EDIT THIS TO ADJUST THE FINAL ADJUSTED PDF FILENAME)
    pdf=FPDF(orientation='P', unit='in', format='Letter')

    # Open the newly created PDF using Chrome
    #chrome_path = ('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
    #p = subprocess.Popen([chrome_path, "file:"+folder+"/"+EditedFilenameO2]) #This uses 'Subprocess' to open the file
    os.popen("pdfviewer " + folder + "FinalReport(O2).pdf")
    #returncode = p.wait() #This waits for the process to close
    '''


def exportBoth(startscreen):
    if startscreen == True:  ## creating pdf from startscreen

        tracerflow_units = 'scfh'
        deltaflow_units = 'scfh'
        # O2xbReset = o2xList
        # O2yb = o2yList
        # H2OxbReset = h2oxList
        # H2Oyb = h2oyList
        global H2Oyb
        global O2yb
        global H2OxbReset
        global O2xbReset
        global xx1, yy1
        global xx2, yy2

        try:
            H2Oyb
        except:
            H2Oyb = yy1
        try:
            O2yb
        except:
            O2yb = yy2
        try:
            H2OxbReset
        except:
            H2OxbReset = xx1
        try:
            O2xbReset
        except:
            O2xbReset = xx2
        h2obAvgEdit = str(round(mean(H2Oyb), 1))
        h2obMaxEdit = str(round(max(H2Oyb), 1))
        h2obFinalEdit = str(round(H2Oyb[-1], 1))

        o2bAvgEdit = str(round(mean(O2yb), 1))
        o2bMaxEdit = str(round(max(O2yb), 1))
        o2bFinalEdit = str(round(O2yb[-1], 1))

        # H2OxbReset = xx1
        # O2xbReset = xx2

        with open(f'{root_path}/Header_default.csv', newline='') as t:
            headreader = csv.reader(t)
            headerdata = []
            for row in headreader:
                headerdata.append(row[0])
    if startscreen == False:  ## creating pdf from startscreen

        tracerflow_units = 'scfh'
        deltaflow_units = 'scfh'
        O2xbReset = o2xList
        O2yb = o2yList
        H2OxbReset = h2oxList
        H2Oyb = h2oyList

        h2obAvgEdit = str(round(mean(H2Oyb), 1))
        h2obMaxEdit = str(round(max(H2Oyb), 1))
        h2obFinalEdit = str(round(H2Oyb[-1], 1))

        o2bAvgEdit = str(round(mean(O2yb), 1))
        o2bMaxEdit = str(round(max(O2yb), 1))
        o2bFinalEdit = str(round(O2yb[-1], 1))

        with open(f'{root_path}/Header_default.csv', newline='') as t:
            headreader = csv.reader(t)
            headerdata = []
            for row in headreader:
                headerdata.append(row[0])

    timestart = datetime.now()
    # Export as O2 graph as PNG to attach to the PDF
    figO2 = plt.figure(figsize=(11.25, 6))
    plt.clf()
    plt.plot(O2xbReset, O2yb, color='forestgreen', marker='o', linewidth=2)
    plt.margins(0.01, 0.05)
    plt.title('Oxygen Test Report', fontproperties=font0, fontsize=28, pad=15)
    plt.xlabel('Time in Minutes', fontsize=14)
    plt.ylabel('PPB', fontsize=14)
    plt.grid(True)
    plt.ticklabel_format(useOffset=False)
    dataRangeo2 = max(O2yb) - min(O2yb)
    o2xMax = max(O2xbReset)
    plt.xlim(0, o2xMax)
    if min(O2yb) < 0:
        plt.ylim(min(O2yb) - 10, max(O2yb) + 10)
    else:
        plt.ylim(0 - 1, max(O2yb) + 10)
    figO2.savefig("PDFpltO2.png", facecolor=figO2.get_facecolor(), edgecolor="none")
    # plt.close()

    # print("first")
    # print(datetime.now()-timestart)

    # Export H2O graph as PNG to attach to the PDF
    figH2O = plt.figure(figsize=(11.25, 6))
    plt.clf()
    plt.plot(H2OxbReset, H2Oyb, color='royalblue', marker='o', linewidth=2)
    plt.margins(0.01, 0.05)
    plt.title('Moisture Test Report', fontproperties=font0, fontsize=28, pad=15)
    plt.xlabel('Time in Minutes', fontsize=14)
    plt.ylabel('PPB', fontsize=14)
    plt.grid(True)
    plt.ticklabel_format(useOffset=False)
    h2oxMax = max(H2OxbReset)
    plt.xlim(0, h2oxMax)
    if min(H2Oyb) < 0:
        plt.ylim(min(H2Oyb) - 10, max(H2Oyb) + 10)
    else:
        plt.ylim(0 - 1, max(H2Oyb) + 10)
    figH2O.savefig("PDFpltH2O.png", facecolor=figH2O.get_facecolor(), edgecolor="none")
    # plt.close()
    # top.destroy()
    # print("second")
    # print(datetime.now()-timestart)

    # Create the first page of the PDF (O2)
    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()
    pdf.image("PDFpltO2.png", x=0, y=35, w=217, h=116)
    pdf.image(f'{root_path}/QAM-Letter12.gif', x=10, y=10, w=120,
              h=24)  # ------- ADJUST THE FILEPATH BASED ON WHERE THE IMAGE IS LOCATED
    # pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=10, y=11, w=52, h=20)
    # pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=80, y=7, w=50, h=20)
    # pdf.image('//Mac/Home/Downloads/QAMletter1.jpg', x=135, y=10, w=65, h=21)

    # print("third")
    # print(datetime.now()-timestart)

    # ADDING HEADER INFO TO THE PDF REPORT
    # Spacing block
    pdf.cell(190, 143, ln=2)

    fieldBoxHeight = 7
    leftFieldBoxWidth = 58
    rightFieldBoxWidth = 40
    leftColumnSpacing = 40
    rightColumnSpacing = 36
    font_size_original = 12
    # First (and only) block
    # pdf.cell(95,8, ln=2)
    pdf.cell(leftColumnSpacing, 7, 'Client:', align='R', ln=0)

    def font_size_shrink(field_length):
        shrink = field_length - font_size_original - 4
        if shrink < 0:
            shrink = 0
        return shrink

    # print("font_size = " + str(font_size_original-font_size_shrink(len(str(header_list[1])))))
    # pdf.set_font("Arial", size=font_size_original-font_size_shrink(len(str(header_list[1]))))
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[1]), border=1, ln=0)
    # pdf.set_font("Arial", size=12)
    pdf.cell(rightColumnSpacing, 7, 'Analyzer:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, 'Delta F', border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Facility:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[3]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Serial Number:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(header_list[10]), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Tool / Equipment ID:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[4]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Calibration Due:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(header_list[11]), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'System:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[2]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Instrument Flow:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth / 2, fieldBoxHeight, str(header_list[12]), border=1, ln=0)
    pdf.cell(rightColumnSpacing / 2.5, 7, 'SCFH', align='R', ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Source ID:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[6]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Start Time/Date:', align='R', ln=0)
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(start_time.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    if startt_stopp == 'manage':
        global newStartTimeO2
        try:

            newStartTimeO2

        except:
            newStartTimeO2 = oldStartTimeRO2
        else:
            pass
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(newStartTimeO2.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Test Point ID:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[0]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Stop Time/Date:', align='R', ln=0)
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(stop_time.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    if startt_stopp == 'manage':
        global newStopTimeO2
        try:
            newStopTimeO2

        except:
            newStopTimeO2 = oldStopTimeRO2
        else:
            pass

        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(newStopTimeO2.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Test Gas:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[5]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Test Duration:', align='R', ln=0)
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(time_elapsed), border=1, ln=1)
    if startt_stopp == 'manage':
        global newTime_durationO2
        try:
            newTime_durationO2
        except:
            global time_elapsedO2
            newTime_durationO2 = time_elapsedO2
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(newTime_durationO2), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Test Flow:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth / 2, fieldBoxHeight, str(header_list[8]), border=1, ln=0)
    pdf.cell(leftColumnSpacing / 2.5, 7, 'SCFH', align='R', ln=0)
    pdf.cell(rightColumnSpacing + 13, 7, 'Average:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth / 2, fieldBoxHeight, o2bAvgEdit, border=1, ln=0)
    pdf.cell(rightColumnSpacing / 3, 7, 'PPB', align='R', ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Technician:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[7]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Final:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth / 2, fieldBoxHeight, o2bFinalEdit, border=1, ln=0)
    pdf.cell(rightColumnSpacing / 3, 7, 'PPB', align='R', ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(134, 7, 'Specification:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth / 2, fieldBoxHeight, str(header_list[13]), border=1, ln=0)
    pdf.cell(rightColumnSpacing / 3, 7, 'PPB', align='R', ln=1)

    # Second block (comments  --> splits into seperate lines after 80 characters)
    # print(header_list[9])
    commentary = header_list[9]
    line = str('\n'.join(textwrap.wrap(commentary[:180], 68)))
    # print(line)
    pdf.cell(190, 12, ln=1)
    pdf.cell(25, 7, 'Comments:', align='R', ln=0)
    pdf.multi_cell(160, 7, line, border=1)

    # print("fourth")
    # print(datetime.now()-timestart)

    pdf.add_page()
    pdf.image("PDFpltH2O.png", x=0, y=35, w=217, h=116)
    pdf.image(f'{root_path}/QAM-Letter12.gif', x=10, y=10, w=120,
              h=24)  # ------- ADJUST THE FILEPATH BASED ON WHERE THE IMAGE IS LOCATED
    # pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=10, y=11, w=52, h=20)
    # pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=80, y=7, w=50, h=20)
    # pdf.image('//Mac/Home/Downloads/QAMletter1.jpg', x=135, y=10, w=65, h=21)

    # print("third")
    # print(datetime.now()-timestart)

    # ADDING HEADER INFO TO THE PDF REPORT
    # Spacing block
    pdf.cell(190, 143, ln=2)

    fieldBoxHeight = 7
    leftFieldBoxWidth = 58
    rightFieldBoxWidth = 40
    leftColumnSpacing = 40
    rightColumnSpacing = 36

    # First (and only) block
    # pdf.cell(95,8, ln=2)
    pdf.cell(leftColumnSpacing, 7, 'Client:', align='R', ln=0)
    pdf.set_font("Arial", size=11)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[1]), border=1, ln=0)
    pdf.set_font("Arial", size=12)
    pdf.cell(rightColumnSpacing, 7, 'Analyzer:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, 'Tracer 2', border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Facility:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[3]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Serial Number:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(header_list[14]), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Tool / Equipment ID:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[4]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Calibration Due:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(header_list[15]), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'System:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[2]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Instrument Flow:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth / 2, fieldBoxHeight, str(header_list[16]), border=1, ln=0)
    pdf.cell(rightColumnSpacing / 2.5, 7, 'SCFH', align='R', ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Source ID:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[6]), border=1, ln=0)

    pdf.cell(rightColumnSpacing, 7, 'Start Time/Date:', align='R', ln=0)
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(start_time.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    if startt_stopp == 'manage':
        global newStartTime
        try:
            newStartTime
            print(newStartTime)
        except:
            newStartTime = oldStartTimeRH2O

        else:
            pass
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(newStartTime.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    pdf.cell(190, 2, ln=1)

    pdf.cell(leftColumnSpacing, 7, 'Test Point ID:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[0]), border=1, ln=0)

    pdf.cell(rightColumnSpacing, 7, 'Stop Time/Date:', align='R', ln=0)
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(stop_time.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    if startt_stopp == 'manage':
        try:
            newStopTime
            print(newStopTime)
        except:
            newStopTime = oldStopTimeRH2O
        else:
            pass
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(newStopTime.strftime("%H:%M %m/%d/%y")), border=1, ln=1)
    pdf.cell(190, 2, ln=1)

    pdf.cell(leftColumnSpacing, 7, 'Test Gas:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[5]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Test Duration:', align='R', ln=0)
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(time_elapsed), border=1, ln=1)
    if startt_stopp == 'manage':
        try:
            global newTime_durationH2O
            newTime_durationH2O
        except:
            global time_elapsedH2O
            newTime_durationH2O = time_elapsedH2O
        pdf.cell(rightFieldBoxWidth, fieldBoxHeight, str(newTime_durationH2O), border=1, ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Test Flow:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth / 2, fieldBoxHeight, str(header_list[8]), border=1, ln=0)
    pdf.cell(leftColumnSpacing / 2.5, 7, 'SCFH', align='R', ln=0)
    pdf.cell(rightColumnSpacing + 13, 7, 'Average:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth / 2, fieldBoxHeight, h2obAvgEdit, border=1, ln=0)
    pdf.cell(rightColumnSpacing / 3, 7, 'PPB', align='R', ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(leftColumnSpacing, 7, 'Technician:', align='R', ln=0)
    pdf.cell(leftFieldBoxWidth, fieldBoxHeight, str(header_list[7]), border=1, ln=0)
    pdf.cell(rightColumnSpacing, 7, 'Final:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth / 2, fieldBoxHeight, h2obFinalEdit, border=1, ln=0)
    pdf.cell(rightColumnSpacing / 3, 7, 'PPB', align='R', ln=1)
    pdf.cell(190, 2, ln=1)
    pdf.cell(134, 7, 'Specification:', align='R', ln=0)
    pdf.cell(rightFieldBoxWidth / 2, fieldBoxHeight, str(header_list[17]), border=1, ln=0)
    pdf.cell(rightColumnSpacing / 3, 7, 'PPB', align='R', ln=1)

    # Second block (comments  --> splits into seperate lines after 80 characters)
    # print(header_list[9])
    commentary = header_list[9]
    line = str('\n'.join(textwrap.wrap(commentary[:180], 68)))
    # print(line)
    pdf.cell(190, 12, ln=1)
    pdf.cell(25, 7, 'Comments:', align='R', ln=0)
    pdf.multi_cell(160, 7, line, border=1)

    # print("fourth")
    # print(datetime.now()-timestart)

    # This saves the PDF file to the current working folder
    if startt_stopp == 'start' or startt_stopp == 'stop':
        pdfname = str(header_list[3]) + "_" + str(header_list[4]) + "_" + str(header_list[2]) + "_" + str(
            header_list[0]) + "_" + stop_timeet + ".pdf"
        global pathF
    if startt_stopp == 'manage':
        pdfname = str(header_list[3]) + "_" + str(header_list[4]) + "_" + str(header_list[2]) + "_" + str(
            header_list[0]) + "_" + str(newStopTime.strftime("%m_%d_%y_%I.%M.%S")) + ".pdf"
        pathF = folder

    pdfpath = pathF + '/' + pdfname
    pdf.output(pdfpath)
    pdf = FPDF(orientation='P', unit='in')
    os.chdir(dir_TGView)
    # print("evince " + pdfpath)
    os.popen("evince " + "'" + pdfpath + "'")

    # returncode = p.wait() #This waits for the process to close


def manage_pdf():
    # Find and print the current working directory
    # os.getcwd()

    # Filepath for Windows testing
    # os.chdir("//Mac/Home/Downloads") #-------(CHANGE THIS TO WORK WITH THE CURRENT COMPUTER)
    # print(os.getcwd())

    # Filepath for Mac testing
    # os.chdir("/Users/Work/Downloads") #-------(CHANGE THIS TO WORK WITH THE CURRENT COMPUTER)
    # print(os.getcwd())

    # Filepath for Pi (Linux) testing
    os.chdir(dir_TGView)  # -------(CHANGE THIS TO WORK WITH THE CURRENT COMPUTER)

    global TestingIncValue
    TestingIncValue = 1  # -------(THIS CONTROLS HOW OFTEN DATA IS COLLECTED AND PLOTTED)

    def openCSV():
        global H2Ocsv
        global O2csv
        global headercsv
        global folder
        H2Ocsv = None
        O2csv = None
        headercsv = None
        folder = None
        otherfiles = []
        root.withdraw()
        # toop=Toplevel()
        # # Width and height for the Tk root window
        # w = 1200
        # h = 700
        # # This gets the current screen width and height
        # ws = toop.winfo_screenwidth()
        # hs = toop.winfo_screenheight()
        # # Calculate the x and y coordinates based on the current screen size
        # sx = (ws/2) - (w/2)
        # sy = (hs/2) - (h/2)
        # # Open the root window in the middle of the screen
        # toop.geometry('%dx%d+%d+%d' % (w, h, sx, sy))
        # toop.resizable(False,False)
        # toop.config(bg="Grey25")
        folder = askopendirname(title='Choose Test to Edit', initialdir='/home/pi/TGView', foldercreation=False)
        print(folder)
        os.chdir(folder)
        global O2csvFound, H2OcsvFound, BothcsvFound
        O2csvFound = False
        H2OcsvFound = False
        BothcsvFound = False
        try:
            for file in os.listdir(folder):
                try:
                    if file.startswith("H2O") and file.endswith(".csv"):
                        H2Ocsv = file
                        H2OcsvFound = True

                    elif file.startswith("O2") and file.endswith(".csv"):
                        O2csv = file
                        O2csvFound = True

                    elif file.startswith("Header") and file.endswith(".csv"):
                        headercsv = file
                        print("Header file found")

                    else:
                        otherfiles.append(file)
                        otherfiles.clear()
                except Exception as e:
                    raise e
        except FileNotFoundError as fnfe:
            raise fnfe

        if O2csvFound == True and H2OcsvFound == True:
            BothcsvFound = True

        global top
        top = Toplevel()
        # Width and height for the Tk root window
        w = 1820
        h = 980
        # This gets the current screen width and height
        ws = top.winfo_screenwidth()
        hs = top.winfo_screenheight()
        # Calculate the x and y coordinates based on the current screen size
        sx = (ws / 2) - (w / 2)
        sy = (hs / 2) - (h / 2)
        # Open the root window in the middle of the screen
        top.geometry('%dx%d+%d+%d' % (w, h, sx, sy))
        top.resizable(False, False)
        top.config(bg="Grey25")
        global ff1
        global ff2
        ff1 = Figure(figsize=(5, 6), dpi=100, facecolor=(0.40, 0.51, 0.46))
        ff2 = Figure(figsize=(5, 6), dpi=100, facecolor=(0.40, 0.51, 0.46))
        aa1 = ff1.add_subplot(211, facecolor=(0.25, 0.25, 0.25))
        aa2 = ff2.add_subplot(211, facecolor=(0.25, 0.25, 0.25))
        aa1new = ff1.add_subplot(212, facecolor=(0.25, 0.25, 0.25))
        aa2new = ff2.add_subplot(212, facecolor=(0.25, 0.25, 0.25))

        # These are for setting the x value to 0 and incrementing by the predetermined value
        x0h = []
        x0o = []

        # These are standard lists that hold the values from the CSV files       GLOBAL LIST
        global xx1, xx2, yy1, yy2
        xx1 = []
        xx2 = []
        yy1 = []
        yy2 = []
        global header_list
        header_list = []
        global o2Path
        global h2oPath
        global dualHeaderPath
        global H2OxbReset
        global H2Oyb

        global oldStartTimeRH2O
        global oldStopTimeRH2O
        global oldStartTimeRO2
        global oldStopTimeRO2
        global h2obMaxUnedit
        global h2obFinalUnedit
        global h2obAvgUnedit
        global o2bAvgUnedit
        global o2bMaxUnedit
        global o2bFinalUnedit
        durationFont = ("century gothic", 16, "bold")
        durationFont1 = ("century gothic", 14, "bold")

        # No CSV files found
        if H2Ocsv is None and O2csv is None:
            print("No H2O or O2 CSV file found.")
            tk.Button(top, text="OK", fg="white", activeforeground="white", bg="#d73a3a", activebackground="#d94d4d",
                      font=("century gothic", 50, "bold"), command=BackToSelect).place(height=150, width=880, x=75,
                                                                                       y=495)
            tk.Label(top, text="Selection Error:", fg="#d73a3a", bg="Grey25", font=("Century Gothic", 85, "bold"),
                     justify="center", wraplength=900).place(x=90, y=75)
            tk.Label(top, text="The folder you selected does not contain an O2 or H2O CSV file.", fg="white",
                     bg="Grey25", font=("Century Gothic", 40, "bold"), justify="center", wraplength=850).place(x=95,
                                                                                                               y=270)


        # ------------------------------------------------------------------------------ #
        #                               O2 GRAPH ONLY                                    #
        # ------------------------------------------------------------------------------ #
        elif H2Ocsv is None:
            print("H2O file NOT found")
            o2Path = os.path.join(folder, O2csv)
            # Using the O2 path, transfer data from O2csv file into corresponding lists
            with open(o2Path) as csvO2:
                plots = csv.reader(csvO2, delimiter=',')
                for row in plots:
                    xx2.append(float(row[0]))
                    yy2.append(float(row[1]))

            # This handles the O2 header file
            dualHeaderPath = os.path.join(folder, headercsv)
            with open(dualHeaderPath) as csvHeaderBoth:
                bothheadernew = csv.reader(csvHeaderBoth, delimiter=',')
                for row in bothheadernew:
                    header_list.append(row[0])
                # print("headers for both graphs: "+str(header_list))

            # Creates the figure, canvas, and button
            ff2 = plt.figure(figsize=(10.1, 6), dpi=100, facecolor=(0.40, 0.51, 0.46))
            aa2 = ff2.add_subplot(211, facecolor=(0.25, 0.25, 0.25))
            aa2.ticklabel_format(useOffset=False)
            canvas1 = FigureCanvasTkAgg(ff2, master=top)
            canvas1.get_tk_widget().place(x=10, y=10)

            def update_and_generatePDF():

                confirm_fields(start_stop='manage')

            tk.Button(top, text="Generate New PDF Report", font=LARGE_FONT, bg="grey35", activebackground="orange",
                      fg="White", activeforeground="white", highlightbackground="orange", highlightthickness=2,
                      relief=FLAT, command=update_and_generatePDF).place(height=90, width=500, x=520, y=620)
            tk.Button(top, text="Return to Dashboard", font=LARGE_FONT, bg="grey35", activebackground="FireBrick1",
                      fg="White", activeforeground="white", highlightbackground="FireBrick1", highlightthickness=2,
                      relief=FLAT, command=BackToSelect).place(height=90, width=500, x=10, y=620)

            global oldStartTimeRO2
            global oldStopTimeRO2

            oldStartTimeRO2 = min(xx2)
            oldStopTimeRO2 = str(max(xx2))
            oldStartTime = header_list[18]
            oldStartTime, oldStartTimeMins, garbage = oldStartTime.split(":")
            oldStartTime, oldStartTimeHours = oldStartTime.split(" ")
            oldStartTimeYear, oldStartTimeMonth, oldStartTimeDay = oldStartTime.split("-")
            oldStartTimeRO2 = datetime(int(oldStartTimeYear), int(oldStartTimeMonth), int(oldStartTimeDay),
                                       int(oldStartTimeHours), int(oldStartTimeMins))

            oldStopTimeMins, oldStopTimeSec = oldStopTimeRO2.split(".")
            oldStopTimeHours, oldStopTimeMins = divmod(int(oldStopTimeMins), 60)
            oldStopTimeSec = int(oldStopTimeSec) / 10 * 6
            oldStopTimeRO2 = oldStartTimeRO2 + timedelta(hours=int(oldStopTimeHours), minutes=int(oldStopTimeMins),
                                                         seconds=int(oldStopTimeSec))

            # setting the top (original) graph
            aa2.plot(xx2, yy2, color='#60d500', linewidth=4, marker='o')
            aa2.grid(True)
            aa2.set_title('Click and drag top graph to select new O2', fontsize=25, pad=12)
            aa2.set_xlabel('Time in minutes', color="white")
            aa2.set_ylabel('PPB', color="white")
            aa2.tick_params(colors='w')
            ff2.subplots_adjust(top=.90, hspace=0.3)
            aa2.title.set_color('w')

            # setting up bottom (edited) graph
            global ax2
            ax2 = ff2.add_subplot(212, facecolor=(0.25, 0.25, 0.25))

            line2, = ax2.plot(xx2, yy2, color='#60d500', linewidth=4, marker='o')
            ax2.grid(True)
            ax2.set_xlabel('Time in minutes', color="white")
            ax2.set_ylabel('PPB', color="white")
            ax2.tick_params(colors='w')

            H2OdurationXfield = 420
            H2OdurationYfield = 820

            O2durationXfield = 1220
            O2durationYfield = H2OdurationYfield
            durationWidth = 250

            o2bAvgUnedit = str(round(mean(yy2), 1))
            o2bMaxUnedit = str(round(max(yy2), 1))
            o2bFinalUnedit = str(round(yy2[-1], 1))

            def onselectO2only(xmin, xmax):
                O2min, O2max = np.searchsorted(xx2, (xmin, xmax))
                O2max = min(len(xx2) - 1, O2max)
                global O2xb
                global O2yb
                O2xb = xx2[O2min:O2max]
                O2yb = yy2[O2min:O2max]
                line2.set_data(O2xb, O2yb)
                # print(O2xb+O2yb)
                ax2.set_xlim(O2xb[0], O2xb[-1])
                dataRangeo2 = max(yy2) - min(yy2)
                if min(yy2) < 0:
                    ax2.set_ylim(bottom=min(yy2) + 10, top=max(yy2) + 10)
                else:
                    ax2.set_ylim(0 - 1, top=max(yy2) + 10)
                ff2.canvas.draw_idle()

                addStartTimeO2 = str(O2xb[0])
                addStartTimeMinsO2, addStartTimeSecO2 = addStartTimeO2.split(".")
                global newStartTimeO2
                newStartTimeO2 = oldStartTimeRO2 + timedelta(minutes=int(addStartTimeMinsO2),
                                                             seconds=int(addStartTimeSecO2))

                # global oldStopTimeRO2
                # print(oldStopTimeRO2)
                # oldStopTimeRO2hours,oldStopTimeRO2, garbage =  str(oldStopTimeRO2).split(':')
                # print(oldStopTimeRO2)
                # oldStopTimeRO2mins,oldStopTimeRO2 =  str(oldStopTimeRO2).split(' ')
                # oldStopTimeRO2month, oldStopTimeRO2day, oldStopTimeRO2year =  str(oldStopTimeRO2).split('/')
                # oldStopTimeRO2year = int(oldStopTimeRO2year)+2000
                # oldStopTimeRO2 = datetime(oldStopTimeRO2year,int(oldStopTimeRO2month),int(oldStopTimeRO2day),int(oldStopTimeRO2hours),int(oldStopTimeRO2mins))
                # print(oldStopTimeRO2)

                addStopTimeO2 = str(O2xb[-1])
                addStopTimeMinsO2, addStopTimeSecO2 = addStopTimeO2.split(".")
                global newStopTimeO2
                newStopTimeO2 = oldStartTimeRO2 + timedelta(minutes=int(addStopTimeMinsO2),
                                                            seconds=int(addStopTimeSecO2))

                global newTime_durationO2

                newTime_durationO2 = newStopTimeO2 - newStartTimeO2
                newTime_durationO2 = time_elapsed_string(newTime_durationO2)

                tk.Label(top, text=newTime_durationO2, fg="#ff9500", bg="grey35", font=durationFont).place(
                    width=durationWidth, x=O2durationXfield, y=O2durationYfield)
                tk.Label(top, text="Edited Test Duration = ", fg="white", bg="grey35", font=durationFont1).place(
                    width=durationWidth, x=O2durationXfield - 250, y=O2durationYfield)

                def incremental_range(start, stop, inc):
                    value = start
                    while value < stop:
                        yield value
                        value += inc

                global O2xbReset
                O2xbReset = list(incremental_range(0, len(O2xb), TestingIncValue))
                global o2bAvgEdit
                o2bAvgEdit = str(round(mean(O2yb), 1))
                global o2bMaxEdit
                o2bMaxEdit = str(round(max(O2yb), 1))
                global o2bFinalEdit
                o2bFinalEdit = str(round(O2yb[-1], 1))

                # Save the selection into a separate .out file
                np.savetxt("O2.out", np.c_[O2xb, O2yb])

            # set useblit True on gtkagg for enhanced performance
            span = SpanSelector(aa2, onselectO2only, 'horizontal', useblit=True,
                                rectprops=dict(alpha=0.5, facecolor='#678176'))
            plt.show()



        # ------------------------------------------------------------------------------ #
        #                                H2O GRAPH ONLY                                  #
        # ------------------------------------------------------------------------------ #
        elif O2csv is None:
            print("O2 file NOT found")
            h2oPath = os.path.join(folder, H2Ocsv)
            # Using the H2O path, transfer data from H2Ocsv file into corresponding lists
            with open(h2oPath) as csvH2O:
                plots = csv.reader(csvH2O, delimiter=',')
                for row in plots:
                    xx1.append(float(row[0]))
                    yy1.append(float(row[1]))

            # This handles the h2O header file
            dualHeaderPath = os.path.join(folder, headercsv)
            with open(dualHeaderPath) as csvHeaderBoth:
                bothheadernew = csv.reader(csvHeaderBoth, delimiter=',')
                for row in bothheadernew:
                    header_list.append(row[0])
                # print("headers for both graphs: "+str(header_list))

            def update_and_generatePDF():

                confirm_fields(start_stop='manage')

            # Creates the figure, canvas, and button
            ff1 = plt.figure(figsize=(10.1, 6), dpi=100, facecolor=(0.40, 0.51, 0.46))
            aa1 = ff1.add_subplot(211, facecolor=(0.25, 0.25, 0.25))
            canvas2 = FigureCanvasTkAgg(ff1, master=top)
            canvas2.get_tk_widget().place(x=10, y=10)
            tk.Button(top, text="Save as PDF", fg="white", activeforeground="white", bg="#d73a3a",
                      activebackground="#d94d4d", font=("century gothic", 30, "bold"),
                      command=update_and_generatePDF).place(height=90, width=500, x=520, y=620)
            tk.Button(top, text="Back to Select", fg="white", activeforeground="white", bg="#ff9500",
                      activebackground="#ffab34", font=("century gothic", 30, "bold"), command=BackToSelect).place(
                height=90, width=500, x=10, y=620)

            oldStartTimeRH2O = min(xx1)
            oldStopTime = str(max(xx1))
            print(oldStopTime)
            oldStartTime = header_list[18]
            oldStartTime, oldStartTimeMins, garbage = oldStartTime.split(":")
            oldStartTime, oldStartTimeHours = oldStartTime.split(" ")
            oldStartTimeYear, oldStartTimeMonth, oldStartTimeDay = oldStartTime.split("-")
            oldStartTimeRH2O = datetime(int(oldStartTimeYear), int(oldStartTimeMonth), int(oldStartTimeDay),
                                        int(oldStartTimeHours), int(oldStartTimeMins))

            try:
                header_list[19]
            except:
                oldStopTimeMins, oldStopTimeSec = oldStopTime.split(".")
                oldStopTimeHours, oldStopTimeMins = divmod(int(oldStopTimeMins), 60)
                oldStopTimeSec = int(oldStopTimeSec) / 10 * 6
                oldStopTimeRH2O = oldStartTimeRH2O + timedelta(hours=int(oldStopTimeHours),
                                                               minutes=int(oldStopTimeMins),
                                                               seconds=int(oldStopTimeSec))
            else:
                oldStopTime = header_list[19]
                oldStopTime, oldStopTimeMins, garbage = oldStopTime.split(":")
                oldStopTime, oldStopTimeHours = oldStopTime.split(" ")
                oldStopTimeYear, oldStopTimeMonth, oldStopTimeDay = oldStopTime.split("-")
                oldStopTimeRH2O = datetime(int(oldStopTimeYear), int(oldStopTimeMonth), int(oldStopTimeDay),
                                           int(oldStopTimeHours), int(oldStopTimeMins))

            # setting the top (original) graph
            aa1.plot(xx1, yy1, color='DodgerBlue', linewidth=4, marker='o')
            aa1.grid(True)
            aa1.set_title('Click and drag top graph to select new H2O', fontsize=25, pad=12)
            aa1.set_xlabel('Time in minutes', color="white")
            aa1.set_ylabel('PPB', color="white")
            aa1.tick_params(colors='w')
            ff1.subplots_adjust(top=.90, hspace=0.3)
            aa1.title.set_color('w')

            # setting up bottom (edited) graph
            ax1 = ff1.add_subplot(212, facecolor=(0.25, 0.25, 0.25))
            line1, = ax1.plot(xx1, yy1, color='DodgerBlue', linewidth=4, marker='o')
            ax1.grid(True)
            ax1.set_xlabel('Time in minutes', color="white")
            ax1.set_ylabel('PPB', color="white")
            ax1.tick_params(colors='w')

            H2OdurationXfield = 420
            H2OdurationYfield = 820

            O2durationXfield = 1220
            O2durationYfield = H2OdurationYfield
            durationWidth = 250

            global h2o
            h2obAvgUnedit = str(round(mean(yy1), 1))
            h2obMaxUnedit = str(round(max(yy1), 1))
            h2obFinalUnedit = str(round(yy1[-1], 1))

            def onselectH2Oonly(xmin, xmax):
                H2Omin, H2Omax = np.searchsorted(xx1, (xmin, xmax))
                H2Omax = min(len(xx1) - 1, H2Omax)
                global H2Oyb
                H2Oxb = xx1[H2Omin:H2Omax]
                H2Oyb = yy1[H2Omin:H2Omax]
                line1.set_data(H2Oxb, H2Oyb)
                ax1.set_xlim(H2Oxb[0], H2Oxb[-1])
                if min(yy1) < 0:
                    ax1.set_ylim(bottom=min(yy1) + 10, top=max(yy1) + 10)
                else:
                    ax1.set_ylim(0 - 1, top=max(yy1) + 10)
                ff1.canvas.draw_idle()

                addStartTime = str(H2Oxb[0])
                addStartTimeMins, addStartTimeSec = addStartTime.split(".")
                global newStartTime
                newStartTime = oldStartTimeRH2O + timedelta(minutes=int(addStartTimeMins), seconds=int(addStartTimeSec))
                print(newStartTime)

                addStopTime = str(H2Oxb[-1])
                addStopTimeMins, addStopTimeSec = addStopTime.split(".")
                global newStopTime
                newStopTime = oldStartTimeRH2O + timedelta(minutes=int(addStopTimeMins), seconds=int(addStopTimeSec))
                print(newStopTime)
                global newTime_durationH2O
                newTime_durationH2O = newStopTime - newStartTime

                newTime_durationH2O = time_elapsed_string(newTime_durationH2O)

                tk.Label(top, text=newTime_durationH2O, fg="#ff9500", bg="grey35", font=durationFont).place(
                    width=durationWidth, x=H2OdurationXfield, y=H2OdurationYfield)
                tk.Label(top, text="Edited Test Duration = ", fg="white", bg="grey35", font=durationFont1).place(
                    width=durationWidth, x=H2OdurationXfield - 250, y=H2OdurationYfield)

                def incremental_range(start, stop, inc):
                    value = start
                    while value < stop:
                        yield value
                        value += inc

                global H2OxbReset
                H2OxbReset = list(incremental_range(0, len(H2Oxb), TestingIncValue))

                global h2obAvgEdit
                h2obAvgEdit = str(round(mean(H2Oyb), 1))
                global h2obMaxEdit
                h2obMaxEdit = str(round(max(H2Oyb), 1))
                global h2obFinalEdit
                h2obFinalEdit = str(round(H2Oyb[-1], 1))

                # Save the selection into a separate .out file
                np.savetxt("H2O.out", np.c_[H2Oxb, H2Oyb])

            # set useblit True on gtkagg for enhanced performance
            span = SpanSelector(aa1, onselectH2Oonly, 'horizontal', useblit=True,
                                rectprops=dict(alpha=0.5, facecolor='#678176'))
            plt.show()



        # ------------------------------------------------------------------------------ #
        #                           BOTH GRAPHS (H2O AND O2)                             #
        # ------------------------------------------------------------------------------ #
        else:
            # This handles the H2O file and graph
            h2oPath = os.path.join(folder, H2Ocsv)
            with open(h2oPath) as csvH2O:
                plots = csv.reader(csvH2O, delimiter=',')
                for row in plots:
                    xx1.append(float(row[0]))
                    yy1.append(float(row[1]))

            # This handles the header file
            dualHeaderPath = os.path.join(folder, headercsv)
            with open(dualHeaderPath) as csvHeaderBoth:
                bothheadernew = csv.reader(csvHeaderBoth, delimiter=',')
                for row in bothheadernew:
                    header_list.append(row[0])
                print("headers for both graphs: " + str(header_list))

            # This handles the O2 file and graph
            o2Path = os.path.join(folder, O2csv)
            with open(o2Path) as csvO2:
                plots = csv.reader(csvO2, delimiter=',')
                for row in plots:
                    xx2.append(float(row[0]))
                    yy2.append(float(row[1]))

                # This is the current threshold for O2 tests
                O2spec = 10.00
                # This pulls the final (ending) value from the O2 test
                lastO2 = (len(yy2) - 1)
                # This checks the final value of the test and determines whether it passed or failed.
                if yy2[lastO2] > O2spec:
                    print("O2 Test Result: Out of Spec.")
                    # This is used to determine the filename
                    FailedO2Test = True
                else:
                    print("O2 Test Result: Within Spec.")
                    FailedO2Test = False

            def update_and_generatePDF():

                confirm_fields(start_stop='manage')

            # Setting up the main figure and canvas for both graphs
            ff1 = plt.figure(figsize=(18, 8.5), dpi=100, facecolor=(0.35, 0.35, 0.35))
            aa1 = ff1.add_subplot(222, facecolor=(0.25, 0.25, 0.25))
            aa2 = ff1.add_subplot(221, facecolor=(0.25, 0.25, 0.25))
            canvas3 = FigureCanvasTkAgg(ff1, master=top)
            canvas3.get_tk_widget().place(x=10, y=10)

            buttonXfield = 10
            buttonYfield = 870
            buttonPad = 905
            # tk.Button(top, text="Save this Graph", fg="white", activeforeground="white", bg="#d73a3a",\
            # activebackground="#d94d4d", font=("century gothic",30,"bold"), command=update_and_generatePDF).place(height=100,width=895,x=buttonXfield+buttonPad,y=buttonYfield)

            # tk.Button(top, text="Exit", fg="white", activeforeground="white", bg="#ff9500", activebackground="#ffab34", font=("century gothic",30,"bold"), command=BackToSelect).place(height=100,width=895,x=buttonXfield,y=buttonYfield)
            tk.Button(top, text="Generate New Report", font=LARGE_FONT, bg="grey35", activebackground="orange",
                      fg="White", activeforeground="white", highlightbackground="orange", highlightthickness=2,
                      relief=FLAT, command=update_and_generatePDF).place(height=100, width=895,
                                                                         x=buttonXfield + buttonPad, y=buttonYfield)
            tk.Button(top, text="Cancel/Close Window", font=LARGE_FONT, bg="grey35", activebackground="FireBrick1",
                      fg="White", activeforeground="white", highlightbackground="FireBrick1", highlightthickness=2,
                      relief=FLAT, command=BackToSelect).place(height=100, width=895, x=buttonXfield, y=buttonYfield)

            lineWidthEdit = 2
            markerStyle = 'o'
            pointSize = 3
            # Setting up the top H2O graph
            aa1.plot(xx1, yy1, color='DodgerBlue', linewidth=lineWidthEdit, marker=markerStyle, markersize=pointSize)
            aa1.grid(True)
            aa1.set_title('Click and drag top graph to select new H2O', fontsize=15, color="white", pad=15)
            aa1.set_xlabel('Time in minutes', color="white")
            aa1.set_ylabel('PPB', color="white")
            aa1.tick_params(colors='w')
            if min(yy1) < 0:
                aa1.set_ylim(bottom=min(yy1) - 10, top=max(yy1) + 10)
            else:
                aa1.set_ylim(0, top=max(yy1) + 10)
            # ff1.subplots_adjust(top=.90, hspace=0.3)

            oldStartTimeRH2O = min(xx1)
            oldStopTime = str(max(xx1))
            print(oldStopTime)
            oldStartTime = header_list[18]
            oldStartTime, oldStartTimeMins, garbage = oldStartTime.split(":")
            oldStartTime, oldStartTimeHours = oldStartTime.split(" ")
            oldStartTimeYear, oldStartTimeMonth, oldStartTimeDay = oldStartTime.split("-")
            oldStartTimeRH2O = datetime(int(oldStartTimeYear), int(oldStartTimeMonth), int(oldStartTimeDay),
                                        int(oldStartTimeHours), int(oldStartTimeMins))

            oldStopTimeMins, oldStopTimeSec = oldStopTime.split(".")
            oldStopTimeHours, oldStopTimeMins = divmod(int(oldStopTimeMins), 60)
            oldStopTimeSec = int(oldStopTimeSec) / 10 * 6
            oldStopTimeRH2O = oldStartTimeRH2O + timedelta(hours=int(oldStopTimeHours), minutes=int(oldStopTimeMins),
                                                           seconds=int(oldStopTimeSec))

            h2obAvgUnedit = str(round(mean(yy1), 1))
            h2obMaxUnedit = str(round(max(yy1), 1))
            h2obFinalUnedit = str(round(yy1[-1], 1))

            # Setting up the top O2 graph
            aa2.plot(xx2, yy2, color='#60d500', linewidth=lineWidthEdit, marker=markerStyle, markersize=pointSize)
            aa2.grid(True)
            aa2.set_title('Click and drag top graph to select new O2', fontsize=15, color="white", pad=15)
            aa2.set_xlabel('Time in minutes', color="white")
            aa2.set_ylabel('PPB', color="white")
            aa2.tick_params(colors='w')
            dataRangeo2 = max(yy2) - min(yy2)
            if min(yy2) < 0:
                aa2.set_ylim(bottom=min(yy2) - 10, top=max(yy2) + 10)
            else:
                aa2.set_ylim(0, top=max(yy2) + 10)
            # ff1.subplots_adjust(top=.90, hspace=0.3, wspace=0.3)

            oldStartTimeRO2 = min(xx2)
            oldStopTimeRO2 = str(max(xx2))
            oldStartTime = header_list[18]
            oldStartTime, oldStartTimeMins, garbage = oldStartTime.split(":")
            oldStartTime, oldStartTimeHours = oldStartTime.split(" ")
            oldStartTimeYear, oldStartTimeMonth, oldStartTimeDay = oldStartTime.split("-")
            oldStartTimeRO2 = datetime(int(oldStartTimeYear), int(oldStartTimeMonth), int(oldStartTimeDay),
                                       int(oldStartTimeHours), int(oldStartTimeMins))

            try:
                header_list[19]
            except:
                oldStopTimeMins, oldStopTimeSec = oldStopTimeRO2.split(".")
                oldStopTimeHours, oldStopTimeMins = divmod(int(oldStopTimeMins), 60)
                oldStopTimeSec = int(oldStopTimeSec) / 10 * 6
                oldStopTimeRO2 = oldStartTimeRH2O + timedelta(hours=int(oldStopTimeHours), minutes=int(oldStopTimeMins),
                                                              seconds=int(oldStopTimeSec))
            else:
                oldStopTime = header_list[19]
                oldStopTime, oldStopTimeMins, garbage = oldStopTime.split(":")
                oldStopTime, oldStopTimeHours = oldStopTime.split(" ")
                oldStopTimeYear, oldStopTimeMonth, oldStopTimeDay = oldStopTime.split("-")
                oldStopTimeRO2 = datetime(int(oldStopTimeYear), int(oldStopTimeMonth), int(oldStopTimeDay),
                                          int(oldStopTimeHours), int(oldStopTimeMins))

            o2bAvgUnedit = str(round(mean(yy2), 1))
            o2bMaxUnedit = str(round(max(yy2), 1))
            o2bFinalUnedit = str(round(yy2[-1], 1))

            # Setting up bottom (edited) H2O graph
            ax1 = ff1.add_subplot(224, facecolor=(0.25, 0.25, 0.25))
            line1, = ax1.plot(xx1, yy1, color='DodgerBlue', linewidth=lineWidthEdit, marker=markerStyle,
                              markersize=pointSize)
            ax1.grid(True)
            ax1.set_xlabel('Time in minutes', color="white")
            ax1.set_ylabel('PPB', color="white")
            ax1.tick_params(colors='w')
            if min(yy1) < 0:
                ax1.set_ylim(bottom=min(yy1) - 10, top=max(yy1) + 10)
            else:
                ax1.set_ylim(0, top=max(yy1) + 10)

            # setting up bottom (edited) O2 graph
            ax2 = ff1.add_subplot(223, facecolor=(0.25, 0.25, 0.25))
            line2, = ax2.plot(xx2, yy2, color='#60d500', linewidth=lineWidthEdit, marker=markerStyle,
                              markersize=pointSize)
            ax2.grid(True)
            ax2.set_xlabel('Time in minutes', color="white")
            ax2.set_ylabel('PPB', color="white")
            ax2.tick_params(colors='w')
            dataRangeo2 = max(yy2) - min(yy2)
            if min(yy2) < 0:
                ax2.set_ylim(bottom=min(yy2) - 10, top=max(yy2) + 10)
            else:
                ax2.set_ylim(0, top=max(yy2) + 10)

            H2OdurationXfield = 1220
            H2OdurationYfield = 820

            O2durationXfield = 420
            O2durationYfield = H2OdurationYfield
            durationWidth = 250

            #### unedited time duration labels (work in progress) ####
            # timeLabelO21 = tk.Label(top, text=newTime_durationO2, fg="#ff9500", bg="#668275", font=durationFont).place(width=durationWidth,x=O2durationXfield,y=O2durationYfield)
            # timeLabelO22 = tk.Label(top, text="Edited Test Duration = ", fg="white", bg="#668275", font=durationFont1).place(width=durationWidth,x=O2durationXfield-250,y=O2durationYfield)

            # This handles the selection of the H2O graph

            def onselectH2O(xmin, xmax):
                H2Omin, H2Omax = np.searchsorted(xx1, (xmin, xmax))
                H2Omax = min(len(xx1) - 1, H2Omax)
                global H2Oxb
                global H2Oyb
                H2Oxb = xx1[H2Omin:H2Omax]
                H2Oyb = yy1[H2Omin:H2Omax]
                line1.set_data(H2Oxb, H2Oyb)
                ax1.set_xlim(H2Oxb[0], H2Oxb[-1])
                if min(yy1) < 0:
                    ax1.set_ylim(bottom=min(yy1) - 10, top=max(yy1) + 10)
                else:
                    ax1.set_ylim(0, top=max(yy1) + 10)
                ff1.canvas.draw_idle()

                addStartTime = str(H2Oxb[0])
                addStartTimeMins, addStartTimeSec = addStartTime.split(".")
                global newStartTime
                newStartTime = oldStartTimeRH2O + timedelta(minutes=int(addStartTimeMins), seconds=int(addStartTimeSec))

                addStopTime = str(H2Oxb[-1])
                addStopTimeMins, addStopTimeSec = addStopTime.split(".")
                global newStopTime
                newStopTime = oldStartTimeRH2O + timedelta(minutes=int(addStopTimeMins), seconds=int(addStopTimeSec))

                global newTime_durationH2O
                newTime_durationH2O = newStopTime - newStartTime
                newTime_durationH2O = time_elapsed_string(newTime_durationH2O)

                tk.Label(top, text=newTime_durationH2O, fg="#ff9500", bg="grey35", font=durationFont).place(
                    width=durationWidth, x=H2OdurationXfield, y=H2OdurationYfield)
                tk.Label(top, text="Edited Test Duration = ", fg="white", bg="grey35", font=durationFont1).place(
                    width=durationWidth, x=H2OdurationXfield - 250, y=H2OdurationYfield)

                def incremental_range(start, stop, inc):
                    value = start
                    while value < stop:
                        yield value
                        value += inc

                global H2OxbReset
                H2OxbReset = list(incremental_range(0, len(H2Oxb), TestingIncValue))

                global h2obAvgEdit
                h2obAvgEdit = str(round(mean(H2Oyb), 1))
                global h2obMaxEdit
                h2obMaxEdit = str(round(max(H2Oyb), 1))
                global h2obFinalEdit
                h2obFinalEdit = str(round(H2Oyb[-1], 1))

                # Save the selection into a separate .out file
                np.savetxt("H2O.out", np.c_[H2Oxb, H2Oyb])

            # This handles the selected portion of the O2 graph
            def onselectO2(xmin, xmax):

                O2min, O2max = np.searchsorted(xx2, (xmin, xmax))
                O2max = min(len(xx2) - 1, O2max)
                global O2xb
                global O2yb
                O2xb = xx2[O2min:O2max]
                O2yb = yy2[O2min:O2max]
                line2.set_data(O2xb, O2yb)
                # print(O2xb+O2yb)
                ax2.set_xlim(O2xb[0], O2xb[-1])
                dataRangeo2 = max(yy2) - min(yy2)
                if min(yy2) < 0:
                    ax2.set_ylim(bottom=min(yy2) - 10, top=max(yy2) + 10)
                else:
                    ax2.set_ylim(0, top=max(yy2) + 10)
                ff1.canvas.draw_idle()

                addStartTimeO2 = str(O2xb[0])
                addStartTimeMinsO2, addStartTimeSecO2 = addStartTimeO2.split(".")
                global newStartTimeO2
                newStartTimeO2 = oldStartTimeRO2 + timedelta(minutes=int(addStartTimeMinsO2),
                                                             seconds=int(addStartTimeSecO2))

                # global oldStopTimeRO2
                # print(oldStopTimeRO2)
                # oldStopTimeRO2hours,oldStopTimeRO2, garbage =  str(oldStopTimeRO2).split(':')
                # print(oldStopTimeRO2)
                # oldStopTimeRO2mins,oldStopTimeRO2 =  str(oldStopTimeRO2).split(' ')
                # oldStopTimeRO2month, oldStopTimeRO2day, oldStopTimeRO2year =  str(oldStopTimeRO2).split('/')
                # oldStopTimeRO2year = int(oldStopTimeRO2year)+2000
                # oldStopTimeRO2 = datetime(oldStopTimeRO2year,int(oldStopTimeRO2month),int(oldStopTimeRO2day),int(oldStopTimeRO2hours),int(oldStopTimeRO2mins))
                # print(oldStopTimeRO2)

                addStopTimeO2 = str(O2xb[-1])
                addStopTimeMinsO2, addStopTimeSecO2 = addStopTimeO2.split(".")
                global newStopTimeO2
                newStopTimeO2 = oldStartTimeRO2 + timedelta(minutes=int(addStopTimeMinsO2),
                                                            seconds=int(addStopTimeSecO2))

                global newTime_durationO2

                newTime_durationO2 = newStopTimeO2 - newStartTimeO2
                newTime_durationO2 = time_elapsed_string(newTime_durationO2)

                tk.Label(top, text=newTime_durationO2, fg="#ff9500", bg="grey35", font=durationFont).place(
                    width=durationWidth, x=O2durationXfield, y=O2durationYfield)
                tk.Label(top, text="Edited Test Duration = ", fg="white", bg="grey35", font=durationFont1).place(
                    width=durationWidth, x=O2durationXfield - 250, y=O2durationYfield)

                def incremental_range(start, stop, inc):
                    value = start
                    while value < stop:
                        yield value
                        value += inc

                global O2xbReset
                O2xbReset = list(incremental_range(0, len(O2xb), TestingIncValue))
                global o2bAvgEdit
                o2bAvgEdit = str(round(mean(O2yb), 1))
                global o2bMaxEdit
                o2bMaxEdit = str(round(max(O2yb), 1))
                global o2bFinalEdit
                o2bFinalEdit = str(round(O2yb[-1], 1))

                # Save the selection into a separate .out file
                np.savetxt("O2.out", np.c_[O2xb, O2yb])

            # set useblit True on gtkagg for enhanced performance
            spanH2O = SpanSelector(aa1, onselectH2O, 'horizontal', useblit=True,
                                   rectprops=dict(alpha=0.5, facecolor='#678176'))
            spanO2 = SpanSelector(aa2, onselectO2, 'horizontal', useblit=True,
                                  rectprops=dict(alpha=0.5, facecolor='#678176'))

            plt.show()

    # --------------------------------------------------------------------------------#
    #                                  COMMANDS                                      #
    # --------------------------------------------------------------------------------#
    def BackToSelect():
        top.destroy()
        ### variable resets ###
        try:
            global newStartTime
            del newStartTime
            print("deleted newStartTime")
        except:
            print("no newStartTime to delete")
            pass
        try:
            global oldStartTimeRH2O
            del oldStartTimeRH2O
            print("deleted oldStartTimeRH2O")
        except:
            print("no oldStartTimeRH2O to delete")
            pass
        try:
            global newStopTime
            del newStopTime
        except:
            print("no newStartTime to delete")
            pass
        try:
            global oldStopTimeRH2O
            del oldStopTimeRH2O
            print("deleted oldStopTimeRH2O")
        except:
            print("no newStartTime to delete")
            pass
        try:
            global newStartTimeO2
            del newStartTimeO2
            print("deleted newStartTimeO2")
        except:
            print("no newStartTimeO2 to delete")
            pass

        try:
            global oldStartTimeO2
            del oldStartTimeO2
            print("deleted oldStartTimeO2")
        except:
            print("no oldStartTimeO2 to delete")
            pass
        try:
            global newStopTimeO2
            del newStopTimeO2
            print("deleted newStopTimeO2")
        except:
            print("no newStopTimeO2 to delete")
            pass

        try:
            global oldStopTimeO2
            del oldStopTimeO2
            print("deleted oldStopTimeO2")
        except:
            print("no oldStopTimeO2 to delete")
            pass
        try:
            global o2bAvgEdit
            del o2bAvgEdit
            print("deleted o2bAvgEdit")
        except:
            print("no o2bAvgEdit to delete")
            pass
        try:
            global o2bAvgUnedit
            del o2bAvgUnedit
            print("deleted o2bAvgUnedit")
        except:
            print("no o2bAvgUnedit to delete")
            pass
        try:
            global o2bMaxEdit
            del o2bMaxEdit
            print("deleted o2bMaxEdit")
        except:
            print("no o2bMaxEdit to delete")
            pass
        try:
            global o2bMaxUnedit
            del o2bMaxUnedit
            print("deleted o2bMaxUnedit")
        except:
            print("no o2bMaxUnedit to delete")
            pass
        try:
            global o2bFinalEdit
            del o2bFinalEdit
            print("deleted o2bFinalEdit")
        except:
            print("no o2bFinalEdit to delete")
            pass
        try:
            global o2bFinalUnedit
            del o2bFinalUnedit
            print("deleted o2bFinalUnedit")
        except:
            print("no newStartTime to delete")
            pass
        try:
            global h2obAvgEdit
            del h2obAvgEdit
            print("deleted h2obAvgEdit")
        except:
            print("no h2obAvgEdit to delete")
            pass
        try:
            global h2obAvgUnedit
            del h2obAvgUnedit
            print("deleted h2obAvgUnedit")
        except:
            print("no h2obAvgUnedit to delete")
            pass
        try:
            global h2obFinalEdit
            del h2obFinalEdit
            print("deleted h2obFinalEdit")
        except:
            print("no h2obFinalEdit to delete")
            pass
        try:
            global h2obFinalUnedit
            del h2obFinalUnedit
            print("deleted h2obFinalUnedit")
        except:
            print("no h2obFinalUnedit to delete")
            pass

    # --------------------------------------------------------------------------------#
    #                                  MAIN WINDOW                                   #
    # --------------------------------------------------------------------------------#
    root = tk.Tk()
    root.title('Modify Existing Report')
    root.resizable(False, False)
    root.config(bg="Grey25")
    # Width and height for the Tk root window
    w = 1030
    h = 720
    # This gets the current screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # Calculate the x and y coordinates based on the current screen size
    sx = (ws / 2) - (w / 2)
    sy = (hs / 2) - (h / 2)
    # Open the root window in the middle of the screen
    root.geometry('%dx%d+%d+%d' % (w, h, sx, sy))

    # --------------------------------------------
    # QAM LOGO
    # --------------------------------------------
    QAMmd = Image.open(f'{root_path}/QAM.gif')
    imgSplash = ImageTk.PhotoImage(QAMmd, master=root)
    imgg = tk.Label(root, image=imgSplash, borderwidth=0, highlightthickness=0)
    imgg.image = imgSplash
    imgg.place(x=625, y=75)

    # --------------------------------------------
    # BUTTON IMAGES
    # --------------------------------------------
    dashIcon = ImageTk.PhotoImage(file=f"{root_path}/dashboard.png", master=root)
    folderIcon = ImageTk.PhotoImage(file=f"{root_path}/foldersolid.png", master=root)

    tk.Button(root, text="Select Folder", font=("century gothic", 50, "bold"), fg="white", activeforeground="white",
              bg="#ff9500", activebackground="#ffab34", image=folderIcon, compound="left", padx=30,
              command=openCSV).place(height=150, width=880, x=75, y=495)
    tk.Button(root, text="Dashboard", font=("Century Gothic", 31, "bold"), fg="white", activeforeground="white",
              bg="#678176", activebackground="#81a6a3", image=dashIcon, compound="left", padx=25,
              command=root.destroy).place(height=125, width=350, x=75, y=75)
    tk.Label(root, text="Select the folder with the correct Name, ID, Test Type, and Date", fg="White", bg="Grey25",
             font=("Century Gothic", 40, "bold"), justify="center", wraplength=850).place(x=100, y=280)

    root.mainloop()


if __name__ == '__main__':
    app = RPiReader()
    ani1 = animation.FuncAnimation(f1, animateo2, interval=intervalO2)
    ani2 = animation.FuncAnimation(f2, animateh2o, interval=intervalH2O)
    app.mainloop()
