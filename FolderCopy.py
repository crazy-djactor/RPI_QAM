import os
import time
import shutil
import threading
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Progressbar
import datetime




os.getcwd()
print(os.getcwd())

os.chdir("/home/pi/TGView")
print(os.getcwd())

def CloseProgram():
    exit()


def SelectUSB():
    os.chdir("/media/pi")
    print(os.getcwd())
    global USB
    USB = filedialog.askdirectory()
    global destinations
    destinations = USB+"/TGView Backup (%s)"%datetime.datetime.now().strftime('%m-%d-%Y %H.%M.%S%p')
    print(USB)
    print(destinations)
    os.chdir(USB)
    print(os.getcwd())
    if os.getcwd() != "/media/pi":
        tk.Button(root, text="Create Backup", font=("century gothic",50,"bold"), fg="white", activeforeground="white", bg="#678277", activebackground="#678277", compound = "left", padx=30,command=CreateBackup).place(height=150,width=880,x=75,y=495)
    else:
        tk.Button(root, text="Create Backup", font=("century gothic",50,"bold"), fg="white", activeforeground="white", bg="grey35", activebackground="grey35", compound = "left", padx=30, state=tk.DISABLED).place(height=150,width=880,x=75,y=495)
    
def CreateBackup():
    
    tk.Button(root, text="Copying...", font=("century gothic",50,"bold"), fg="white", activeforeground="white", bg="#ff9500", activebackground="#ff9500", compound = "left", padx=30, command=None).place(height=150,width=630,x=75,y=255)
    tk.Label(root, text='This will automatically close once the copy is complete.', fg="White", bg="Grey25", font=("Century Gothic",40, "bold"), justify="center", wraplength=950).place(x=80,y=55)
    
    s1=ttk.Style()
    TROUGH_COLOR = 'grey35'
    BAR_COLOR = '#209736'
    s1.configure('red.Horizontal.TProgressbar', troughcolor=TROUGH_COLOR, bordercolor=TROUGH_COLOR,background=BAR_COLOR,lightcolor=BAR_COLOR,darkcolor=BAR_COLOR)
    global progress
    progress = Progressbar(root, style='red.Horizontal.TProgressbar', orient=tk.HORIZONTAL, length = 880, mode='determinate', maximum = 100, value=10)
    progress.place(x=75,y=495, height = 150)
    
            
    def bar():
        progress['value'] = 10
        root.update_idletasks()
        time.sleep(0.1)
        progress['value'] = 20
        root.update_idletasks()
        time.sleep(0.1)
        progress['value'] = 30
        root.update_idletasks()
        time.sleep(0.1)
        progress['value'] = 40
        root.update_idletasks()
        time.sleep(0.1)
        progress['value'] = 50
        root.update_idletasks()
        time.sleep(0.1)
        progress['value'] = 60
        root.update_idletasks()
        time.sleep(0.1)
        progress['value'] = 70
        root.update_idletasks()
        time.sleep(0.1)
        progress['value'] = 80
        root.update_idletasks()
        time.sleep(0.1)
        shutil.copytree("/home/pi/TGView", destinations)
        progress['value'] = 90
        root.update_idletasks()
        time.sleep(0.1)
        progress['value'] = 100
        root.update_idletasks()
        time.sleep(0.1)
    bar()
    
    
    tk.Label(root, text="Done!", fg="White", bg="#209736", font=("Century Gothic",50, "bold"), justify="center").place(x=395,y=530)
    print("DONE!!!")
    tk.Button(root, text="Closing...", font=("century gothic",50,"bold"), fg="white", activeforeground="white", bg="#ff9500", activebackground="#ff9500", compound = "left", padx=30, command=None).place(height=150,width=630,x=75,y=255)
    exit()


root = tk.Tk()
root.title('   Backup to USB   ')
p1=PhotoImage(file= '/home/pi/Pictures/USBcopy2.png')
root.iconphoto(False,p1)
root.resizable(False,False)
root.config(bg="Grey25")
# Width and height for the Tk root window
w=1030
h=720
# This gets the current screen width and height
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
# Calculate the x and y coordinates based on the current screen size
sx = (ws/2) - (w/2)
sy = (hs/2) - (h/2)
# Open the root window in the middle of the screen
root.geometry('%dx%d+%d+%d' % (w, h, sx, sy))

print (os.getcwd())


tk.Button(root, text="Create Backup", font=("century gothic",50,"bold"), fg="white", activeforeground="white", bg="grey35", activebackground="grey35", compound = "left", padx=30, state=tk.DISABLED).place(height=150,width=880,x=75,y=495)
tk.Button(root, text="Select Drive", font=("century gothic",50,"bold"), fg="white", activeforeground="white", bg="#ff9500", activebackground="#ff9500", compound = "left", padx=30, command=SelectUSB).place(height=150,width=630,x=75,y=255)
tk.Button(root, text="X", font=("century gothic",50,"bold"), fg="white", activeforeground="white", bg="indianred", activebackground="indianred", compound = "left", padx=30, command=CloseProgram).place(height=150,width=150,x=800,y=255)

#tk.Button(root, text="Select Folder", font=("Century Gothic",31, "bold"), fg="white", activeforeground="white", bg="#678176", activebackground="#81a6a3", image=dashIcon, compound = "left", padx=25, command=root.destroy).place(height=125, width=350,x=75,y=75)
tk.Label(root, text='Double-tap the USB Drive folder then tap "OK"', fg="White", bg="Grey25", font=("Century Gothic",40, "bold"), justify="center", wraplength=850).place(x=120,y=55)

root.mainloop()
