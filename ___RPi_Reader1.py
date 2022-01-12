#!/usr/bin/python3

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.widgets import SpanSelector
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
from fpdf import FPDF
from statistics import mean

import random
import re
import serial
import time
import binascii
import csv
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import numpy as np
from datetime import datetime
import PIL
from PIL import ImageTk
from PIL import Image
import os, sys
import subprocess
from tkinter import Toplevel
from tkinter import messagebox

QAM_GREEN = "#7fa6a3"
#have a method for checking if the usb chords are plugged in correctly
#method would write serial command and check for correct response from analyzer
#def check_serial():
        
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

def write_upperandlower(valueToUpper,valueToLower):
    write_serial_float(bytearray([178]),bytearray([15]),valueToUpper)
    time.sleep(0.08)
    write_serial_float(bytearray([178]),bytearray([16]),valueToLower)

def read_serial_float(operand):
    operand = bytearray([operand])
    
    data = bytearray()
    echo = bytearray()
    command=bytearray([146])
    #operand =bytearray([16])
    
    sleepy = 0.02
    
    ser = serial.Serial(
    port='/dev/ttyUSB1',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout = 0)
    
    data = bytearray()
    ser.write(command) #send command byte
    time.sleep(sleepy)
    echo = ser.read(1) #recieve command byte
    data = data + echo
    
    
    ser.write(operand)
    time.sleep(sleepy)
    echo = ser.read(2)
    data = data + echo
    
    ser.write(bytearray([echo[-1]]))
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    
    ser.write(bytearray([echo[-1]]))
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    
    ser.write(bytearray([echo[-1]]))
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    
    
    ser.write(bytearray([echo[-1]]))
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    #print(data)
    return(data)

    ser.close()

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
    
    sleepy = 0.02
    
    ser = serial.Serial(
    port='/dev/ttyUSB1',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout = 0)
    
    data = bytearray()
    ser.write(command) #send command byte
    time.sleep(sleepy)
    echo = ser.read(1) #recieve command byte
    data = data + echo
    
    
    ser.write(operand)
    time.sleep(sleepy)
    echo = ser.read(2)
    data = data + echo
    
    ser.write(databyte1)
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    
    ser.write(databyte2)
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    
    ser.write(databyte3)
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    
    
    ser.write(databyte4)
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    
    ser.write(databyte5)
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    return(data)

    ser.close()
    

def write_serial_int(send,n):
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
    if send==True:
        command=bytearray([162])
    else:
        command=bytearray([130])
    operand =bytearray([4])
    data = bytearray()
    echo = bytearray()
    
    sleepy = 0.02
    
    ser = serial.Serial(
    port='/dev/ttyUSB1',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout = 0)
    
    ser.write(command) #send command byte
    time.sleep(sleepy)
    echo = ser.read(1) #recieve command byte
    data = data + echo
    
    
    ser.write(operand)
    time.sleep(sleepy)
    echo = ser.read(2)
    data = data + echo
    
    ser.write(byte1)
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    
    ser.write(byte2)
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    
    ser.write(byte3)
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    return(int(data[4]))
    

    ser.close()
    if int(data[4]) == 1:
                currentMode.set('Inert')
    if int(data[4]) == 0:
                currentMode.set('Service')

# gets O2 data and converts to ppb
def get_O2():
    ser = serial.Serial(
        port='/dev/ttyUSB0',\
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout = 0)

    sleepy = 0.04
    i=0
    fullcommand = bytearray([1,2,1,0,0,3,13])
    ser.write(fullcommand)
    ser.write(b' ')
    time.sleep(sleepy)
    deldata = ser.read(8)
    data = str(binascii.hexlify(deldata[4:8]))

    c = [data[i:i+2] for i in range (0, len(data), 2)]
    try:
        byte1 = "{:08b}".format(int(c[1], base=16))
        byte2 = "{:08b}".format(int(c[2], base=16))
        byte3 = "{:08b}".format(int(c[3], base=16))
        byte4 = "{:08b}".format(int(c[4], base=16))
    
        o2_bin = byte1+byte2+byte3+byte4
    
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
    
        return(str(o2_ppb))
    except:
        pass

# gets raw h2o data: need to use raw_to_ppb function to convert to ppb
def get_h20():
    data = bytearray()
    echo = bytearray()
    command=bytearray([146])
    operand =bytearray([0])
    sleepy = 0.02
    
    ser = serial.Serial(
    port='/dev/ttyUSB1',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout = 0)
    
    data = bytearray()
    ser.write(command) #send command byte
    time.sleep(sleepy)
    echo = ser.read(1) #recieve command byte
    data = data + echo
    
    
    ser.write(operand)
    time.sleep(sleepy)
    echo = ser.read(2)
    data = data + echo
    
    ser.write(bytearray([echo[-1]]))
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    
    ser.write(bytearray([echo[-1]]))
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    
    ser.write(bytearray([echo[-1]]))
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    
    
    ser.write(bytearray([echo[-1]]))
    time.sleep(sleepy)
    echo = ser.read(1)
    data = data + echo
    return(data)

    ser.close()

# converts raw h2o data to ppb
def raw_to_ppb (data):
    raw_hex = str(binascii.hexlify(data[2:]))
    c = [raw_hex[i:i+2] for i in range (0, len(raw_hex), 2)]
    try:
        byte1 = "{:08b}".format(int(c[1], base=16))
        byte2 = "{:08b}".format(int(c[2], base=16))
        byte3 = "{:08b}".format(int(c[3], base=16))
        byte4 = "{:08b}".format(int(c[4], base=16))
        byte5 = "{:08b}".format(int(c[5], base=16))
    
        h20_bin = byte1+byte2+byte3+byte4+byte5
    
        m1 = h20_bin[14:16]
        m2 = h20_bin[17:24]
        m3 = h20_bin[25:32]
        m4 = h20_bin[33:40]
        m = m1+m2+m3+m4
            
        mantissa =      (int(m[0])*2**22+int(m[1])*2**21+int(m[2])*2**20+int(m[3])*\
                    2**19+int(m[4])*2**18+int(m[5])*2**17+int(m[6])*2**16+int(m[7])*\
                    2**15+int(m[8])*2**14+int(m[9])*2**13+int(m[10])*2**12+int(m[11])*\
                    2**11+int(m[12])*2**10+int(m[13])*2**9+int(m[14])*2**8+int(m[15])*\
                     2**7+int(m[16])*2**6+int(m[17])*2**5+int(m[18])*2**4+int(m[19])*\
                     2**3+int(m[20])*2**2+int(m[21])*2**1+int(m[22])*2**0)/8388608
        
        e1 = h20_bin[5:8]
        e2 = h20_bin[9:14]
        e = e1+e2
        exponent = int(e,2)
        sign = (-1)**(int(h20_bin[4],2))
        
        h20_ppb = sign*(2**(exponent-127))*(1+mantissa)
    
        return(str(h20_ppb))
    except:
        pass





#####GUI
LARGEST_FONT = ("Helvetica", 36, 'bold')
LARGE_FONT = ("Helvetica", 28, 'bold')
SMALL_FONT = ("Helvetica", 20, 'bold')
SMALLEST_FONT = ("Helvetica", 8)
style.use("dark_background")
global o2IsWorking
o2IsWorking = True
global h2oIsWorking
h2oIsWorking = True
f1 = Figure(figsize=(8,5),dpi=100)
#f2 = Figure(figsize=(10,2),dpi=100)
a1 = f1.add_subplot(111)
#a2 = f2.add_subplot(111)
#f2.subplots_adjust(left=0.12, right=0.95, bottom =0.2, top=0.9)
f1.subplots_adjust(left=0.12, right=0.95, bottom =0.2, top=0.9)
o2_dataList = ""
h2o_dataList = ""
recording=False
start_time=datetime.now()
global start_timee
start_timee = start_time.strftime("%m_%d_%y_%I:%M:%S")
h2odata_max = 10
h2odata_min = 0
#global start_timet
#start_timet = StringVar(value = '0')
#start_timet.set(start_time.strftime("%I:%M %p"))
## All the field names for test details

#RPiReader class unpacks and shows pages. Also holds the window title and icon. Any new pages need to be added to self.frames{}

class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Splash")
        self.gambar = Image.open('qam_logo_transparent(1.5k).png')
        self.imgSplash = ImageTk.PhotoImage(self.gambar)
        self.img = Label(self, image=self.imgSplash, bg="grey25")
        self.img.image = self.imgSplash
        self.img.grid(row=1,column=1, sticky=N)
        self.update()
        


class RPiReader(tk.Tk):
    def __init__(self, *args, **kwargs): #args are variables. kwargs are keyboard args (dictionarys and such)
    
        tk.Tk.__init__(self, *args, **kwargs)
        self.withdraw()
        splash=Splash(self)
        
        #tk.Tk.iconbitmap(self,default="qam_logo_icon.ico")
        tk.Tk.wm_title(self, "Pi-View")
        
        time.sleep(0.5)
        splash.destroy()
        self.deiconify()
        container = tk.Frame(self, bg='black')
        self.geometry("1400x900+300+200")
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = { }
        
        for F in (StartPage, PageOne, FieldsScreen):
            
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column = 0, sticky="nsew")
        
        self.show_frame(StartPage)
        
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()

        
        
        


#StartPage appears first. contains

        
class StartPage(tk.Frame):
    recording = False
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=1600, height=1100)
        label1 = tk.Label(self, text="Quality Assurance Management Inc.", font=LARGEST_FONT)
        label1.place(x=150,y=5)
        label1.config(bg="grey25", fg=QAM_GREEN)
        
        self.configure(background="grey25")
        
        
        
        with open('Header_default.csv', newline='') as t:
                headreader = csv.reader(t)
                global header_list
                header_list = []
                for row in headreader:
                        header_list.append(row[0])
        
        global title
        global client
        global location
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
        location = header_list[2]
        test_gas = header_list[3]
        source_gas = header_list[4]
        technician = header_list[5]
        system_flow = header_list[6]
        comments = header_list[7]
        deltaf_serial = header_list[8]
        deltaf_cal = header_list[9]
        deltaf_flow = header_list[10]
        deltaf_spec = header_list[11]
        tracer_serial = header_list[12]
        tracer_cal = header_list[13]
        tracer_flow = header_list[14]
        tracer_spec = header_list[15]
        
        paddx = 15
        paddy = 15
        
        global var2
        var2 = StringVar()
        var2.set('radBoth')
        def h2o_selected():
            print(var2.get())

        def o2_selected():
            print(var2.get())
            #Label(self, text="Select the O2 CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="SpringGreen3", justify="right").place(x=75,y=188)
            #Button(self, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="white", command=open2).place(height=50, width=125, x=450, y=185)
            #Label(self, text="Select the H2O CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="Grey50", justify="right").place(x=69,y=108)
            #Button(self, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="Grey25", state="disabled").place(height=50, width=125, x=450, y=102)

        def both_selected():
            print(var2.get())
            #Label(self, text="Select the H2O CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="DeepSkyBlue", justify="right").place(x=69,y=108)
            #Button(self, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="white", command=open1).place(height=50, width=125, x=450, y=102)
            #Label(self, text="Select the O2 CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="SpringGreen3", justify="right").place(x=75,y=188)
            #Button(self, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="white", command=open2).place(height=50, width=125, x=450, y=185)

        s1 = ttk.Style()
        s1.configure("h2o.TRadiobutton", font=('Century Gothic',17,'bold'), background="#404040", foreground="#00BFFF")
        s1.configure("o2.TRadiobutton", font=('Century Gothic',17,'bold'), background="#404040", foreground="#00CD66")
        s1.configure("both.TRadiobutton", font=('Century Gothic',17,'bold'), background="#404040", foreground="Orange")
        
        

        # Radiobuttons
        rad_h2o = ttk.Radiobutton(self, text="H2O", style="h2o.TRadiobutton", variable=var2, value="radH2O", command=h2o_selected).place(x=500,y=200)
        rad_o2 = ttk.Radiobutton(self, text="O2", style="o2.TRadiobutton", variable=var2, value="radO2", command=o2_selected).place(x=600,y=200)
        rad_both = ttk.Radiobutton(self, text="Both", style="both.TRadiobutton", variable=var2, value="radBoth", command=both_selected).place(x=680,y=200)
        
        global img
        gambar = Image.open('graph.png')
        imgSplash = ImageTk.PhotoImage(gambar)
        img = Label(self, image=imgSplash, bg="grey25")
        img.image = imgSplash
        img.place(x=400,y=80)
        
        photo = PhotoImage(file = 'chart-line-solid.png')
        photoimage = photo.subsample(3,3)
        
        button1 = tk.Button(self, text="Modify Report",bg=QAM_GREEN,fg="White",font=('calibri',36,'bold'),borderwidth = '1', width = 18, height = 2, command=manage_pdf)
        button1.place(x=20,y=420)
        
        button1 = tk.Button(self, text="Set Fields",bg="Orange",fg="White",font=('calibri',36,'bold'),borderwidth = '1', width = 17, height = 2, command=lambda: controller.show_frame(FieldsScreen))
        button1.place(x=500,y=420)
        
        #Start Recording Button => starts the record() function and shows test screen                                                ###work in progress###
        #button2 = tk.Button(self, text="Start Test",bg="grey15",fg="grey75",font=LARGE_FONT, command=self.start_show_test)
        #button2.grid(row=2,column=4)
        
        
        
        
        #This one just goes to test screen... see above work in progress
        button1 = tk.Button(self, text="Begin Test",bg="Red",fg="White",font=('calibri',36,'bold'),borderwidth = '1', width = 37, height = 2, command=lambda: controller.show_frame(PageOne))
        button1.place(x=20,y=660)
        
        #Show Current O2 Reading
        label13 = tk.Label(self, text="Current O2:", font=SMALL_FONT)
        label13.place(x=50,y=150)
        label13.config(bg="grey25",fg="white")
        
        global currento2
        currento2 = StringVar(value=0)
        label14 = tk.Label(self,textvariable=currento2, width=10,bg="grey35",fg="#00CD66", font=('calibri',20,'bold'))
        label14.place(x=230,y=150)
        
        #Show Current H2O Reading
        label13 = tk.Label(self, text="Current H2O:", font=SMALL_FONT)
        label13.place(x=50,y=210)
        label13.config(bg="grey25",fg="white")
        
        global currenth2o
        currenth2o = StringVar(value=0)
        label14 = tk.Label(self,textvariable=currenth2o, width=10,bg="grey35",fg="#00BFFF", font=('calibri',20,'bold'))
        label14.place(x=230,y=210)
        
        button1 = tk.Button(self, text="Equipment Controls",bg="#2FA4FF",fg="White",font=('calibri',36,'bold'),borderwidth = '1', width = 37, height = 2, command=equipment_controls)
        button1.place(x=20,y=540)
     
        
