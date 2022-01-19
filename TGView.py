#!/usr/bin/python3

import matplotlib

from GlobalConst import dir_TGView, root_path, LARGEST_FONT, LARGER_FONT, LARGE_FONT, SMALL_FONT, SMALLER_FONT, \
    SMALLERR_FONT, SMALLEST_FONT, manageGraphData, s_interface
from component.PopupWindow import PopupWindow
from component.splash import Splash
from component.startpage import StartPage
from modules.AdjustFigure import AdjustFigure
from modules.Util import raw_to_ppb, time_elapsed_string
from modules.serial_interface import SerialInterface

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
from modules.manage_graph import ManageGraph

import math
import textwrap
import shutil
import random

import time
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

#####GUI

# assign font for final PDF graphs
font0 = FontProperties()
font0.set_family('sans-serif')
font0.set_weight('bold')
font0.set_size('xx-large')

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
# global start_timee
# start_timee = start_time.strftime("%m_%d_%y_%I.%M.%S")
global start_timeez
start_timeez = start_time.strftime("%m/%d/%y @ %I:%M %p")

##assign global cycle counts and set to plot the next data grab##
global cycleO2, cycleH2O
cycleH2O = 14
cycleO2 = 14

## set initial plot min/max to 0/10 (this is adjust based on data being plotted)

