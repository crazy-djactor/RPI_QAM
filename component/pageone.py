import tkinter as tk
from datetime import datetime

from GlobalConst import s_interface


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.start_time = datetime.now()

        global currentRaw
        currentRaw = tk.StringVar()
        if s_interface.deltafConnected == True and s_interface.meecoConnected == True:
            testingStatusMessageMeeco.set('')
            testingStatusMessageDeltaf.set('')
        elif s_interface.deltafConnected == True and s_interface.meecoConnected == False:
            testingStatusMessageMeeco.set("Check Tracer 2 Connection")
            testingStatusMessageDeltaf.set('')
        elif s_interface.deltafConnected == False and s_interface.meecoConnected == True:
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
        start_timet = tk.StringVar(value='0')
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