def equipment_controls():
        paddx = 15
        paddy = 15
        top5 = Toplevel()
        top5.title("Equipment Controls")
        top5.geometry("1000x500")
        top5.configure(background="grey25")
        
        button1 = tk.Button(top5, text="Back",bg="Orange",fg="White",font=('calibri',36,'bold'),borderwidth = '1', width = 14, height = 1, command=top5.destroy)
        button1.place(x=500, y=5)
        
        label1 = tk.Label(top5, text="Meeco Tracer 2",bg="grey25", fg = QAM_GREEN, font=LARGEST_FONT)
        label1.place(x=100, y=100)
        
        #Show Current Meeco Mode
        label1 = tk.Label(top5, text="Current Mode:",bg="grey25", fg = "grey85", font=LARGE_FONT)
        label1.place(x=50, y=160)
        
        global currentMode
        label14 = tk.Label(top5,textvariable=currentMode, width=10,bg="grey25",fg="red", font=('calibri',20,'bold'))
        label14.place(x=320, y=170)
        
        button1 = tk.Button(top5, text="Service",bg="grey15",fg="grey85",font=SMALL_FONT, command=lambda: write_serial_int(True,0))
        button1.place(x=500,y=160)
        
        button1 = tk.Button(top5, text="Inert",bg="grey15",fg="grey85",font=SMALL_FONT, command=lambda: write_serial_int(True,1))
        button1.place(x=650,y=160)
        
        label14 = tk.Label(top5,text="Upper Band:",bg="grey25",fg="white", font=SMALL_FONT)
        label14.place(x=50,y=250)
        
        label14 = tk.Label(top5,text="Lower Band:",bg="grey25",fg="white", font=SMALL_FONT)
        label14.place(x=400,y=250)
        
        global currentUpper
        label14 = tk.Label(top5,textvariable=currentUpper, width=10,bg="grey25",fg="grey85", font=('calibri',20,'bold'))
        label14.place(x=220,y=255)
        
        global currentLower
        label14 = tk.Label(top5,textvariable=currentLower, width=10,bg="grey25",fg="grey85", font=('calibri',20,'bold'))
        label14.place(x=570,y=255)
        
        label14 = tk.Label(top5,text="Set Upper Band:", width=20,bg="grey25",fg="white", font=SMALL_FONT)
        label14.place(x=5,y=320)
        
        label14 = tk.Label(top5,text="Set Lower Band:", width=20,bg="grey25",fg="white", font=SMALL_FONT)
        label14.place(x=350,y=320)
        
        upper_band = DoubleVar()
        textbox = ttk.Entry(top5,width=10, textvariable = upper_band)
        textbox.place(x=270,y=330)
        
        lower_band = DoubleVar()
        textbox = ttk.Entry(top5,width=10, textvariable = lower_band)
        textbox.place(x=615,y=330)
        
        button1 = tk.Button(top5, text="Set Bands",bg="grey15",fg="grey75",font=LARGE_FONT, command=lambda: write_upperandlower(upper_band.get(),lower_band.get()))
        button1.place(x=130,y=400)
        

        
class FieldsScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #label1 = tk.Label(self, text="Field Screen", font=LARGEST_FONT)
        #label1.grid(row=1,column=1, columnspan=3, sticky=N)
        #label1.config(bg="grey25", fg="#7fa6a3")
        
        self.configure(background="grey25")
        
        self.gambar = Image.open('qam_logo_transparent(2).png')
        self.imgSplash = ImageTk.PhotoImage(self.gambar)
        self.img = Label(self, image=self.imgSplash, bg="grey25")
        self.img.image = self.imgSplash
        self.img.place(x=400, y=10)
        
        def update_fields():
                global header_list
                header_list =[]
                header_list.append(title.get())
                header_list.append(client.get())
                header_list.append(location.get())
                header_list.append(test_gas.get())
                header_list.append(source_gas.get())
                header_list.append(technician.get())
                header_list.append(system_flow.get())
                header_list.append(comments.get())
                header_list.append(deltaf_serial.get())
                header_list.append(deltaf_cal.get())
                header_list.append(deltaf_flow.get())
                header_list.append(deltaf_spec.get())
                header_list.append(tracer_serial.get())
                header_list.append(tracer_cal.get())
                header_list.append(tracer_flow.get())
                header_list.append(tracer_spec.get())
                with open('/home/pi/Desktop/JoelPi/Header_default.csv', 'w+',newline='') as d:
                    writer4 = csv.writer(d)
                    for row in header_list:
                        writer4.writerow([row])
                    d.close()
        
        button1 = tk.Button(self, text="Back",bg="grey15",fg="grey75",font=LARGE_FONT, command=lambda: controller.show_frame(StartPage))
        button1.place(x=20,y=20)
        
        #button1 = tk.Button(self, text="Update Fields",bg="grey15",fg="grey75",font=LARGE_FONT, command=update_fields)
        #button1.grid(row=4,column=4)
        
        with open('Header_default.csv', newline='') as t:
                headreader = csv.reader(t)
                global header_list
                header_list = []
                for row in headreader:
                        header_list.append(row[0])
        
        paddx = 380
        paddy = 75
        
        ####Document fields (title, client, etc)
        # title entry
        label3 = tk.Label(self, text="Test Point ID:", font=SMALL_FONT)
        label3.place(x=20,y=100)
        label3.config(bg="grey25",fg="#7fa6a3")
        
        global title
        self.title = StringVar(self, value=header_list[0])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.title)
        self.textbox.place(x=20,y=140)
        title = self.title
        
        # client entry
        label4 = tk.Label(self, text="Client:", font=SMALL_FONT)
        label4.place(x=20,y=100+paddy)
        label4.config(bg="grey25",fg="#7fa6a3")
        
        global client
        self.client = StringVar(self, value=header_list[1])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.client)
        self.textbox.place(x=20,y=140+paddy)
        client = self.client
        
        # Location entry
        label4 = tk.Label(self, text="Location:", font=SMALL_FONT)
        label4.place(x=20,y=100+paddy*2)
        label4.config(bg="grey25",fg="#7fa6a3")
        
        global location
        self.location = StringVar(self, value=header_list[2])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.location)
        self.textbox.place(x=20,y=140+paddy*2)
        location = self.location
        
        # test gas entry
        label5 = tk.Label(self, text="Test Gas:", font=SMALL_FONT)
        label5.place(x=20,y=100+paddy*3)
        label5.config(bg="grey25",fg="#7fa6a3")
        
        global test_gas
        self.test_gas = StringVar(self, value=header_list[3])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.test_gas)
        self.textbox.place(x=20,y=140+paddy*3)
        test_gas = self.test_gas
        
        # source gas entry
        label6 = tk.Label(self, text="Source Gas:", font=SMALL_FONT)
        label6.place(x=20,y=100+paddy*4)
        label6.config(bg="grey25",fg="#7fa6a3")
        
        global source_gas
        self.source_gas = StringVar(self, value=header_list[4])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.source_gas)
        self.textbox.place(x=20,y=140+paddy*4)
        source_gas = self.source_gas
        
        # technician entry
        label7 = tk.Label(self, text="Technician:", font=SMALL_FONT)
        label7.place(x=20,y=100+paddy*5)
        label7.config(bg="grey25",fg="#7fa6a3")
        
        global technician
        self.technician = StringVar(self, value=header_list[5])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.technician)
        self.textbox.place(x=20,y=140+paddy*5)
        technician = self.technician
        
        # system flow entry
        label8 = tk.Label(self, text="System Flow:", font=SMALL_FONT)
        label8.place(x=20,y=100+paddy*6)
        label8.config(bg="grey25",fg="#7fa6a3")
        
        global system_flow
        self.system_flow = StringVar(self, value=header_list[6])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.system_flow)
        self.textbox.place(x=20,y=140+paddy*6)
        system_flow = self.system_flow
        
        #comments entry
        label9 = tk.Label(self, text="Comments:", font=SMALL_FONT)
        label9.place(x=20,y=100+paddy*7)
        label9.config(bg="grey25",fg="#7fa6a3")
        
        global comments
        self.comments = StringVar(self, value=header_list[7])
        self.textbox = ttk.Entry(self,width=40, textvariable = self.comments)
        self.textbox.place(x=20,y=140+paddy*7)
        comments = self.comments
        
        ### analyser info entries
        ## delta f info entry
        #deltaf serial number entry
        label10 = tk.Label(self, text="Delta-F", font=LARGE_FONT)
        label10.place(x=20+paddx,y=300)
        label10.config(bg="grey25", fg="white")
        
        label10 = tk.Label(self, text="Delta-F Serial #:", font=SMALL_FONT)
        label10.place(x=20+paddx,y=340)
        label10.config(bg="grey25",fg="#7fa6a3")
        
        global deltaf_serial
        self.deltaf_serial = StringVar(self, value=header_list[8])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.deltaf_serial)
        self.textbox.place(x=20+paddx,y=380)
        deltaf_serial = self.deltaf_serial
        
        #deltaf calibration date entry
        label11 = tk.Label(self, text="Delta-F Calibration Date:", font=SMALL_FONT)
        label11.place(x=20+paddx,y=340+paddy)
        label11.config(bg="grey25",fg="#7fa6a3")
        
        global deltaf_cal
        self.deltaf_cal = StringVar(self, value=header_list[9])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.deltaf_cal)
        self.textbox.place(x=20+paddx,y=380+paddy)
        deltaf_cal = self.deltaf_cal
        
        #instrument flow entry
        label12 = tk.Label(self, text="Delta-F Flow:", font=SMALL_FONT)
        label12.place(x=20+paddx,y=340+paddy*2)
        label12.config(bg="grey25",fg="#7fa6a3")
        
        global deltaf_flow
        self.deltaf_flow = StringVar(self, value=header_list[10])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.deltaf_flow)
        self.textbox.place(x=20+paddx,y=380+paddy*2)
        deltaf_flow = self.deltaf_flow
        
        #instrument specification
        label13 = tk.Label(self, text="Specification", font=SMALL_FONT)
        label13.place(x=20+paddx,y=340+paddy*3)
        label13.config(bg="grey25",fg="#7fa6a3")
        
        global deltaf_spec
        self.deltaf_spec = StringVar(self, value=header_list[11])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.deltaf_spec)
        self.textbox.place(x=20+paddx,y=380+paddy*3)
        deltaf_spec = self.deltaf_spec
        
        ## tracer2 info entry
        #tracer2 serial number entry
        label10 = tk.Label(self, text="Meeco Tracer2", font=LARGE_FONT)
        label10.place(x=20+paddx*2,y=300)
        label10.config(bg="grey25", fg="white")
        
        label10 = tk.Label(self, text="Instrument Serial #:", font=SMALL_FONT)
        label10.place(x=20+paddx*2,y=340)
        label10.config(bg="grey25",fg="#7fa6a3")
        
        global tracer_serial
        self.tracer_serial = StringVar(self, value=header_list[12])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.tracer_serial)
        self.textbox.place(x=20+paddx*2,y=380)
        tracer_serial = self.tracer_serial
        
        #tracer2 calibration date entry
        label11 = tk.Label(self, text="Instrument Calibration Date:", font=SMALL_FONT)
        label11.place(x=20+paddx*2,y=340+paddy)
        label11.config(bg="grey25",fg="#7fa6a3")
        
        global tracer_cal
        self.tracer_cal = StringVar(self, value=header_list[13])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.tracer_cal)
        self.textbox.place(x=20+paddx*2,y=380+paddy)
        tracer_cal = self.tracer_cal
        
        #instrument flow entry
        label12 = tk.Label(self, text="Instrument Flow:", font=SMALL_FONT)
        label12.place(x=20+paddx*2,y=340+paddy*2)
        label12.config(bg="grey25",fg="#7fa6a3")
        
        global tracer_flow
        self.tracer_flow = StringVar(self, value=header_list[14])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.tracer_flow)
        self.textbox.place(x=20+paddx*2,y=380+paddy*2)
        tracer_flow = self.tracer_flow
        
        #instrument specification
        label13 = tk.Label(self, text="Specification", font=SMALL_FONT)
        label13.place(x=20+paddx*2,y=340+paddy*3)
        label13.config(bg="grey25",fg="#7fa6a3")
        
        global tracer_spec
        self.tracer_spec = StringVar(self, value=header_list[14])
        self.textbox = ttk.Entry(self,width=20, textvariable = self.tracer_spec)
        self.textbox.place(x=20+paddx*2,y=380+paddy*3)
        tracer_spec = self.tracer_spec
        
        #current o2
        #label13 = tk.Label(self, text="Current H2O:", font=LARGE_FONT)
        #label13.grid(row=13,column=2, padx=paddx,pady=paddy)
        #label13.config(bg="grey25",fg="white")
        
        #label14 = tk.Label(self,textvariable=currento2, width=20,bg="grey35",fg="white", font=SMALL_FONT)
        #label14.grid(row=14, column=3, padx=paddx,pady=paddy)
        
        #current h2o
        #label13 = tk.Label(self, text="Current O2:", font=LARGE_FONT)
        #label13.grid(row=13,column=3, padx=paddx,pady=paddy)
        #label13.config(bg="grey25",fg="white")
        
        #label14 = tk.Label(self,textvariable=currenth2o, width=20,bg="grey35",fg="white", font=SMALL_FONT)
        #label14.grid(row=14, column=2, padx=paddx,pady=paddy)
        
        
        
    
        
        
