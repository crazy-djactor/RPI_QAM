import os
import csv
import PIL
import matplotlib
import numpy as np
import tkinter as tk
matplotlib.use("TkAgg")
from tkinter import ttk
from tkinter import Toplevel
from matplotlib import style
from PIL import ImageTk, Image
from tkinter import filedialog
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

os.getcwd()
print(os.getcwd())

os.chdir("/home/pi/Desktop/JoelPi")
print(os.getcwd())

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
    print(os.getcwd())
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
    top.geometry("1030x720")
    top.resizable(False,False)
    top.config(bg="Grey25")
    global f1
    global f2
    f1 = Figure(figsize=(5,6), dpi=100, facecolor=(0.40,0.51,0.46))
    f2 = Figure(figsize=(5,6), dpi=100, facecolor=(0.40,0.51,0.46))
    a1 = f1.add_subplot(211,facecolor=(0.25,0.25,0.25))
    a2 = f2.add_subplot(211,facecolor=(0.25,0.25,0.25))
    a1new = f1.add_subplot(212,facecolor=(0.25,0.25,0.25))
    a2new = f2.add_subplot(212,facecolor=(0.25,0.25,0.25))

    x1 = []
    x2 = []    
    y1 = []
    y2 = []

    if H2Ocsv is None:
        print("H2O file NOT found")
        global h2oPath
        o2Path = os.path.join(folder,O2csv)
        with open(o2Path) as csvO2:
            plots = csv.reader(csvO2, delimiter=',')
            for row in plots:
                x2.append(float(row[0]))
                y2.append(float(row[1]))

        #Creates the figure, canvas, and button
        f2 = plt.figure(figsize=(10.1,6), dpi=100, facecolor=(0.40,0.51,0.46))
        a2 = f2.add_subplot(211,facecolor=(0.25,0.25,0.25))
        canvas1 = FigureCanvasTkAgg(f2, master=top)
        canvas1.get_tk_widget().place(x=10,y=10)
        tk.Button(top, text="Save as PDF", fg="white", bg="#d73a3a", font=("century gothic",30,"bold"), command=exportO2).place(height=90,width=500,x=520,y=620)
        tk.Button(top, text="Back to Select", fg="white", bg="#ff9500", font=("century gothic",30,"bold"), command=exportO2).place(height=90,width=500,x=10,y=620)
        
        #setting the top (original) graph
        a2.plot(x2, y2, color='#60d500', marker='o')
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
        line2, = ax2.plot(x2, y2, color='#60d500', marker='o')
        ax2.grid(True)
        ax2.set_xlabel('Time in minutes')
        ax2.set_ylabel('PPB')

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
            # save
            np.savetxt("O2.out", np.c_[O2x, O2y])
        # set useblit True on gtkagg for enhanced performance
        span = SpanSelector(a2, onselect, 'horizontal', useblit=True,
                            rectprops=dict(alpha=0.5, facecolor='#678176'))
        plt.show() 

    elif O2csv is None:
        print("O2 file NOT found")
        global h2oPath
        h2oPath = os.path.join(folder,H2Ocsv)
        with open(h2oPath) as csvH2O:
            plots = csv.reader(csvH2O, delimiter=',')
            for row in plots:
                x1.append(float(row[0]))
                y1.append(float(row[1]))

        #Creates the figure, canvas, and button
        f1 = plt.figure(figsize=(10.1,6), dpi=100, facecolor=(0.40,0.51,0.46))
        a1 = f1.add_subplot(211,facecolor=(0.25,0.25,0.25))
        canvas2 = FigureCanvasTkAgg(f1, master=top)
        canvas2.get_tk_widget().place(x=10,y=10)
        tk.Button(top, text="Save as PDF", fg="white", bg="#d73a3a", font=("century gothic",30,"bold"), command=exportH2O).place(height=90,width=500,x=520,y=620)
        tk.Button(top, text="Back to Select", fg="white", bg="#ff9500", font=("century gothic",30,"bold"), command=exportH2O).place(height=90,width=500,x=10,y=620)
        
        #setting the top (original) graph
        a1.plot(x1, y1, color='DodgerBlue', marker='o')
        a1.grid(True)
        a1.set_title('Click and drag to select new H2O', fontsize=25, pad=12)
        a1.set_xlabel('Time in minutes', color="white")
        a1.set_ylabel('PPB', color="white")
        a1.tick_params(colors='w')
        f1.subplots_adjust(top=.90, hspace=0.3)
        a1.title.set_color('w')

        #setting up bottom (edited) graph
        ax1 = f1.add_subplot(212,facecolor=(0.25,0.25,0.25))
        line1, = ax1.plot(x1, y1, color='DodgerBlue', marker='o')
        ax1.grid(True)
        ax1.set_xlabel('Time in minutes')
        ax1.set_ylabel('PPB')

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
            f1.canvas.draw_idle()
            # save
            np.savetxt("H2O.out", np.c_[H2Ox, H2Oy])
        # set useblit True on gtkagg for enhanced performance
        span = SpanSelector(a1, onselect, 'horizontal', useblit=True,
                            rectprops=dict(alpha=0.5, facecolor='#678176'))
        plt.show()
        
    else:
        #This handles the H2O file and graph
        h2oPath = os.path.join(folder,H2Ocsv)
        with open(h2oPath) as csvH2O:
            plots = csv.reader(csvH2O, delimiter=',')
            for row in plots:
                x1.append(float(row[0]))
                y1.append(float(row[1]))

        #This handles the O2 file and graph
        o2Path = os.path.join(folder,O2csv)
        with open(o2Path) as csvO2:
            plots = csv.reader(csvO2, delimiter=',')
            for row in plots:
                x2.append(float(row[0]))
                y2.append(float(row[1]))
        #Setting up the main figure and canvas for both graphs
        f1 = plt.figure(figsize=(10.1,6), dpi=100, facecolor=(0.40,0.51,0.46))
        a1 = f1.add_subplot(221,facecolor=(0.25,0.25,0.25))
        a2 = f1.add_subplot(222,facecolor=(0.25,0.25,0.25))
        canvas3 = FigureCanvasTkAgg(f1, master=top)
        canvas3.get_tk_widget().place(x=10,y=10)
        tk.Button(top, text="Save as PDF", fg="white", bg="#d73a3a", font=("century gothic",30,"bold"), command=exportBoth).place(height=90,width=500,x=520,y=620)
        tk.Button(top, text="Back to Select", fg="white", bg="#ff9500", font=("century gothic",30,"bold"), command=exportBoth).place(height=90,width=500,x=10,y=620)
        
        #Setting up the top H2O graph
        a1.plot(x1, y1, color='DodgerBlue', marker='.')
        a1.grid(True)
        a1.set_title('Click and drag to select new H2O',fontsize=15, color="white", pad=15)
        a1.set_xlabel('Time in minutes', color="white")
        a1.set_ylabel('PPB', color="white")
        a1.tick_params(colors='w')
        f1.subplots_adjust(top=.90, hspace=0.3)

        #Setting up the top O2 graph
        a2.plot(x2, y2, color='#60d500', marker='.')
        a2.grid(True)
        a2.set_title('Click and drag to select new O2',fontsize=15, color="white", pad=15)
        a2.set_xlabel('Time in minutes', color="white")
        a2.set_ylabel('PPB', color="white")
        a2.tick_params(colors='w')
        f1.subplots_adjust(top=.90, hspace=0.3, wspace=0.3)

        #Setting up bottom (edited) H2O graph
        ax1 = f1.add_subplot(223,facecolor=(0.25,0.25,0.25))
        line1, = ax1.plot(x1, y1, color='DodgerBlue', marker='.')
        ax1.grid(True)
        ax1.set_xlabel('Time in minutes', color="white")
        ax1.set_ylabel('PPB', color="white")
        ax1.tick_params(colors='w')

        #setting up bottom (edited) graph
        ax2 = f1.add_subplot(224,facecolor=(0.25,0.25,0.25))
        line2, = ax2.plot(x2, y2, color='#60d500', marker='.')
        ax2.grid(True)
        ax2.set_xlabel('Time in minutes', color="white")
        ax2.set_ylabel('PPB', color="white")
        ax2.tick_params(colors='w')

        #This handles the selection of the H2O graph
        def onselectH2O(xmin, xmax):
            H2Omin, H2Omax = np.searchsorted(x1, (xmin, xmax))
            H2Omax = min(len(x1) - 1, H2Omax)
            H2Ox = x1[H2Omin:H2Omax]
            H2Oy = y1[H2Omin:H2Omax]
            line1.set_data(H2Ox, H2Oy)
            ax1.set_xlim(H2Ox[0]-1, H2Ox[-1]+1)
            ax1.set_ylim(min(H2Oy)-1, max(H2Oy)+1)
            f1.canvas.draw_idle()
            #Save the selection into a separate .out file
            np.savetxt("H2O.out", np.c_[H2Ox, H2Oy])

        #This handles the selected portion of the O2 graph
        def onselectO2(xmin, xmax):
            O2min, O2max = np.searchsorted(x2, (xmin, xmax))
            O2max = min(len(x2) - 1, O2max)
            O2x = x2[O2min:O2max]
            O2y = y2[O2min:O2max]
            line2.set_data(O2x, O2y)
            ax2.set_xlim(O2x[0]-1, O2x[-1]+1)
            ax2.set_ylim(min(O2y)-1, max(O2y)+1)
            f1.canvas.draw_idle()
            #Save the selection into a separate .out file
            np.savetxt("O2.out", np.c_[O2x, O2y])
        # set useblit True on gtkagg for enhanced performance
        spanH2O = SpanSelector(a1, onselectH2O, 'horizontal', useblit=True,
                            rectprops=dict(alpha=0.5, facecolor='#678176'))
        spanO2 = SpanSelector(a2, onselectO2, 'horizontal', useblit=True,
                            rectprops=dict(alpha=0.5, facecolor='#678176'))
        plt.show()

def exportH2O():
    print('H2O')
    top.destroy()

def exportO2():
    print('O2')
    top.destroy()

def exportBoth():
    print('Both')
    top.destroy()

root = tk.Tk()
root.title('Pi View')
root.resizable(False, False)
root.config(bg="Grey25")
root.geometry("600x425")

QAMmd = Image.open('QAMmd.gif')
imgSplash = ImageTk.PhotoImage(QAMmd)
img_o2 = tk.Label(root, image=imgSplash, borderwidth=0, highlightthickness=0)
img_o2.image = imgSplash
img_o2.place(x=350, y=50)

tk.Button(root, text="Select Folder", font=("century gothic",30,"bold"), fg="white", bg="#ff9500", command=openCSV).place(height=100,width=500,x=50,y=275)
tk.Button(root, text="Dashboard", font=("Century Gothic",17, "bold"), fg="white", bg="#678176", command=root.destroy).place(height=75, width=175,x=50,y=50)
tk.Label(root, text="Select the folder with the correct Name, ID, Test Type, and Date", fg="White", bg="Grey25", font=("Century Gothic",22, "bold"), justify="center", wraplength=490).place(x=60,y=165)

root.mainloop()