#
# ####First Toplevel frame to appear is Splash. RPiReader initializes after splash####
# class Splash(tk.Toplevel):
#     def __init__(self, parent):
#         tk.Toplevel.__init__(self, parent, bg='grey25')
#         # w, h = self.winfo_screenwidth(), self.winfo_screenheight()
#         # self.geometry("%dx%d%+d%+d" % (1920, 1080, 0, 0))
#         self.attributes('-type', 'splash')
#         self.geometry("%dx%d%+d%+d" % (1920, 1080, -2, 30))
#         self.title("  Trace Gas View  ")
#
#         self.myIcon = ImageTk.PhotoImage(file=f'{root_path}/TGViewClean.png')
#         self.iconphoto(True, self.myIcon)
#
#         ####### REPLACED the time, date, and logo image with a splash screen image #######
#         splashXField = 550
#         splashYField = 180
#         splashXPadding = 25
#         splashYPadding = 170
#
#         ### Splash Logo
#         self.gambar = Image.open(f'{root_path}/SplashScreen2021.png')
#         self.imgSplash = ImageTk.PhotoImage(self.gambar)
#         self.img = Label(self, image=self.imgSplash, bg="grey25")
#         self.img.image = self.imgSplash
#         # self.img.place(x=splashXField+splashXPadding*4,y=splashYField+splashYPadding)
#         self.img.place(x=0, y=0)
#
#         ### Splash Title - COMMENTED OUT 9/4/2020
#         # label1 = tk.Label(self, text="Trace Gas View", font=("Helvetica", 69, 'bold'))
#         # label1.place(x=splashXField+splashXPadding,y=splashYField)
#         # label1.config(bg="grey25", fg='white')
#
#         ### Current time and date display for Splash Screen - COMMENTED OUT 9/4/2020
#         # label3 = tk.Label(self, text=start_timeez, font=("Helvetica", 58, 'bold'))
#         # label3.place(x=splashXField,y=splashYField+splashYPadding*4.2)
#         # label3.config(bg="grey25", fg='white')
#         self.update()


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

        s_interface.serial_checker()
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
            if s_interface.meecoConnected == True and s_interface.deltafConnected == False:
                writer1.writerow(['DELTAF WAS DISCONNECTED DURING TESTING'])
                writer1.writerow(['LIST DETAILS OF FAILURE BELOW FOR REVIEW'])
            elif s_interface.meecoConnected == False and s_interface.deltafConnected == True:
                writer1.writerow(['MEECO WAS DISCONNECTED DURING TESTING'])
                writer1.writerow(['LIST DETAILS OF FAILURE BELOW FOR REVIEW'])
            elif s_interface.meecoConnected == False and s_interface.deltafConnected == False:
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
        s_interface.write_serial_int(True, 0)
        currentMode.set("Service")

    def change_to_inert():
        s_interface.write_serial_int(True, 1)
        currentMode.set("Inert")

    button1 = tk.Button(top5, text="Service", bg="grey35", activebackground="#2fa4ff", fg="White",
                        activeforeground="white", highlightbackground="#2fa4ff", highlightthickness=2, relief=tk.FLAT,
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





def plot_axes_o2(x_list, y_list, axe):
    marker_style = '.'
    o2x_max = max(x_list)
    if manageGraphData.o2data_min < 0:
        axe.set_ylim(manageGraphData.o2data_min - 10, manageGraphData.o2data_max + 10)
    else:
        axe.set_ylim(0 - 1, manageGraphData.o2data_max + 10)
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
    if manageGraphData.h2odata_min < 0:
        axe.set_ylim(manageGraphData.h2odata_min - 10, h2ox_max_val + 10)
    else:
        axe.set_ylim(0 - 1, manageGraphData.h2odata_max + 10)
    axe.plot(x_list, y_list, color='#2FA4FF', marker=marker_style, picker=5, linewidth=1)

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
        global cycleH2O
        demo_mode = False
        if s_interface.meecoConnected == True and var2.get() != 'radO2':
            attempts = 0
            while attempts < 6:
                try:

                    h2o = raw_to_ppb(s_interface.get_h20())  #### comment out for random data###
                    # await asyncio.sleep(0.02)
                    # time.sleep(0.02)
                    h2o = round(float(h2o), 1)
                    # currentRaw.set(round(float(raw_to_ppb(read_serial_float(0))), 1)) #### comment out for random data###
                    s_interface.meecoConnected = True
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
                    s_interface.meecoConnected = True
                    if h2o < 0:
                        h2o = 0
                    currenth2o.set(h2o)
                    demo_mode = True
                    break
                    #####################
                    currenth2o.set("N/A")
                    h2o = -20
                    if recording == True and s_interface.meecoConnected == False and cycleH2O == 14:
                        print(
                            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nMEECO WAS DISCONNECTED DURING TESTING. PLEASE RESTART TGVIEW\n\n\n\n\n")
                        fuckitup('disconnect')
                        break
        elif s_interface.meecoConnected == False and var2.get() != 'radO2':
            attempts = 0
            while attempts < 6:
                try:

                    h2o = raw_to_ppb(s_interface.get_h20())  #### comment out for random data###
                    h2o = round(float(h2o), 1)
                    s_interface.meecoConnected = True
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
                    s_interface.meecoConnected = True
                    if h2o < 0:
                        h2o = 0
                    currenth2o.set(h2o)
                    demo_mode = True
                    break
                    #####################

                    s_interface.meecoConnected = False
                    currenth2o.set("N/A")
                    h2o = -20

                    if recording == True and s_interface.meecoConnected == False and cycleH2O == 14:
                        print(
                            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nMEECO WAS DISCONNECTED DURING TESTING. PLEASE RESTART TGVIEW\n\n\n\n\n")
                        fuckitup('disconnect')
                        break
        elif var2.get() == 'radO2':
            currenth2o.set('N/A')
            h2o = 9999

        if h2o < 0:
            h2o = 0
        if s_interface.meecoConnected == True:
            # print('h2o is working')
            if not demo_mode:
                testingStatusMessageMeeco.set("")
            else:
                testingStatusMessageMeeco.set("Demo Mode")
        if s_interface.meecoConnected == False:
            # print('h2o is fucked')
            testingStatusMessageMeeco.set("Check Tracer 2 Connection")

        if not manageGraphData.update_h2o_values(h2o):
            return

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
            if manageGraphData.h2odata_min < 0:
                a2.set_ylim(manageGraphData.h2odata_min - 10, manageGraphData.h2odata_max + 10)
            else:
                a2.set_ylim(0 - 1, manageGraphData.h2odata_max + 10)
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
        global cycleO2
        demo_mode = False
        o2 = 0
        if s_interface.deltafConnected == True and var2.get() != 'radH2O':
            attempts = 0
            while attempts < 15:

                try:
                    # await asyncio.sleep(0.02)
                    # time.sleep(0.02)
                    # print('..... attempting with ' + comPortOxygen + '.....')
                    o2 = s_interface.get_O2()  #### comment out for random data###

                    if 'e' in o2:
                        currento2.set('N/A')
                        o2 = round(float(o2), 1)
                        s_interface.deltafConnected = False
                    else:
                        o2 = round(float(o2), 1)
                        currento2.set(o2)
                        s_interface.deltafConnected = True

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
                        s_interface.deltafConnected = True
                        attempts = 15
                        print('attempt FAILED for O2')
                        demo_mode = True
                        break
                        ##############

                        o2 = 9999
                        s_interface.deltafConnected = False
                        print('attempt FAILED for O2')
                        currento2.set('N/A')
                        if recording == True and s_interface.deltafConnected == False and cycleO2 == 14:
                            print(
                                "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nDELTAF WAS DISCONNECTED DURING TESTING. PLEASE RESTART TGVIEW\n\n\n\n\n")
                            fuckitup('disconnect')
                            break

        elif not s_interface.deltafConnected and var2.get() != 'radH2O':
            attempts = 0
            while attempts < 3:
                try:
                    # await asyncio.sleep(0.02)
                    # time.sleep(0.02)
                    # print('..... attempting with ' + comPortOxygen + '.....')
                    o2 = s_interface.get_O2()  #### comment out for random data###

                    # print(o2)
                    if 'e' in o2:
                        currento2.set('N/A')
                        o2 = round(float(o2), 1)
                        s_interface.deltafConnected = False
                    else:
                        o2 = round(float(o2), 1)
                        currento2.set(o2)
                        s_interface.deltafConnected = True

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
                        s_interface.deltafConnected = True
                        attempts = 15
                        demo_mode = True
                        break
                        #########################

                        o2 = 9999
                        s_interface.deltafConnected = False
                        print('attempt FAILED for O2')
                        currento2.set('N/A')
                        if recording == True and s_interface.deltafConnected == False and cycleO2 == 14:
                            print(
                                "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nDELTAF WAS DISCONNECTED DURING TESTING. PLEASE RESTART TGVIEW\n\n\n\n\n")
                            fuckitup('disconnect')
                            break
        elif var2.get() == 'radH2O':
            currento2.set('N/A')
            o2 = 9999
        if s_interface.deltafConnected == True:
            if not demo_mode:
                # print('o2 is working')
                testingStatusMessageDeltaf.set("")
            else:
                testingStatusMessageDeltaf.set("Demo Mode")
        else:
            # print('o2 is fucked')
            testingStatusMessageDeltaf.set("Check DeltaF Connection")

        if not manageGraphData.update_o2_values(o2):
            return

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
                o2xMax = max(o2xList)
                if manageGraphData.o2data_min < 0:
                    a1.set_ylim(manageGraphData.o2data_min - 10, manageGraphData.o2data_max + 10)
                else:
                    a1.set_ylim(0 - 1, manageGraphData.o2data_max + 10)
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

    # global start_timea
    # start_timea = start_time.strftime("%H:%M  %m/%d/%y")
    stop_timee = stop_time.strftime("%H:%M  %m/%d/%y")

    confirm_fields(start_stop="stop")





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