class PageOne(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #label = tk.Label(self, text="Testing Screen", font=LARGEST_FONT)
        #label.config(bg="grey25", fg="#7fa6a3")
        #label.grid(row=1,column=1,columnspan=2)
        
        self.configure(background="grey25")
        global start_timet
        start_timet = StringVar(value = '0')
        start_timet.set(start_time.strftime("%I:%M %p"))
        global directory
        directory = '/home/pi/Desktop/JoelPi'
        
        global o2data_max
        global o2data_min
        self.o2data_max = 0
        self.o2data_min = 0
        
        global canvas1
        #Oxygen DeltaF Graph
        canvas1 = FigureCanvasTkAgg(f1, self)
        canvas1.draw()
        canvas1.get_tk_widget().place(x=5,y=5)
        
        #Moisture Tracer Graph
        #canvas2 = FigureCanvasTkAgg(f2, self)
        #canvas2.draw()
        #canvas2.get_tk_widget().place(x=5,y=400)
        
        #toolbar = NavigationToolbar2Tk(canvas1,self)
        #toolbar.update()
        #canvas1._tkcanvas.grid(row=8,column=1)
        
        #toolbar = NavigationToolbar2Tk(canvas2,self)
        #toolbar.update()
        #canvas2._tkcanvas.grid(row=3,column=2)
        
        #Stop Recording Button => starts the stop() function
        button3 = tk.Button(self, text="Stop Recording",bg="#D73A3A",fg="grey85",width=16,height = 1, font=('calibri',36,'bold'), command=self.stop)
        button3.place(x=430,y=540)
        
        #Start Recording Button => starts the record() function
        button2 = tk.Button(self, text="Start Recording",bg="#D73A3A",fg="grey85",width=16,height = 1,font=('calibri',36,'bold'), command=self.record)
        button2.place(x=5,y=540)
        
        button1 = tk.Button(self, text="Back",bg="grey15",fg="grey85",width=20, command=lambda: controller.show_frame(StartPage))
        button1.place(x=875,y=440)
        
        #button2 = tk.Button(self, text="PDF",bg="grey15",fg="grey85",width=20, command=lambda: controller.show_frame(PageTwo))
        #button2.grid(row=7,column=3, pady=3, padx=2)
        
        #button2 = tk.Button(self, text="Select File Location",bg="grey15",fg="grey85",width=20, command=self.choose_directory)
        #button2.grid(row=3,column=3, pady=3, padx=2)
        
        #self.label15 = tk.Label(self, text="IDLE", bg="IndianRed",fg="grey85",width=20,height=2, font=('Century Gothic',10,'bold'))
        #self.label15.grid(row=2,column=3, pady=3, padx=2)
        
        self.gambar = Image.open('qam_logo_transparent(200).png')
        self.imgSplash = ImageTk.PhotoImage(self.gambar)
        self.img = Label(self, image=self.imgSplash, bg="grey25")
        self.img.image = self.imgSplash
        self.img.place(x=875, y=5)
        
        #Start Time Display
        label13 = tk.Label(self, text="Start Time:", font=SMALL_FONT)
        label13.place(x=875, y=150)
        label13.config(bg="grey25",fg="white")
        
        label14 = tk.Label(self,textvariable=start_timet, width=20,bg="grey25",fg="#FFA500", font=('calibri',20,'bold'))
        label14.place(x=820, y=190)
        
        #current o2
        label13 = tk.Label(self, text="Current O2:", font=SMALL_FONT)
        label13.place(x=875, y=250)
        label13.config(bg="grey25",fg="white")
        
        label14 = tk.Label(self,textvariable=currento2, width=20,bg="grey25",fg="#60D500", font=('calibri',20,'bold'))
        label14.place(x=820, y=290)
        
        #current h2o
        label13 = tk.Label(self, text="Current H2O:", font=SMALL_FONT)
        label13.place(x=875, y=350)
        label13.config(bg="grey25",fg="white")
        
        label14 = tk.Label(self,textvariable=currenth2o, width=20,bg="grey25",fg="#2FA4FF", font=('calibri',20,'bold'))
        label14.place(x=820, y=390)
        
        
    #def idle_on_off(self):
    #    if self.label15['text'] == 'IDLE':
    #        self.label15.configure(text="RECORDING", bg="#7fa6a3")
    #    else:
    #        self.label15.configure(text="IDLE", bg="IndianRed")
        
    def choose_directory(self):
        global directory
        directory = filedialog.askdirectory()
    
    
        
### Start Recording function: writes o2, h20, and time variables to csv files        
    def record(self):
        
        confirm_fields('start')
        #PageOne.idle_on_off(self)
        
        global recording
        red_green = 'green'
        on_off = "Recording"
        recording=True
        
        global start_time
        start_time=datetime.now()
        #print(start_time)
        global start_timee
        start_timee = start_time.strftime("%m_%d_%y_%I:%M:%S")
        start_timet.set(start_time.strftime("%I:%M %p"))
        
        
        global o2dataList
        global h2odataList
        global o2_dataList
        global h2o_dataList
        global x2
        global y2
        global x1
        global y1
        o2_dataList = ''
        h2o_dataList = ''
        
        #x2 = 0
        #y2 = 0
        #x1 = 0
        #y1 = 0
        
        
        
        self.headerFileTitle = "Header"
        path = directory + '/' + str(client.get())+ "_" + str(location.get()) + "_" + str(title.get()) + start_timee
        i=0
        
        os.mkdir(path)
        global pathF
        pathF=str(path)
        with open(os.path.join(path,self.headerFileTitle)+'.csv', 'w+', newline='') as c:
            writer3 = csv.writer(c)
            writer3.writerow([title.get()])
            writer3.writerow([client.get()])
            writer3.writerow([location.get()])
            writer3.writerow([test_gas.get()])
            writer3.writerow([source_gas.get()])
            writer3.writerow([technician.get()])
            writer3.writerow([system_flow.get()])
            writer3.writerow([comments.get()])
            writer3.writerow([deltaf_serial.get()])
            writer3.writerow([deltaf_cal.get()])
            writer3.writerow([deltaf_flow.get()])
            writer3.writerow([deltaf_spec.get()])
            writer3.writerow([tracer_serial.get()])
            writer3.writerow([tracer_cal.get()])
            writer3.writerow([tracer_flow.get()])
            writer3.writerow([tracer_spec.get()])
            writer3.writerow([start_timee])
            c.flush()
            
            
    def stop(self):
        
        global recording
        recording = False
        #PageOne.idle_on_off(self)
        global stop_time
        stop_time= datetime.now()
        
        global o2MeanValue
        o2MeanValue = str(round(mean(o2Valuelist),2))
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
        h2oMeanValue = str(round(mean(h2oValuelist),2))
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
        
        global pathF
        self.headerFileTitle = "Header"
        path = directory + '/' + str(title.get())
        with open(os.path.join(pathF,self.headerFileTitle)+'.csv', 'a', newline='') as c:
            writer3 = csv.writer(c)
            writer3.writerow([stop_time])
            writer3.writerow([o2MeanValue])
            writer3.writerow([o2MaxValue])
            writer3.writerow([o2FinalValue])
            writer3.writerow([h2oMeanValue])
            writer3.writerow([h2oMaxValue])
            writer3.writerow([h2oFinalValue])
            c.close()
            
        global h2otest_passing
        h2o_limit = re.findall(r"[-+]?\d*\.*\d+",header_list[15])
        h2o_limit = float(h2o_limit[0])
        
        if float(h2oFinalValue) < h2o_limit:
                h2otest_passing = True
        if float(h2oFinalValue) > h2o_limit:
                h2otest_passing = False
        
        global o2test_passing
        o2_limit = re.findall(r"[-+]?\d*\.*\d+",header_list[15])
        o2_limit = float(o2_limit[0])
        
        if float(o2FinalValue) < o2_limit:
                o2test_passing = True
        if float(o2FinalValue) > o2_limit:
                o2test_passing = False
        
        
        with open('/home/pi/Desktop/JoelPi/Header_default.csv', 'w+',newline='') as d:
            writer4 = csv.writer(d)
            for row in header_list:
                writer4.writerow([row])
            d.close()
        
        if o2test_passing == True and h2otest_passing == True:
                pathG = os.path.join(os.path.dirname(pathF),"P_"+os.path.basename(pathF))
                print(pathG)
        else:
                pathG = os.path.join(os.path.dirname(pathF),"F_"+os.path.basename(pathF))
        os.rename(pathF,pathG)
        pathF = pathG
        confirm_fields(start_stop='stop')
            
        
def confirm_fields(start_stop):
        
        top4 = Toplevel()
        top4.title("Confirm Fields")
        label1 = tk.Label(top4, text="Field Screen", font=LARGEST_FONT)
        label1.grid(row=1,column=1, columnspan=3, sticky=N)
        label1.config(bg="grey25", fg="#7fa6a3")
        
        top4.configure(background="grey25")
        
        top4.gambar = Image.open('qam_logo_transparent(2).png')
        top4.imgSplash = ImageTk.PhotoImage(top4.gambar)
        top4.img = Label(top4, image=top4.imgSplash, bg="grey25")
        top4.img.image = top4.imgSplash
        top4.img.grid(row=16,column=4,rowspan = 4, sticky=S)
        
        
        
        def update_fields():
                path = directory + '/' + str(client.get())+ "_" + str(location.get()) + "_" + str(title.get()) + start_timee
                i=0
                
                #os.mkdir(path)
                global pathG
                pathG=str(path)
                
                os.chdir("/home/pi/Desktop/JoelPi")
                global pathF
                os.rename(pathF,pathG)
                pathF = pathG
                
                global header_list
                header_list =[]
                header_list.append(title.get())
                header_list.append(client.get())
                header_list.append(location.get())
                header_list.append(test_gas.get())
                header_list.append(source_gas.get())
                header_list.append(technician.get())
                header_list.append(system_flow.get())
                header_list.append(comments.get())
                header_list.append(deltaf_serial.get())
                header_list.append(deltaf_cal.get())
                header_list.append(deltaf_flow.get())
                header_list.append(deltaf_spec.get())
                header_list.append(tracer_serial.get())
                header_list.append(tracer_cal.get())
                header_list.append(tracer_flow.get())
                header_list.append(tracer_spec.get())
                
                
                with open('/home/pi/Desktop/JoelPi/Header_default.csv', 'w+',newline='') as d:
                    writer4 = csv.writer(d)
                    for row in header_list:
                        writer4.writerow([row])
                    d.close()
                    
                    
                with open(os.path.join(pathG,'Header.csv'), 'w+', newline='') as c:
                    writer3 = csv.writer(c)
                    writer3.writerow([title.get()])
                    writer3.writerow([client.get()])
                    writer3.writerow([location.get()])
                    writer3.writerow([test_gas.get()])
                    writer3.writerow([source_gas.get()])
                    writer3.writerow([technician.get()])
                    writer3.writerow([system_flow.get()])
                    writer3.writerow([comments.get()])
                    writer3.writerow([deltaf_serial.get()])
                    writer3.writerow([deltaf_cal.get()])
                    writer3.writerow([deltaf_flow.get()])
                    writer3.writerow([deltaf_spec.get()])
                    writer3.writerow([tracer_serial.get()])
                    writer3.writerow([tracer_cal.get()])
                    writer3.writerow([tracer_flow.get()])
                    writer3.writerow([tracer_spec.get()])
                    if start_stop == 'stop':
                            writer3.writerow([start_timee])
                            writer3.writerow([stop_time])
                            writer3.writerow([o2MeanValue])
                            writer3.writerow([o2MaxValue])
                            writer3.writerow([o2FinalValue])
                            writer3.writerow([h2oMeanValue])
                            writer3.writerow([h2oMaxValue])
                            writer3.writerow([h2oFinalValue])
                    c.flush()
                    c.close()
        
        button1 = tk.Button(top4, text="Back",bg="grey15",fg="grey75",font=LARGE_FONT, command=top4.destroy)
        button1.grid(row=3,column=4)
        
        button1 = tk.Button(top4, text="Update Fields",bg="grey15",fg="grey75",font=LARGE_FONT, command=update_fields)
        button1.grid(row=4,column=4)
        
        with open('Header_default.csv', newline='') as t:
                headreader = csv.reader(t)
                global header_list
                header_list = []
                for row in headreader:
                        header_list.append(row[0])
        
        paddx = 2
        paddy = 2
        
        ####Document fields (title, client, etc)
        # title entry
        label3 = tk.Label(top4, text="Test Point ID:", font=SMALL_FONT)
        label3.grid(row=2,column=1, padx=paddx,pady=paddy)
        label3.config(bg="grey25",fg="white")
        
        global title
        top4.title = StringVar(top4, value=header_list[0])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.title)
        top4.textbox.grid(row=3,column=1, padx=paddx,pady=paddy)
        title = top4.title
        
        # client entry
        label4 = tk.Label(top4, text="Client:", font=SMALL_FONT)
        label4.grid(row=4,column=1, padx=paddx,pady=paddy)
        label4.config(bg="grey25",fg="white")
        
        global client
        top4.client = StringVar(top4, value=header_list[1])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.client)
        top4.textbox.grid(row=5,column=1, padx=paddx,pady=paddy)
        client = top4.client
        
        # client entry
        label4 = tk.Label(top4, text="Location:", font=SMALL_FONT)
        label4.grid(row=4,column=1, padx=paddx,pady=paddy)
        label4.config(bg="grey25",fg="white")
        
        global location
        top4.location = StringVar(top4, value=header_list[2])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.location)
        top4.textbox.grid(row=5,column=1, padx=paddx,pady=paddy)
        location = top4.location
        
        # test gas entry
        label5 = tk.Label(top4, text="Test Gas:", font=SMALL_FONT)
        label5.grid(row=6,column=1, padx=paddx,pady=paddy)
        label5.config(bg="grey25",fg="white")
        
        global test_gas
        top4.test_gas = StringVar(top4, value=header_list[3])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.test_gas)
        top4.textbox.grid(row=7,column=1, padx=paddx,pady=paddy)
        test_gas = top4.test_gas
        
        # source gas entry
        label6 = tk.Label(top4, text="Source Gas:", font=SMALL_FONT)
        label6.grid(row=8,column=1, padx=paddx,pady=paddy)
        label6.config(bg="grey25",fg="white")
        
        global source_gas
        top4.source_gas = StringVar(top4, value=header_list[4])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.source_gas)
        top4.textbox.grid(row=9,column=1, padx=paddx,pady=paddy)
        source_gas = top4.source_gas
        
        # technician entry
        label7 = tk.Label(top4, text="Technician:", font=SMALL_FONT)
        label7.grid(row=10,column=1, padx=paddx,pady=paddy)
        label7.config(bg="grey25",fg="white")
        
        global technician
        top4.technician = StringVar(top4, value=header_list[5])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.technician)
        top4.textbox.grid(row=11,column=1, padx=paddx,pady=paddy)
        technician = top4.technician
        
        # system flow entry
        label8 = tk.Label(top4, text="System Flow:", font=SMALL_FONT)
        label8.grid(row=12,column=1, padx=paddx,pady=paddy)
        label8.config(bg="grey25",fg="white")
        
        global system_flow
        top4.system_flow = StringVar(top4, value=header_list[6])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.system_flow)
        top4.textbox.grid(row=13,column=1, padx=paddx,pady=paddy)
        system_flow = top4.system_flow
        
        #comments entry
        label9 = tk.Label(top4, text="Comments:", font=SMALL_FONT)
        label9.grid(row=14,column=1, padx=paddx,pady=paddy)
        label9.config(bg="grey25",fg="white")
        
        global comments
        top4.comments = StringVar(top4, value=header_list[7])
        top4.textbox = ttk.Entry(top4,width=40, textvariable = top4.comments)
        top4.textbox.grid(row=15,column=1, padx=paddx,pady=paddy)
        comments = top4.comments
        
        ### analyser info entries
        ## delta f info entry
        #deltaf serial number entry
        label10 = tk.Label(top4, text="Servomex", font=LARGE_FONT)
        label10.grid(row=2,column=2, padx=paddx,pady=paddy)
        label10.config(bg="grey25", fg="#7fa6a3")
        
        label10 = tk.Label(top4, text="Instrument Serial #:", font=SMALL_FONT)
        label10.grid(row=3,column=2, padx=paddx,pady=paddy)
        label10.config(bg="grey25",fg="white")
        
        global deltaf_serial
        top4.deltaf_serial = StringVar(top4, value=header_list[8])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.deltaf_serial)
        top4.textbox.grid(row=4,column=2, padx=paddx,pady=paddy)
        deltaf_serial = top4.deltaf_serial
        
        #deltaf calibration date entry
        label11 = tk.Label(top4, text="Instrument Calibration Date:", font=SMALL_FONT)
        label11.grid(row=5,column=2, padx=paddx,pady=paddy)
        label11.config(bg="grey25",fg="white")
        
        global deltaf_cal
        top4.deltaf_cal = StringVar(top4, value=header_list[9])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.deltaf_cal)
        top4.textbox.grid(row=6,column=2, padx=paddx,pady=paddy)
        deltaf_cal = top4.deltaf_cal
        
        #instrument flow entry
        label12 = tk.Label(top4, text="Instrument Flow:", font=SMALL_FONT)
        label12.grid(row=7,column=2, padx=paddx,pady=paddy)
        label12.config(bg="grey25",fg="white")
        
        global deltaf_flow
        top4.deltaf_flow = StringVar(top4, value=header_list[10])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.deltaf_flow)
        top4.textbox.grid(row=8,column=2, padx=paddx,pady=paddy)
        deltaf_flow = top4.deltaf_flow
        
        #instrument specification
        label13 = tk.Label(top4, text="Specification", font=SMALL_FONT)
        label13.grid(row=9,column=2, padx=paddx,pady=paddy)
        label13.config(bg="grey25",fg="white")
        
        global deltaf_spec
        top4.deltaf_spec = StringVar(top4, value=header_list[11])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.deltaf_spec)
        top4.textbox.grid(row=10,column=2, padx=paddx,pady=paddy)
        deltaf_spec = top4.deltaf_spec
        
        ## tracer2 info entry
        #tracer2 serial number entry
        label10 = tk.Label(top4, text="Meeco Tracer2", font=LARGE_FONT)
        label10.grid(row=2,column=3, padx=paddx,pady=paddy)
        label10.config(bg="grey25", fg="#7fa6a3")
        
        label10 = tk.Label(top4, text="Instrument Serial #:", font=SMALL_FONT)
        label10.grid(row=3,column=3, padx=paddx,pady=paddy)
        label10.config(bg="grey25",fg="white")
        
        global tracer_serial
        top4.tracer_serial = StringVar(top4, value=header_list[12])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.tracer_serial)
        top4.textbox.grid(row=4,column=3, padx=paddx,pady=paddy)
        tracer_serial = top4.tracer_serial
        
        #tracer2 calibration date entry
        label11 = tk.Label(top4, text="Instrument Calibration Date:", font=SMALL_FONT)
        label11.grid(row=5,column=3, padx=paddx,pady=paddy)
        label11.config(bg="grey25",fg="white")
        
        global tracer_cal
        top4.tracer_cal = StringVar(top4, value=header_list[13])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.tracer_cal)
        top4.textbox.grid(row=6,column=3, padx=paddx,pady=paddy)
        tracer_cal = top4.tracer_cal
        
        #instrument flow entry
        label12 = tk.Label(top4, text="Instrument Flow:", font=SMALL_FONT)
        label12.grid(row=7,column=3, padx=paddx,pady=paddy)
        label12.config(bg="grey25",fg="white")
        
        global tracer_flow
        top4.tracer_flow = StringVar(top4, value=header_list[14])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.tracer_flow)
        top4.textbox.grid(row=8,column=3, padx=paddx,pady=paddy)
        tracer_flow = top4.tracer_flow
        
        #instrument specification
        label13 = tk.Label(top4, text="Specification", font=SMALL_FONT)
        label13.grid(row=9,column=3, padx=paddx,pady=paddy)
        label13.config(bg="grey25",fg="white")
        
        global tracer_spec
        top4.tracer_spec = StringVar(top4, value=header_list[15])
        top4.textbox = ttk.Entry(top4,width=20, textvariable = top4.tracer_spec)
        top4.textbox.grid(row=10,column=3, padx=paddx,pady=paddy)
        tracer_spec = top4.tracer_spec
        
        
        if start_stop == 'stop':
                #Mean Moisture Value
                label13 = tk.Label(top4, text="Moisture Mean Value:", font=SMALL_FONT)
                label13.grid(row=13,column=2, padx=paddx,pady=paddy)
                label13.config(bg="grey25",fg="white")
                
                label14 = tk.Label(top4,textvariable=h2oMeanValueVar, width=20,bg="grey35",fg="white", font=SMALL_FONT)
                label14.grid(row=14, column=2, padx=paddx,pady=paddy)
                
                #Max Moisture Value
                label13 = tk.Label(top4, text="Mositure Max Value", font=SMALL_FONT)
                label13.grid(row=15,column=2, padx=paddx,pady=paddy)
                label13.config(bg="grey25",fg="white")
                
                label14 = tk.Label(top4,textvariable=h2oMaxValueVar, width=20,bg="grey35",fg="white", font=SMALL_FONT)
                label14.grid(row=16, column=2, padx=paddx,pady=paddy)
                
                #Final Moisture Value
                label13 = tk.Label(top4, text="Moisture Final Value", font=SMALL_FONT)
                label13.grid(row=17,column=2, padx=paddx,pady=paddy)
                label13.config(bg="grey25",fg="white")
                
                label14 = tk.Label(top4,textvariable=h2oFinalValueVar, width=20,bg="grey35",fg="white", font=SMALL_FONT)
                label14.grid(row=18, column=2, padx=paddx,pady=paddy)
                
                #Mean Oxygen Value
                label13 = tk.Label(top4, text="Oxygen Mean Value:", font=SMALL_FONT)
                label13.grid(row=13,column=3, padx=paddx,pady=paddy)
                label13.config(bg="grey25",fg="white")
                
                label14 = tk.Label(top4,textvariable=o2MeanValueVar, width=20,bg="grey35",fg="white", font=SMALL_FONT)
                label14.grid(row=14, column=3, padx=paddx,pady=paddy)
                
                #Max Oxygen Value
                label13 = tk.Label(top4, text="Oxygen Max Value", font=SMALL_FONT)
                label13.grid(row=15,column=3, padx=paddx,pady=paddy)
                label13.config(bg="grey25",fg="white")
                
                label14 = tk.Label(top4,textvariable=o2MaxValueVar, width=20,bg="grey35",fg="white", font=SMALL_FONT)
                label14.grid(row=16, column=3, padx=paddx,pady=paddy)
                
                #Final Oxygen Value
                label13 = tk.Label(top4, text="Oxygen Final Value", font=SMALL_FONT)
                label13.grid(row=17,column=3, padx=paddx,pady=paddy)
                label13.config(bg="grey25",fg="white")
                
                label14 = tk.Label(top4,textvariable=o2FinalValueVar, width=20,bg="grey35",fg="white", font=SMALL_FONT)
                label14.grid(row=18, column=3, padx=paddx,pady=paddy)
        
            
            
