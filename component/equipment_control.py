import tkinter as tk

###### meeco controls
# reads raw cell value, current upper/lower band limits, and current mode (service/inert)
# writes upper/lowerband limites and mode (service/inert)
from tkinter import ttk

from GlobalConst import QAM_GREEN, LARGEST_FONT, s_interface, LARGE_FONT, SMALL_FONT
from modules.Util import raw_to_ppb


def equipment_controls():
    paddx = 15
    paddy = 15
    top5 = tk.Toplevel()
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

    currentMode = tk.StringVar()
    meecoMode = int(s_interface.write_serial_int(False, 0))  #### comment out for random data###
    # meecoMode = 0
    if meecoMode == 1:
        currentMode.set('Inert')
    if meecoMode == 0:
        currentMode.set('Service')
    currentUpper = tk.StringVar()
    currentLower = tk.StringVar()
    currentUpper.set(round(float(raw_to_ppb(s_interface.read_serial_float(15))), 1))  #### comment out for random data###
    # time.sleep(0.02)
    currentLower.set(round(float(raw_to_ppb(s_interface.read_serial_float(16))), 1))  #### comment out for random data###
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
                        activeforeground="white", highlightbackground="#00cd66", highlightthickness=2, relief=tk.FLAT,
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
    upper_band = tk.DoubleVar(value=currentUpper.get())
    textbox = ttk.Entry(top5, width=10, textvariable=upper_band)
    textbox.place(x=bandXfield + bandXpad1, y=160 + paddy)

    lower_band = tk.DoubleVar(value=currentLower.get())
    textbox = ttk.Entry(top5, width=10, textvariable=lower_band)
    textbox.place(x=bandXfield + bandXpad1 + bandXpad2, y=160 + paddy)
    paddy += 60
    button1 = tk.Button(top5, text="Set New Bands", bg="grey35", activebackground="orange", fg="White",
                        activeforeground="white", highlightbackground="orange", highlightthickness=2, relief=tk.FLAT,
                        font=LARGE_FONT, borderwidth='1', width=12,
                        command=lambda: s_interface.write_upperandlower(upper_band.get(), lower_band.get()))
    button1.place(x=185, y=160 + paddy)
    button1 = tk.Button(top5, text="Save/Exit", bg="grey35", activebackground="firebrick1", fg="White",
                        activeforeground="white", highlightbackground="firebrick1", highlightthickness=2, relief=tk.FLAT,
                        font=LARGE_FONT, borderwidth='1', width=12, command=top5.destroy)
    button1.place(x=485, y=160 + paddy)
