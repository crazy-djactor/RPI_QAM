##### Global Methods #####
import csv
import sys
import time
from datetime import datetime
from tkinter import Message, Button, FLAT
from tkinter import Toplevel

from GlobalConst import *
from modules.serial import SerialInterface


def exit_app():
    sys.exit()


def disconnect(how):
    error_time = datetime.now()
    error_file = "error entry " + str(error_time.strftime("%m_%d_%y_%I.%M.%S"))
    with open(os.path.join(err_log_path, error_file) + '.csv', 'w+', newline='') as o:
        writer1 = csv.writer(o, escapechar=' ', quoting=csv.QUOTE_NONE)

        writer1.writerow([str(error_file)])
        if how == "start":
            writer1.writerow(['DO NOT OPEN MULTIPLE INSTANCES OF TGVIEW'])
            writer1.writerow(['CHECK REMOTE DESKTOP FOR RUNNING TEST'])
        else:
            if SerialInterface.meecoConnected == True and SerialInterface.deltafConnected == False:
                writer1.writerow(['DELTAF WAS DISCONNECTED DURING TESTING'])
                writer1.writerow(['LIST DETAILS OF FAILURE BELOW FOR REVIEW'])
            elif SerialInterface.meecoConnected == False and SerialInterface.deltafConnected == True:
                writer1.writerow(['MEECO WAS DISCONNECTED DURING TESTING'])
                writer1.writerow(['LIST DETAILS OF FAILURE BELOW FOR REVIEW'])
            elif SerialInterface.meecoConnected == False and SerialInterface.deltafConnected == False:
                writer1.writerow(['BOTH ANALYZERS STOPPED COMMUNICATING DURING TESTING'])
                writer1.writerow(['LIST DETAILS OF FAILURE BELOW FOR REVIEW'])
        o.flush()

    os.popen("mousepad " + "'" + os.path.join(err_log_path, error_file) + ".csv'")
    time.sleep(0.5)

    ######### error message should show error and close out program #######
    err_widget = Toplevel()
    err_widget.title("Error")
    # Width and height for the Tk root window
    w = 500
    h = 180
    # This gets the current screen width and height
    ws = err_widget.winfo_screenwidth()
    hs = err_widget.winfo_screenheight()
    # Calculate the x and y coordinates based on the current screen size
    sx = (ws / 2) - (w / 2)
    sy = (hs / 2) - (h / 2)
    # Open the root window in the middle of the screen
    err_widget.geometry('%dx%d+%d+%d' % (w, h, sx, sy))
    err_widget.resizable(False, False)
    err_widget.config(bg="Grey25")
    msg = Message(err_widget, text="Error has been logged.\nPlease restart TGView.", width=500, bg="grey25", fg="grey85",
                  font=LARGE_FONT)
    msg.pack()
    button = Button(err_widget, text="EXIT", command=exit_app, width=20, height=2, bg="firebrick1", fg="white",
                    activebackground="firebrick2", activeforeground="white", highlightbackground="firebrick1",
                    relief=FLAT)
    button['font'] = LARGER_FONT
    button.pack()