def animateo2(i):   #### animation function. despite the name it actually animates both o2 and h2o. 
                        #  it also functions to save csv files if the variable 'recording' is set to TRUE
        global currentMode
        currentMode=StringVar()
        #meecoMode = int(write_serial_int(False,0))                                      #### comment out for random data###
        meecoMode = 0
        if meecoMode == 1:
                currentMode.set('Inert')
        if meecoMode == 0:
                currentMode.set('Service')

        global currentUpper
        global currentLower
        currentUpper=StringVar()
        currentLower=StringVar()
        #currentUpper.set(round(float(raw_to_ppb(read_serial_float(15))),2))        #### comment out for random data###
        #currentLower.set(round(float(raw_to_ppb(read_serial_float(16))),2))        #### comment out for random data###
        currentUpper.set(random.random())
        currentLower.set(random.random())
        

        #### data gathering for o2 graph
        global o2IsWorking
        if o2IsWorking == False:
                for x in range(2):
                        try:
                                #o2 = get_O2()                                      #### comment out for random data###
                                o2 = random.random()*100
                                o2 = round(float(o2),2)
                                o2IsWorking = True
                                break
                        except:
                                time.sleep(0.08)
                                o2 = 0
                                o2IsWorking = False
        if o2IsWorking == True:
                for x in range(5):
                        try:
                                #o2 = get_O2()                                      #### comment out for random data###
                                o2 = random.random()*100
                                o2 = round(float(o2),2)
                                o2IsWorking = True
                                break
                        except:
                                time.sleep(0.08)
                                o2 = 0
                                o2IsWorking = False
                
        currento2.set(o2)
        #if o2IsWorking==True:
        #        print('o2 is working')
        #if o2IsWorking==False:
        #        print('o2 is fucked')
        try:
                if o2data_max<o2:
                        o2data_max = o2
                if o2data_min>o2:
                        o2data_min = o2
        except:
                o2data_max = 0
                o2data_min = 0
                if o2data_max<o2:
                        o2data_max = o2
                if o2data_min>o2:
                        o2data_min = o2
        o2time = datetime.now()-start_time
        global o2_dataList
        global o2dataList
        o2_dataList = o2_dataList + '\n' + str(round((o2time.total_seconds())/60,2))+ ',' + str(o2)
        
        o2dataList = o2_dataList.split('\n')
        #print(o2_dataList)
        o2dataList.pop(0)
        initial_tick = o2dataList[0].split(',')
        #print(initial_tick[1])
        o2dataList[0] = "0,"+initial_tick[1]
        #print(o2dataList)
        o2xList = []
        o2yList = []
        global x1
        global y1
        for eachLine in o2dataList:
            if len(str(eachLine)) > 1:
                x1, y1 = eachLine.split(',')
                o2xList.append(float(x1))
                o2yList.append(float(y1))
        #o2xList[0] = 0

        #### data gathering for h2o graph
        global h2oIsWorking
        if h2oIsWorking == False:
                for x in range(2):
                        try:
                                #h2o = raw_to_ppb(get_h20())                                      #### comment out for random data###
                                h2o = random.random()*100
                                h2o = round(float(h2o),2)
                                h2oIsWorking=True
                                break
                        except:
                                time.sleep(0.08)
                                h2oIsWorking = False
                                h2o=0
        if h2oIsWorking == True:
                for x in range(5):
                        try:
                                #h2o = raw_to_ppb(get_h20())                                      #### comment out for random data###
                                h2o = random.random()*100
                                h2o = round(float(h2o),2)
                                h2oIsWorking = True
                                break
                        except:
                                time.sleep(0.08)
                                h2oIsWorking = False
                                h2o=0

        if h2o<0:
                h2o=0
        currenth2o.set(h2o)
        #if h2oIsWorking==True:
        #        print('h2o is working')
        #if h2oIsWorking==False:
        #        print('h2o is fucked')
        global h2odata_max
        global h2odata_min
        if h2odata_max<h2o:
                h2odata_max = h2o
        if h2odata_min>h2o:
                h2odata_min = h2o
        print(h2odata_max)
        h2otime = datetime.now()-start_time
        global h2o_dataList
        global h2odataList
        h2o_dataList = h2o_dataList + '\n' + str(round((h2otime.total_seconds())/60,2))+ ',' + str(h2o)
        h2odataList = h2o_dataList.split('\n')
        h2odataList.pop(0)
        initial_h2otick = h2odataList[0].split(',')
        #print(initial_h2otick[1])
        h2odataList[0] = "0,"+initial_h2otick[1]
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
        a1.clear()
        a1.ticklabel_format(useOffset=False)
        if var2.get() == 'radO2':
                a1.set_ylim(min((0, o2data_min+o2data_min*0.1)), max((10, o2data_max+o2data_max*0.1)))
                a1.plot(o2xList,o2yList,'#60D500')
                if o2IsWorking == True:
                        a1.set_title("Oxygen (PPB) vs Time (minutes)")
                else:
                        a1.set_title("Check DeltaF Connections")
                a1.set_xlabel('Time (minutes)')
                a1.set_ylabel('Oxygen (PPB)')
        if var2.get() == 'radBoth':
                #print('radBoth')
                a1.set_ylim(min((0, o2data_min*1.1, h2odata_min*1.1)), max((10, o2data_max*1.1, h2odata_max*1.1)))
                a1.plot(o2xList,o2yList,'#60D500')
                a1.plot(h2oxList, h2oyList,'#2FA4FF')
                if o2IsWorking ==True and h2oIsWorking ==True:
                        a1.set_title("PPB vs Time (minutes)")
                if o2IsWorking ==False:
                        a1.set_title("Check DeltaF Connection")
                if h2oIsWorking ==False:
                        a1.set_title("Check Meeco Connection")
                a1.set_xlabel("Time (minutes)")
                a1.set_ylabel("PPB")
                
        if var2.get() == 'radH2O':
                a1.set_ylim(min((0, h2odata_min+h2odata_min*0.1)), max((10, h2odata_max+h2odata_max*0.1)))
                a1.plot(h2oxList, h2oyList,'#2FA4FF')
                if h2oIsWorking == True:
                        a1.set_title("Moisture (PPB) vs Time (minutes)")
                else:
                        a1.set_title("Check Meeco Connection")
                a1.set_xlabel('Time (minutes)')
                a1.set_ylabel('Moisture (PPB)')
        
        
        f1.savefig('graph.png')
        basewidth = 535
        imgg = Image.open('graph.png')
        wpercent = (basewidth/float(imgg.size[0]))
        hsize = int((float(imgg.size[1])*float(wpercent)*1))
        imgg = imgg.resize((basewidth,hsize), Image.ANTIALIAS)
        imgg.save('graph.png')
        img2 = ImageTk.PhotoImage(Image.open('graph.png'))
        img.configure(image=img2)
        img.image = img2
        
        
        
        o2fileTitle = "O2"

        if recording == True:
            global o2Valuelist
            o2Valuelist = []
            with open(os.path.join(pathF,o2fileTitle)+'.csv', 'w+', newline='') as o:
                writer1 = csv.writer(o, escapechar=' ',quoting=csv.QUOTE_NONE)
                for eachLine in o2dataList:
                        writer1.writerow([eachLine])
                        everyLine = eachLine.split(",")
                        o2Valuelist.append(float(everyLine[1]))
                #print(o2Valuelist)
                
                o.flush()


        h2ofileTitle = "H2O"


        if recording == True:
            global h2oValuelist
            h2oValuelist = []
            with open(os.path.join(pathF,h2ofileTitle)+'.csv', 'w+', newline='') as h:
                writer2 = csv.writer(h, escapechar=' ',quoting=csv.QUOTE_NONE)
                for eachLine in h2odataList:
                        writer2.writerow([eachLine])
                        everyLine = eachLine.split(",")
                        h2oValuelist.append(float(everyLine[1]))
                
                h.flush()





def manage_pdf():
        # Find and print the current working directory
        os.getcwd()
        print(os.getcwd())

        # Filepath for Windows testing 
        #os.chdir("//Mac/Home/Downloads") #-------(CHANGE THIS TO WORK WITH THE CURRENT COMPUTER)
        #print(os.getcwd())

        # Filepath for Mac testing 
        #os.chdir("/Users/Work/Downloads") #-------(CHANGE THIS TO WORK WITH THE CURRENT COMPUTER)
        #print(os.getcwd())
        
        # Filepath for Pi (Linux) testing 
        os.chdir("/home/pi/Desktop/JoelPi") #-------(CHANGE THIS TO WORK WITH THE CURRENT COMPUTER)
        print(os.getcwd())

        global TestingIncValue
        TestingIncValue = 1    #-------(THIS CONTROLS HOW OFTEN DATA IS COLLECTED AND PLOTTED)

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
            folder = filedialog.askdirectory()
            print(folder)
            os.chdir(folder)
            try:
                for file in os.listdir(folder):
                    try:
                        if file.startswith("H2O") and file.endswith(".csv"):
                            H2Ocsv = file
                            print("H2O file found")
                            
                        elif file.startswith("O2") and file.endswith(".csv"):
                            O2csv = file
                            print("O2 file found")

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

            global top 
            top=Toplevel()
            # Width and height for the Tk root window
            w = 1030
            h = 720
            # This gets the current screen width and height
            ws = top.winfo_screenwidth()
            hs = top.winfo_screenheight()
            # Calculate the x and y coordinates based on the current screen size
            sx = (ws/2) - (w/2)
            sy = (hs/2) - (h/2)
            # Open the root window in the middle of the screen
            top.geometry('%dx%d+%d+%d' % (w, h, sx, sy))
            top.resizable(False,False)
            top.config(bg="Grey25")
            global ff1
            global ff2
            ff1 = Figure(figsize=(5,6), dpi=100, facecolor=(0.40,0.51,0.46))
            ff2 = Figure(figsize=(5,6), dpi=100, facecolor=(0.40,0.51,0.46))
            a1 = ff1.add_subplot(211,facecolor=(0.25,0.25,0.25))
            a2 = ff2.add_subplot(211,facecolor=(0.25,0.25,0.25))
            a1new = ff1.add_subplot(212,facecolor=(0.25,0.25,0.25))
            a2new = ff2.add_subplot(212,facecolor=(0.25,0.25,0.25))
            
            # These are for setting the x value to 0 and incrementing by the predetermined value
            x0h = []
            x0o = []

            # These are standard lists that hold the values from the CSV files
            x1 = []
            x2 = []    
            y1 = []
            y2 = []
            global headerdata
            headerdata = []

            # No CSV files found
            if H2Ocsv is None and O2csv is None:
                print("No H2O or O2 CSV file found.")
                tk.Button(top, text="OK", fg="white", activeforeground="white", bg="#d73a3a", activebackground="#d94d4d", font=("century gothic",50,"bold"), command=BackToSelect).place(height=150,width=880,x=75,y=495)
                tk.Label(top, text="Selection Error:", fg="#d73a3a", bg="Grey25", font=("Century Gothic",85, "bold"), justify="center", wraplength=900).place(x=90,y=75)
                tk.Label(top, text="The folder you selected does not contain an O2 or H2O CSV file.", fg="white", bg="Grey25", font=("Century Gothic",40, "bold"), justify="center", wraplength=850).place(x=95,y=270)


            # ------------------------------------------------------------------------------ #
            #                               O2 GRAPH ONLY                                    #
            # ------------------------------------------------------------------------------ #
            elif H2Ocsv is None:
                print("H2O file NOT found")
                global o2Path
                o2Path = os.path.join(folder,O2csv)
                # Using the O2 path, transfer data from O2csv file into corresponding lists
                with open(o2Path) as csvO2:
                    plots = csv.reader(csvO2, delimiter=',')
                    for row in plots:
                        x2.append(float(row[0]))
                        y2.append(float(row[1]))
                
                #This handles the O2 header file
                o2HeaderPath = os.path.join(folder,headercsv)
                with open(o2HeaderPath) as csvHeaderO2:
                    o2headernew = csv.reader(csvHeaderO2, delimiter=',')
                    for row in o2headernew:
                        headerdata.append(row[1])
                    print(headerdata)

                    # This is the current threshold for O2 tests
                    O2spec = 10.00
                    # This pulls the final (ending) value from the O2 test
                    lastO2 = (len(y2)-1)
                    # This checks the final value of the test and determines whether it passed or failed.
                    if y2[lastO2] > O2spec:
                        print("O2 Test Result: Out of Spec.")
                        # This is used to determine the filename
                        global FailedTest
                        FailedTest = True
                    else:
                        print("O2 Test Result: Within Spec.")
                        FailedTest = False

                if FailedTest:
                    print("Failed Test: Unable to edit")
                    tk.Button(top, text="OK", fg="white", activeforeground="white", bg="#d73a3a", activebackground="#d94d4d", font=("century gothic",50,"bold"), command=BackToSelect).place(height=150,width=880,x=75,y=495)
                    tk.Label(top, text="Selection Error:", fg="#d73a3a", bg="Grey25", font=("Century Gothic",85, "bold"), justify="center", wraplength=900).place(x=90,y=75)
                    tk.Label(top, text="The folder you selected contains a failed test.", fg="white", bg="Grey25", font=("Century Gothic",45, "bold"), justify="center", wraplength=800).place(x=180,y=265)
                else:
                    #Creates the figure, canvas, and button
                    f2 = plt.figure(figsize=(10.1,6), dpi=100, facecolor=(0.40,0.51,0.46))
                    a2 = f2.add_subplot(211,facecolor=(0.25,0.25,0.25))
                    canvas1 = FigureCanvasTkAgg(f2, master=top)
                    canvas1.get_tk_widget().place(x=10,y=10)
                    tk.Button(top, text="Save as PDF", fg="white", activeforeground="white", bg="#d73a3a", activebackground="#d94d4d", font=("century gothic",30,"bold"), command=exportO2).place(height=90,width=500,x=520,y=620)
                    tk.Button(top, text="Back to Select", fg="white", activeforeground="white", bg="#ff9500", activebackground="#ffab34", font=("century gothic",30,"bold"), command=BackToSelect).place(height=90,width=500,x=10,y=620)
                    
                    #setting the top (original) graph
                    a2.plot(x2, y2, color='#60d500', linewidth=4)
                    a2.grid(True)
                    a2.set_title('Click and drag to select new O2', fontsize=25, pad=12)
                    a2.set_xlabel('Time in minutes', color="white")
                    a2.set_ylabel('PPB', color="white")
                    a2.tick_params(colors='w')
                    f2.subplots_adjust(top=.90, hspace=0.3)
                    a2.title.set_color('w')

                    #setting up bottom (edited) graph
                    global ax2
                    ax2 = f2.add_subplot(212,facecolor=(0.25,0.25,0.25))
                    line2, = ax2.plot(x2, y2, color='#60d500', linewidth=4)
                    ax2.grid(True)
                    ax2.set_xlabel('Time in minutes', color="white")
                    ax2.set_ylabel('PPB', color="white")
                    ax2.tick_params(colors='w')

                    def onselect(xmin, xmax):
                        indmin, indmax = np.searchsorted(x2, (xmin, xmax))
                        indmax = min(len(x2) - 1, indmax)
                        global O2x
                        global O2y
                        O2x = x2[indmin:indmax]
                        O2y = y2[indmin:indmax]
                        line2.set_data(O2x, O2y)
                        ax2.set_xlim(O2x[0]-1, O2x[-1]+1)
                        ax2.set_ylim(min(O2y)-1, max(O2y)+1)
                        f2.canvas.draw_idle()

                        def incremental_range(start, stop, inc):
                            value = start
                            while value < stop:
                                yield value
                                value += inc
                        global O2xReset
                        O2xReset = list(incremental_range(0,len(O2x),TestingIncValue))

                        global o2AvgEdit
                        o2AvgEdit = str(round(mean(O2y),2))
                        global o2MaxEdit
                        o2MaxEdit = str(round(max(O2y),2))
                        global o2FinalEdit
                        o2FinalEdit = str(round(O2y[-1],2))

                        # save
                        np.savetxt("O2.out", np.c_[O2x, O2y])
                    # set useblit True on gtkagg for enhanced performance
                    span = SpanSelector(a2, onselect, 'horizontal', useblit=True,
                                        rectprops=dict(alpha=0.5, facecolor='#678176'))
                    plt.show()
                
                

            # ------------------------------------------------------------------------------ #
            #                                H2O GRAPH ONLY                                  #
            # ------------------------------------------------------------------------------ #
            elif O2csv is None:
                print("O2 file NOT found")
                global h2oPath
                h2oPath = os.path.join(folder,H2Ocsv)
                # Using the H2O path, transfer data from H2Ocsv file into corresponding lists
                with open(h2oPath) as csvH2O:
                    plots = csv.reader(csvH2O, delimiter=',')
                    for row in plots:
                        x1.append(float(row[0]))
                        y1.append(float(row[1]))
                
                #This handles the h2O header file
                h2oHeaderPath = os.path.join(folder,headercsv)
                with open(h2oHeaderPath) as csvHeaderH2O:
                    h2oheadernew = csv.reader(csvHeaderH2O, delimiter=',')
                    for row in h2oheadernew:
                        headerdata.append(row[1])
                    print(headerdata)

                    # This is the current threshold for O2 tests
                    H2Ospec = 10.00
                    # This pulls the final (ending) value from the O2 test
                    lastH2O = (len(y1)-1)
                    # This checks the final value of the test and determines whether it passed or failed.
                    if y1[lastH2O] > H2Ospec:
                        print("H2O Test Result: Out of Spec.")
                        # This is used to determine the filename
                        FailedTest = True
                    else:
                        print("H2O Test Result: Within Spec.")
                        FailedTest = False
                if FailedTest:
                    print("Failed Test: Unable to edit")
                    tk.Button(top, text="OK", fg="white", activeforeground="white", bg="#d73a3a", activebackground="#d94d4d", font=("century gothic",50,"bold"), command=BackToSelect).place(height=150,width=880,x=75,y=495)
                    tk.Label(top, text="Selection Error:", fg="#d73a3a", bg="Grey25", font=("Century Gothic",85, "bold"), justify="center", wraplength=900).place(x=90,y=75)
                    tk.Label(top, text="The folder you selected contains a failed test.", fg="white", bg="Grey25", font=("Century Gothic",45, "bold"), justify="center", wraplength=800).place(x=180,y=265)

                else:
                    #Creates the figure, canvas, and button
                    ff1 = plt.figure(figsize=(10.1,6), dpi=100, facecolor=(0.40,0.51,0.46))
                    a1 = ff1.add_subplot(211,facecolor=(0.25,0.25,0.25))
                    canvas2 = FigureCanvasTkAgg(ff1, master=top)
                    canvas2.get_tk_widget().place(x=10,y=10)
                    tk.Button(top, text="Save as PDF", fg="white", activeforeground="white", bg="#d73a3a", activebackground="#d94d4d", font=("century gothic",30,"bold"), command=exportH2O).place(height=90,width=500,x=520,y=620)
                    tk.Button(top, text="Back to Select", fg="white", activeforeground="white", bg="#ff9500", activebackground="#ffab34", font=("century gothic",30,"bold"), command=BackToSelect).place(height=90,width=500,x=10,y=620)
                    
                    #setting the top (original) graph
                    a1.plot(x1, y1, color='DodgerBlue', linewidth=4)
                    a1.grid(True)
                    a1.set_title('Click and drag to select new H2O', fontsize=25, pad=12)
                    a1.set_xlabel('Time in minutes', color="white")
                    a1.set_ylabel('PPB', color="white")
                    a1.tick_params(colors='w')
                    ff1.subplots_adjust(top=.90, hspace=0.3)
                    a1.title.set_color('w')

                    #setting up bottom (edited) graph
                    ax1 = ff1.add_subplot(212,facecolor=(0.25,0.25,0.25))
                    line1, = ax1.plot(x1, y1, color='DodgerBlue',linewidth=4)
                    ax1.grid(True)
                    ax1.set_xlabel('Time in minutes', color="white")
                    ax1.set_ylabel('PPB', color="white")
                    ax1.tick_params(colors='w')

                    def onselect(xmin, xmax):
                        indmin, indmax = np.searchsorted(x1, (xmin, xmax))
                        indmax = min(len(x1) - 1, indmax)
                        global H2Ox
                        global H2Oy
                        H2Ox = x1[indmin:indmax]
                        H2Oy = y1[indmin:indmax]
                        line1.set_data(H2Ox, H2Oy)
                        ax1.set_xlim(H2Ox[0]-1, H2Ox[-1]+1)
                        ax1.set_ylim(min(H2Oy)-1, max(H2Oy)+1)
                        ff1.canvas.draw_idle()

                        def incremental_range(start, stop, inc):
                            value = start
                            while value < stop:
                                yield value
                                value += inc
                        global H2OxReset
                        H2OxReset = list(incremental_range(0,len(H2Ox),TestingIncValue))

                        global h2oAvgEdit
                        h2oAvgEdit = str(round(mean(H2Oy),2))
                        global h2oMaxEdit
                        h2oMaxEdit = str(round(max(H2Oy),2))
                        global h2oFinalEdit
                        h2oFinalEdit = str(round(H2Oy[-1],2))

                        # save
                        np.savetxt("H2O.out", np.c_[H2Ox, H2Oy])
                    # set useblit True on gtkagg for enhanced performance
                    span = SpanSelector(a1, onselect, 'horizontal', useblit=True,
                                        rectprops=dict(alpha=0.5, facecolor='#678176'))
                    plt.show()
                

            # ------------------------------------------------------------------------------ #
            #                           BOTH GRAPHS (H2O AND O2)                             #
            # ------------------------------------------------------------------------------ #
            else:
                #This handles the H2O file and graph
                h2oPath = os.path.join(folder,H2Ocsv)
                with open(h2oPath) as csvH2O:
                    plots = csv.reader(csvH2O, delimiter=',')
                    for row in plots:
                        x1.append(float(row[0]))
                        y1.append(float(row[1]))

                # This handles the header file
                dualHeaderPath = os.path.join(folder,headercsv)
                with open(dualHeaderPath) as csvHeaderBoth:
                    bothheadernew = csv.reader(csvHeaderBoth, delimiter=',')
                    for row in bothheadernew:
                        headerdata.append(row[0])
                    print(headerdata)                
                    
                    # This is the current threshold for O2 tests
                    H2Ospec = 10.00
                    # This pulls the final (ending) value from the O2 test
                    lastH2O = (len(y1)-1)
                    # This checks the final value of the test and determines whether it passed or failed.
                    if y1[lastH2O] > H2Ospec:
                        print("H2O Test Result: Out of Spec.")
                        # This is used to determine the filename
                        FailedH2OTest = True
                    else:
                        print("H2O Test Result: Within Spec.")
                        FailedH2OTest = False

                #This handles the O2 file and graph
                o2Path = os.path.join(folder,O2csv)
                with open(o2Path) as csvO2:
                    plots = csv.reader(csvO2, delimiter=',')
                    for row in plots:
                        x2.append(float(row[0]))
                        y2.append(float(row[1]))

                    # This is the current threshold for O2 tests
                    O2spec = 10.00
                    # This pulls the final (ending) value from the O2 test
                    lastO2 = (len(y2)-1)
                    # This checks the final value of the test and determines whether it passed or failed.
                    if y2[lastO2] > O2spec:
                        print("O2 Test Result: Out of Spec.")
                        # This is used to determine the filename
                        FailedO2Test = True
                    else:
                        print("O2 Test Result: Within Spec.")
                        FailedO2Test = False

                if FailedH2OTest is True and FailedO2Test is True:
                    print("Both Tests Failed")
                    tk.Button(top, text="OK", fg="white", activeforeground="white", bg="#d73a3a", activebackground="#d94d4d", font=("century gothic",50,"bold"), command=BackToSelect).place(height=150,width=880,x=75,y=495)
                    tk.Label(top, text="Selection Error:", fg="#d73a3a", bg="Grey25", font=("Century Gothic",85, "bold"), justify="center", wraplength=900).place(x=90,y=75)
                    tk.Label(top, text="The folder you selected contains two failed tests.", fg="white", bg="Grey25", font=("Century Gothic",45, "bold"), justify="center", wraplength=800).place(x=155,y=265)

                elif FailedH2OTest:
                    #Creates the figure, canvas, and button
                    f2 = plt.figure(figsize=(10.1,5.6), dpi=100, facecolor=(0.40,0.51,0.46))
                    a2 = f2.add_subplot(211,facecolor=(0.25,0.25,0.25))
                    canvas1 = FigureCanvasTkAgg(f2, master=top)
                    canvas1.get_tk_widget().place(x=10,y=50)
                    tk.Button(top, text="Save as PDF", fg="white", activeforeground="white", bg="#d73a3a", activebackground="#d94d4d", font=("century gothic",30,"bold"), command=exportO2).place(height=90,width=500,x=520,y=620)
                    tk.Button(top, text="Back to Select", fg="white", activeforeground="white", bg="#ff9500", activebackground="#ffab34", font=("century gothic",30,"bold"), command=BackToSelect).place(height=90,width=500,x=10,y=620)
                    tk.Label(top, text="The         test concluded beyond the acceptable limit and therefore cannot be edited.", fg="#ff9500", bg="grey25", font=("century gothic",19, "bold")).place(x=15,y=7)
                    tk.Label(top, text="H2O", fg="DodgerBlue", bg="grey25", font=("century gothic",19, "bold")).place(x=65,y=7)

                    #setting the top (original) graph
                    a2.plot(x2, y2, color='#60d500', linewidth=2)
                    a2.grid(True)
                    a2.set_title('Click and drag to select new O2', fontsize=25, pad=12)
                    a2.set_xlabel('Time in minutes', color="white")
                    a2.set_ylabel('PPB', color="white")
                    a2.tick_params(colors='w')
                    f2.subplots_adjust(top=.90, hspace=0.3)
                    a2.title.set_color('w')

                    #setting up bottom (edited) graph
                    ax2 = f2.add_subplot(212,facecolor=(0.25,0.25,0.25))
                    line2, = ax2.plot(x2, y2, color='#60d500', linewidth=2)
                    ax2.grid(True)
                    ax2.set_xlabel('Time in minutes', color="white")
                    ax2.set_ylabel('PPB', color="white")
                    ax2.tick_params(colors='w')

                    def onselect(xmin, xmax):
                        indmin, indmax = np.searchsorted(x2, (xmin, xmax))
                        indmax = min(len(x2) - 1, indmax)
                        global O2x
                        global O2y
                        O2x = x2[indmin:indmax]
                        O2y = y2[indmin:indmax]
                        line2.set_data(O2x, O2y)
                        ax2.set_xlim(O2x[0]-1, O2x[-1]+1)
                        ax2.set_ylim(min(O2y)-1, max(O2y)+1)
                        f2.canvas.draw_idle()

                        def incremental_range(start, stop, inc):
                            value = start
                            while value < stop:
                                yield value
                                value += inc
                        global O2xReset
                        O2xReset = list(incremental_range(0,len(O2x),TestingIncValue))
                        

                        # save
                        np.savetxt("O2.out", np.c_[O2x, O2y])
                    # set useblit True on gtkagg for enhanced performance
                    span = SpanSelector(a2, onselect, 'horizontal', useblit=True,
                                        rectprops=dict(alpha=0.5, facecolor='#678176'))
                    plt.show()


                elif FailedO2Test:
                    ff1 = plt.figure(figsize=(10.1,5.6), dpi=100, facecolor=(0.40,0.51,0.46))
                    a1 = ff1.add_subplot(211,facecolor=(0.25,0.25,0.25))
                    canvas2 = FigureCanvasTkAgg(ff1, master=top)
                    canvas2.get_tk_widget().place(x=10,y=50)
                    tk.Button(top, text="Save as PDF", fg="white", activeforeground="white", bg="#d73a3a", activebackground="#d94d4d", font=("century gothic",30,"bold"), command=exportH2O).place(height=90,width=500,x=520,y=620)
                    tk.Button(top, text="Back to Select", fg="white", activeforeground="white", bg="#ff9500", activebackground="#ffab34", font=("century gothic",30,"bold"), command=BackToSelect).place(height=90,width=500,x=10,y=620)
                    tk.Label(top, text="The       test concluded beyond the acceptable limit and therefore cannot be edited.", fg="#ff9500", bg="grey25", font=("century gothic",19, "bold")).place(x=24,y=7)
                    tk.Label(top, text="O2", fg="#60d500", bg="grey25", font=("century gothic",19, "bold")).place(x=75,y=7)

                    #setting the top (original) graph
                    a1.plot(x1, y1, color='DodgerBlue', linewidth=2)
                    a1.grid(True)
                    a1.set_title('Click and drag to select new H2O', fontsize=25, pad=12)
                    a1.set_xlabel('Time in minutes', color="white")
                    a1.set_ylabel('PPB', color="white")
                    a1.tick_params(colors='w')
                    ff1.subplots_adjust(top=.90, hspace=0.3)
                    a1.title.set_color('w')

                    #setting up bottom (edited) graph
                    ax1 = ff1.add_subplot(212,facecolor=(0.25,0.25,0.25))
                    line1, = ax1.plot(x1, y1, color='DodgerBlue', linewidth=2)
                    ax1.grid(True)
                    ax1.set_xlabel('Time in minutes', color="white")
                    ax1.set_ylabel('PPB', color="white")
                    ax1.tick_params(colors='w')

                    def onselect(xmin, xmax):
                        indmin, indmax = np.searchsorted(x1, (xmin, xmax))
                        indmax = min(len(x1) - 1, indmax)
                        global H2Ox
                        global H2Oy
                        H2Ox = x1[indmin:indmax]
                        H2Oy = y1[indmin:indmax]
                        line1.set_data(H2Ox, H2Oy)
                        ax1.set_xlim(H2Ox[0]-1, H2Ox[-1]+1)
                        ax1.set_ylim(min(H2Oy)-1, max(H2Oy)+1)
                        ff1.canvas.draw_idle()

                        def incremental_range(start, stop, inc):
                            value = start
                            while value < stop:
                                yield value
                                value += inc
                        global H2OxReset
                        H2OxReset = list(incremental_range(0,len(H2Ox),TestingIncValue))

                        global h2oAvgEdit
                        h2oAvgEdit = str(round(mean(H2Oy),2))
                        global h2oMaxEdit
                        h2oMaxEdit = str(round(max(H2Oy),2))
                        global h2oFinalEdit
                        h2oFinalEdit = str(round(H2Oy[-1],2))

                        # save
                        np.savetxt("H2O.out", np.c_[H2Ox, H2Oy])
                    # set useblit True on gtkagg for enhanced performance
                    span = SpanSelector(a1, onselect, 'horizontal', useblit=True,
                                        rectprops=dict(alpha=0.5, facecolor='#678176'))
                    plt.show()

                else:
                    #Setting up the main figure and canvas for both graphs
                    ff1 = plt.figure(figsize=(10.1,6), dpi=100, facecolor=(0.40,0.51,0.46))
                    a1 = ff1.add_subplot(221,facecolor=(0.25,0.25,0.25))
                    a2 = ff1.add_subplot(222,facecolor=(0.25,0.25,0.25))
                    canvas3 = FigureCanvasTkAgg(ff1, master=top)
                    canvas3.get_tk_widget().place(x=10,y=10)
                    tk.Button(top, text="Save as PDF", fg="white", activeforeground="white", bg="#d73a3a", activebackground="#d94d4d", font=("century gothic",30,"bold"), command=exportBoth).place(height=90,width=500,x=520,y=620)
                    tk.Button(top, text="Back to Select", fg="white", activeforeground="white", bg="#ff9500", activebackground="#ffab34", font=("century gothic",30,"bold"), command=BackToSelect).place(height=90,width=500,x=10,y=620)
                    
                    #Setting up the top H2O graph
                    a1.plot(x1, y1, color='DodgerBlue', linewidth=2)
                    a1.grid(True)
                    a1.set_title('Click and drag to select new H2O',fontsize=15, color="white", pad=15)
                    a1.set_xlabel('Time in minutes', color="white")
                    a1.set_ylabel('PPB', color="white")
                    a1.tick_params(colors='w')
                    ff1.subplots_adjust(top=.90, hspace=0.3)

                    #Setting up the top O2 graph
                    a2.plot(x2, y2, color='#60d500', linewidth=2)
                    a2.grid(True)
                    a2.set_title('Click and drag to select new O2',fontsize=15, color="white", pad=15)
                    a2.set_xlabel('Time in minutes', color="white")
                    a2.set_ylabel('PPB', color="white")
                    a2.tick_params(colors='w')
                    ff1.subplots_adjust(top=.90, hspace=0.3, wspace=0.3)

                    #Setting up bottom (edited) H2O graph
                    ax1 = ff1.add_subplot(223,facecolor=(0.25,0.25,0.25))
                    line1, = ax1.plot(x1, y1, color='DodgerBlue', linewidth=3)
                    ax1.grid(True)
                    ax1.set_xlabel('Time in minutes', color="white")
                    ax1.set_ylabel('PPB', color="white")
                    ax1.tick_params(colors='w')

                    #setting up bottom (edited) graph
                    ax2 = ff1.add_subplot(224,facecolor=(0.25,0.25,0.25))
                    line2, = ax2.plot(x2, y2, color='#60d500', linewidth=3)
                    ax2.grid(True)
                    ax2.set_xlabel('Time in minutes', color="white")
                    ax2.set_ylabel('PPB', color="white")
                    ax2.tick_params(colors='w')

                    #This handles the selection of the H2O graph
                    def onselectH2O(xmin, xmax):
                        H2Omin, H2Omax = np.searchsorted(x1, (xmin, xmax))
                        H2Omax = min(len(x1) - 1, H2Omax)
                        global H2Oxb
                        global H2Oyb
                        H2Oxb = x1[H2Omin:H2Omax]
                        H2Oyb = y1[H2Omin:H2Omax]
                        line1.set_data(H2Oxb, H2Oyb)
                        ax1.set_xlim(H2Oxb[0]-1, H2Oxb[-1]+1)
                        ax1.set_ylim(min(H2Oyb)-1, max(H2Oyb)+1)
                        ff1.canvas.draw_idle()

                        def incremental_range(start, stop, inc):
                            value = start
                            while value < stop:
                                yield value
                                value += inc
                        global H2OxbReset
                        H2OxbReset = list(incremental_range(0,len(H2Oxb),TestingIncValue))

                        global h2obAvgEdit
                        h2obAvgEdit = str(round(mean(H2Oyb),2))
                        global h2obMaxEdit
                        h2obMaxEdit = str(round(max(H2Oyb),2))
                        global h2obFinalEdit
                        h2obFinalEdit = str(round(H2Oyb[-1],2))

                        #Save the selection into a separate .out file
                        np.savetxt("H2O.out", np.c_[H2Oxb, H2Oyb])

                    #This handles the selected portion of the O2 graph
                    def onselectO2(xmin, xmax):
                        O2min, O2max = np.searchsorted(x2, (xmin, xmax))
                        O2max = min(len(x2) - 1, O2max)
                        global O2xb
                        global O2yb
                        O2xb = x2[O2min:O2max]
                        O2yb = y2[O2min:O2max]
                        line2.set_data(O2xb, O2yb)
                        ax2.set_xlim(O2xb[0]-1, O2xb[-1]+1)
                        ax2.set_ylim(min(O2yb)-1, max(O2yb)+1)
                        ff1.canvas.draw_idle()

                        def incremental_range(start, stop, inc):
                            value = start
                            while value < stop:
                                yield value
                                value += inc
                        global O2xbReset
                        O2xbReset = list(incremental_range(0,len(O2xb),TestingIncValue))

                        global o2bAvgEdit
                        o2bAvgEdit = str(round(mean(O2yb),2))
                        global o2bMaxEdit
                        o2bMaxEdit = str(round(max(O2yb),2))
                        global o2bFinalEdit
                        o2bFinalEdit = str(round(O2yb[-1],2))

                        #Save the selection into a separate .out file
                        np.savetxt("O2.out", np.c_[O2xb, O2yb])
                    # set useblit True on gtkagg for enhanced performance
                    spanH2O = SpanSelector(a1, onselectH2O, 'horizontal', useblit=True,
                                        rectprops=dict(alpha=0.5, facecolor='#678176'))
                    spanO2 = SpanSelector(a2, onselectO2, 'horizontal', useblit=True,
                                        rectprops=dict(alpha=0.5, facecolor='#678176'))
                    plt.show()



        #--------------------------------------------------------------------------------#
        #                                  COMMANDS                                      #
        #--------------------------------------------------------------------------------#
        def BackToSelect():
            top.destroy()

        def exportH2O():
            # Export as PNG to attach to the PDF
            fig = plt.figure(figsize=(11.25,6))
            plt.clf()
            plt.plot(H2OxReset, H2Oy, color='royalblue', marker='.', linewidth=5)
            plt.margins(0.01,0.05)
            plt.title('Meeco Moisture Analyzer', fontsize=18, pad=15)
            plt.xlabel('Time in Minutes', fontsize=14)
            plt.ylabel('PPB', fontsize=14)
            plt.grid(True)
            fig.savefig("PDFpltH2O.png")
            plt.close()
            top.destroy()

            pdf = FPDF()
            pdf.set_font("Arial", size=12)
            pdf.add_page()
            pdf.image("PDFpltH2O.png", x=-5, y=26, w=217, h=116)
            pdf.image('/home/pi/Desktop/JoelPi/Logo/QPDFH.png', x=10, y=10, w=186, h=20) #------- ADJUST THE FILEPATH BASED ON WHERE THE IMAGE IS LOCATED
            #pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=10, y=11, w=52, h=20)
            #pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=80, y=7, w=50, h=20)
            #pdf.image('//Mac/Home/Downloads/QAMletter1.jpg', x=135, y=10, w=65, h=21)

            # ADDING HEADER INFO TO THE PDF REPORT
            # Spacing block
            pdf.cell(190,132,ln=2)
            # First block (client, location, serial #)
            pdf.cell(4,10,ln=0)
            pdf.cell(116,7,'Client:', align='L', ln=0)
            pdf.cell(35,7,'Calibration Date:', align='L', ln=1)
            pdf.cell(4,10,ln=0)
            pdf.cell(95,7,str(headerdata[2]),border=1,ln=0)
            pdf.cell(21,7,ln=0)
            pdf.cell(65,7,str(headerdata[13]),border=1,ln=1) #------- ADJUST "headerH2O" TO "hheaderlist" IN FINAL BUILD
            pdf.cell(4,10,ln=0)
            pdf.cell(116,7,'Location:', align='L', ln=0)
            pdf.cell(35,7,'Specification:', align='L', ln=1)
            pdf.cell(4,10,ln=0)
            pdf.cell(95,7,str(headerdata[1]),border=1,ln=0)
            pdf.cell(21,7,ln=0)
            pdf.cell(65,7,str(headerdata[15]),border=1,ln=1)
            pdf.cell(4,10,ln=0)
            pdf.cell(116,7,'Instrument Serial #:', align='L', ln=0)
            pdf.cell(35,7,'Instrument Flow:', align='L', ln=1)
            pdf.cell(4,10,ln=0)
            pdf.cell(95,7,str(headerdata[12]),border=1,ln=0)
            pdf.cell(21,7,ln=0)
            pdf.cell(65,7, str(headerdata[14])+' SLPM',border=1,ln=1)

            # Second block (calibration date, spec., flow)
            pdf.cell(95,11, ln=2)
            pdf.cell(30,7, 'Test Gas:', align='R',ln=0)
            pdf.cell(60,7,str(headerdata[3]),border=1,ln=0)
            pdf.cell(40,7, 'Start Time:', align='R',ln=0)
            pdf.cell(55,7,str(headerdata[16]),border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(30,7, 'Source Gas:', align='R',ln=0)
            pdf.cell(60,7,str(headerdata[4]),border=1,ln=0)
            pdf.cell(40,7, 'Stop Time:', align='R',ln=0)
            pdf.cell(55,7,str(headerdata[17]),border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(30,7,'Test Point ID:', align='R', ln=0)
            pdf.cell(60,7,str(headerdata[0]),border=1,ln=0)
            pdf.cell(40,7, 'Maximum:', align='R',ln=0)
            pdf.cell(55,7,h2oMaxEdit + ' PPB',border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(30,7, 'Technician:', align='R', ln=0)
            pdf.cell(60,7,str(headerdata[5]),border=1,ln=0)
            pdf.cell(40,7, 'Average:', align='R',ln=0)
            pdf.cell(55,7,h2oAvgEdit + ' PPB',border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(30,7, 'System Flow:', align='R', ln=0)
            pdf.cell(60,7,str(headerdata[6])+' SLPM',border=1,ln=0)
            pdf.cell(40,7, 'Final:', align='R',ln=0)
            pdf.cell(55,7,h2oFinalEdit + ' PPB',border=1,ln=1)

            # Third block (comments and approval)
            pdf.cell(195,12,ln=2)
            pdf.cell(25,14, 'Comments:', align='R',ln=0)
            pdf.cell(160,14,str(headerdata[7]),border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(25,10, 'Approval:', align='R',ln=0)
            pdf.cell(160,10,border=1,ln=1)

            # This saves the PDF file to the current working folder
            EditedFilenameH2O = "FinalReport(H2O).pdf"
            pdf.output(EditedFilenameH2O)     #-------(EDIT THIS TO ADJUST THE FINAL ADJUSTED PDF FILENAME)
            pdf=FPDF(orientation='P', unit='in')

            # Open the newly created PDF using Chrome
            chrome_path = ('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
            p = subprocess.Popen([chrome_path, "file:"+folder+"/"+EditedFilenameH2O]) #This uses 'Subprocess' to open the file
            #returncode = p.wait() #This waits for the process to close

        def exportO2():
            # Export as PNG to attach to the PDF
            fig = plt.figure(figsize=(11.25,6))
            plt.clf()
            plt.plot(O2xReset, O2y, color='forestgreen', marker='.', linewidth=5)
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
            pdf.image('/home/pi/Desktop/JoelPi/Logo/QPDFH.png', x=10, y=10, w=186, h=20)     #------- ADJUST THE FILEPATH BASED ON WHERE THE IMAGE IS LOCATED
            #pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=10, y=1, w=55, h=20)
            #pdf.image('//Mac/Home/Downloads/QAMletter1.jpg', x=135, y=10, w=65, h=21)

            # ADDING HEADER INFO TO THE PDF REPORT
            # Spacing block
            pdf.cell(190,132,ln=2)
            # First block (client, location, serial #)
            pdf.cell(4,10,ln=0)
            pdf.cell(116,7,'Client:', align='L', ln=0)
            pdf.cell(35,7,'Calibration Date:', align='L', ln=1)
            pdf.cell(4,10,ln=0)
            pdf.cell(95,7,str(headerdata[2]),border=1,ln=0)
            pdf.cell(21,7,ln=0)
            pdf.cell(65,7,str(headerdata[9]),border=1,ln=1) #------- ADJUST "headerH2O" TO "hheaderlist" IN FINAL BUILD
            pdf.cell(4,10,ln=0)
            pdf.cell(116,7,'Location:', align='L', ln=0)
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
            pdf.cell(30,7, 'Source Gas:', align='R',ln=0)
            pdf.cell(60,7,str(headerdata[4]),border=1,ln=0)
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
            chrome_path = ('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
            p = subprocess.Popen([chrome_path, "file:"+folder+"/"+EditedFilenameO2]) #This uses 'Subprocess' to open the file
            #returncode = p.wait() #This waits for the process to close

        def exportBoth():
            # Export as O2 graph as PNG to attach to the PDF
            figO2 = plt.figure(figsize=(11.25,6))
            plt.clf()
            plt.plot(O2xbReset, O2yb, color='forestgreen', marker='.', linewidth=5)
            plt.margins(0.01,0.05)
            plt.title('Delta F Oxygen Analyzer', fontsize=18, pad=15)
            plt.xlabel('Time in Minutes', fontsize=14)
            plt.ylabel('PPB', fontsize=14)
            plt.grid(True)
            figO2.savefig("PDFpltO2.png")
            plt.close()

            # Export H2O graph as PNG to attach to the PDF
            figH2O = plt.figure(figsize=(11.25,6))
            plt.clf()
            plt.plot(H2OxbReset, H2Oyb, color='royalblue', marker='.', linewidth=5)
            plt.margins(0.01,0.05)
            plt.title('Meeco Moisture Analyzer', fontsize=18, pad=15)
            plt.xlabel('Time in Minutes', fontsize=14)
            plt.ylabel('PPB', fontsize=14)
            plt.grid(True)
            figH2O.savefig("PDFpltH2O.png")
            plt.close()
            top.destroy()

            # Create the first page of the PDF (O2)
            pdf = FPDF()
            pdf.set_font("Arial", size=12)
            pdf.add_page()
            pdf.image("PDFpltO2.png", x=-5, y=26, w=217, h=116)
            pdf.image('//Mac/Home/Downloads/Logo/QPDFH.png', x=10, y=10, w=186, h=20) #------- ADJUST THE FILEPATH BASED ON WHERE THE IMAGE IS LOCATED
            #pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=10, y=11, w=52, h=20)     
            #pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=80, y=7, w=50, h=20)
            #pdf.image('//Mac/Home/Downloads/QAMletter1.jpg', x=135, y=10, w=65, h=21)

            # ADDING HEADER INFO TO THE PDF REPORT
            # Spacing block
            pdf.cell(190,132,ln=2)
            # First block (client, location, serial #)
            pdf.cell(4,10,ln=0)
            pdf.cell(116,7,'Client:', align='L', ln=0)
            pdf.cell(35,7,'Calibration Date:', align='L', ln=1)
            pdf.cell(4,10,ln=0)
            pdf.cell(95,7,str(headerdata[2]),border=1,ln=0)
            pdf.cell(21,7,ln=0)
            pdf.cell(65,7,str(headerdata[9]),border=1,ln=1) #------- ADJUST "headerH2O" TO "hheaderlist" IN FINAL BUILD
            pdf.cell(4,10,ln=0)
            pdf.cell(116,7,'Location:', align='L', ln=0)
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
            pdf.cell(30,7, 'Source Gas:', align='R',ln=0)
            pdf.cell(60,7,str(headerdata[4]),border=1,ln=0)
            pdf.cell(40,7, 'Stop Time:', align='R',ln=0)
            pdf.cell(55,7,str(headerdata[17]),border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(30,7,'Test Point ID:', align='R', ln=0)
            pdf.cell(60,7,str(headerdata[0]),border=1,ln=0)
            pdf.cell(40,7, 'Maximum:', align='R',ln=0)
            pdf.cell(55,7,o2bMaxEdit + ' PPB',border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(30,7, 'Technician:', align='R', ln=0)
            pdf.cell(60,7,str(headerdata[5]),border=1,ln=0)
            pdf.cell(40,7, 'Average:', align='R',ln=0)
            pdf.cell(55,7,o2bAvgEdit + ' PPB',border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(30,7, 'System Flow:', align='R', ln=0)
            pdf.cell(60,7,str(headerdata[6])+' SLPM',border=1,ln=0)
            pdf.cell(40,7, 'Final:', align='R',ln=0)
            pdf.cell(55,7,o2bFinalEdit + ' PPB',border=1,ln=1)

            # Third block (comments and approval)
            pdf.cell(195,12,ln=2)
            pdf.cell(25,14, 'Comments:', align='R',ln=0)
            pdf.cell(160,14,str(headerdata[7]),border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(25,10, 'Approval:', align='R',ln=0)
            pdf.cell(160,10,border=1,ln=1)
            
            # Add the second page of the PDF (H2O)
            pdf.add_page()
            pdf.image("PDFpltH2O.png", x=-5, y=26, w=217, h=116)
            pdf.image('//Mac/Home/Downloads/Logo/QPDFH.png', x=10, y=10, w=186, h=20) #------- ADJUST THE FILEPATH BASED ON WHERE THE IMAGE IS LOCATED
            #pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=10, y=11, w=52, h=20)     
            #pdf.image('//Mac/Home/Downloads/QAMletter2.jpg', x=80, y=7, w=50, h=20)
            #pdf.image('//Mac/Home/Downloads/QAMletter1.jpg', x=135, y=10, w=65, h=21)

            # ADDING HEADER INFO TO THE PDF REPORT
            # Spacing block
            pdf.cell(190,132,ln=2)
            # First block (client, location, serial #)
            pdf.cell(4,10,ln=0)
            pdf.cell(116,7,'Client:', align='L', ln=0)
            pdf.cell(35,7,'Calibration Date:', align='L', ln=1)
            pdf.cell(4,10,ln=0)
            pdf.cell(95,7,str(headerdata[2]),border=1,ln=0)
            pdf.cell(21,7,ln=0)
            pdf.cell(65,7,str(headerdata[13]),border=1,ln=1) #------- ADJUST "headerH2O" TO "hheaderlist" IN FINAL BUILD
            pdf.cell(4,10,ln=0)
            pdf.cell(116,7,'Location:', align='L', ln=0)
            pdf.cell(35,7,'Specification:', align='L', ln=1)
            pdf.cell(4,10,ln=0)
            pdf.cell(95,7,str(headerdata[1]),border=1,ln=0)
            pdf.cell(21,7,ln=0)
            pdf.cell(65,7,str(headerdata[15]),border=1,ln=1)
            pdf.cell(4,10,ln=0)
            pdf.cell(116,7,'Instrument Serial #:', align='L', ln=0)
            pdf.cell(35,7,'Instrument Flow:', align='L', ln=1)
            pdf.cell(4,10,ln=0)
            pdf.cell(95,7,str(headerdata[12]),border=1,ln=0)
            pdf.cell(21,7,ln=0)
            pdf.cell(65,7, str(headerdata[14])+' SLPM',border=1,ln=1)

            # Second block (calibration date, spec., flow)
            pdf.cell(95,11, ln=2)
            pdf.cell(30,7, 'Test Gas:', align='R',ln=0)
            pdf.cell(60,7,str(headerdata[3]),border=1,ln=0)
            pdf.cell(40,7, 'Start Time:', align='R',ln=0)
            pdf.cell(55,7,str(headerdata[16]),border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(30,7, 'Source Gas:', align='R',ln=0)
            pdf.cell(60,7,str(headerdata[4]),border=1,ln=0)
            pdf.cell(40,7, 'Stop Time:', align='R',ln=0)
            pdf.cell(55,7,str(headerdata[17]),border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(30,7,'Test Point ID:', align='R', ln=0)
            pdf.cell(60,7,str(headerdata[0]),border=1,ln=0)
            pdf.cell(40,7, 'Maximum:', align='R',ln=0)
            pdf.cell(55,7,h2obMaxEdit + ' PPB',border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(30,7, 'Technician:', align='R', ln=0)
            pdf.cell(60,7,str(headerdata[5]),border=1,ln=0)
            pdf.cell(40,7, 'Average:', align='R',ln=0)
            pdf.cell(55,7,h2obAvgEdit + ' PPB',border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(30,7, 'System Flow:', align='R', ln=0)
            pdf.cell(60,7,str(headerdata[6])+' SLPM',border=1,ln=0)
            pdf.cell(40,7, 'Final:', align='R',ln=0)
            pdf.cell(55,7,h2obFinalEdit + ' PPB',border=1,ln=1)

            # Third block (comments and approval)
            pdf.cell(195,12,ln=2)
            pdf.cell(25,14, 'Comments:', align='R',ln=0)
            pdf.cell(160,14,str(headerdata[7]),border=1,ln=1)
            pdf.cell(190,2,ln=1)
            pdf.cell(25,10, 'Approval:', align='R',ln=0)
            pdf.cell(160,10,border=1,ln=1)

            # This saves the PDF file to the current working folder
            EditedFilenameBoth = "FinalReport(Both).pdf"
            pdf.output(EditedFilenameBoth)     #-------(EDIT THIS TO ADJUST THE FINAL ADJUSTED PDF FILENAME)
            pdf=FPDF(orientation='P', unit='in')

            # Open the newly created PDF using Chrome
            chrome_path = ('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
            p = subprocess.Popen([chrome_path, "file:"+folder+"/"+EditedFilenameBoth])
            #returncode = p.wait() #This waits for the process to close
                

        #--------------------------------------------------------------------------------#
        #                                  MAIN WINDOW                                   #
        #--------------------------------------------------------------------------------#
        root = tk.Tk()
        root.title('Pi View')
        root.resizable(False, False)
        root.config(bg="Grey25")
        # Width and height for the Tk root window
        w = 1030
        h = 720
        # This gets the current screen width and height
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        # Calculate the x and y coordinates based on the current screen size
        sx = (ws/2) - (w/2)
        sy = (hs/2) - (h/2)
        # Open the root window in the middle of the screen
        root.geometry('%dx%d+%d+%d' % (w, h, sx, sy))

        #--------------------------------------------
        # QAM LOGO
        #--------------------------------------------
        QAMmd = Image.open('QAM.gif')
        imgSplash = ImageTk.PhotoImage(QAMmd, master=root)
        imgg = tk.Label(root, image=imgSplash, borderwidth=0, highlightthickness=0)
        imgg.image = imgSplash
        imgg.place(x=625, y=75)

        #--------------------------------------------
        # BUTTON IMAGES
        #--------------------------------------------
        dashIcon = ImageTk.PhotoImage(file = r"dashboard.png", master=root)
        folderIcon = ImageTk.PhotoImage(file = r"foldersolid.png", master=root)

        tk.Button(root, text="Select Folder", font=("century gothic",50,"bold"), fg="white", activeforeground="white", bg="#ff9500", activebackground="#ffab34", image=folderIcon, compound = "left", padx=30, command=openCSV).place(height=150,width=880,x=75,y=495)
        tk.Button(root, text="Dashboard", font=("Century Gothic",31, "bold"), fg="white", activeforeground="white", bg="#678176", activebackground="#81a6a3", image=dashIcon, compound = "left", padx=25, command=root.destroy).place(height=125, width=350,x=75,y=75)
        tk.Label(root, text="Select the folder with the correct Name, ID, Test Type, and Date", fg="White", bg="Grey25", font=("Century Gothic",40, "bold"), justify="center", wraplength=850).place(x=100,y=280)

        root.mainloop()
        
        
        
        
        
        


        
app = RPiReader()

ani1 = animation.FuncAnimation(f1, animateo2, interval=1000)

app.mainloop()
