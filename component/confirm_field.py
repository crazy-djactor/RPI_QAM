import csv
import os
import shutil
import tkinter as tk
from statistics import mean

from PIL import ImageTk, Image
from matplotlib.widgets import SpanSelector

import GlobalConst
from GlobalConst import LARGEST_FONT, QAM_GREEN
from datetime import datetime
import csv
import os

import matplotlib
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from tkfilebrowser import askopendirname
import matplotlib.pyplot as plt


matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from GlobalConst import dir_TGView, LARGE_FONT, root_path

# see above
def retreive_input(inputs):
    inputValue = inputs.get("1.0", "end-1c")
    return inputValue


class ConfirmExport:
    confirm_method = ""
    newStartTime = ""
    oldStartTimeRH2O = ""
    newStopTime = ""
    oldStopTimeRH2O = ""
    newStartTimeO2 = ""
    oldStartTimeO2 = ""
    newStopTimeO2 = ""
    oldStopTimeO2 = ""
    o2bAvgEdit = ""
    o2bAvgUnedit = ""
    o2bMaxEdit = ""
    o2bMaxUnedit = ""
    o2bFinalEdit = ""
    o2bFinalUnedit = ""
    h2obAvgEdit = ""
    h2obAvgUnedit = ""
    h2obFinalEdit = ""
    h2obFinalUnedit = ""
    TestingIncValue = 0
    folder = ""

    def __init__(self):
        ConfirmExport.confirm_method = ""
        ConfirmExport.newStartTime = ""
        ConfirmExport.oldStartTimeRH2O = ""
        ConfirmExport.newStopTime = ""
        ConfirmExport.oldStopTimeRH2O = ""
        ConfirmExport.newStartTimeO2 = ""
        ConfirmExport.oldStartTimeO2 = ""
        ConfirmExport.newStopTimeO2 = ""
        ConfirmExport.oldStopTimeO2 = ""
        ConfirmExport.o2bAvgEdit = ""
        ConfirmExport.o2bAvgUnedit = ""
        ConfirmExport.o2bMaxEdit = ""
        ConfirmExport.o2bMaxUnedit = ""
        ConfirmExport.o2bFinalEdit = ""
        ConfirmExport.o2bFinalUnedit = ""
        ConfirmExport.h2obAvgEdit = ""
        ConfirmExport.h2obAvgUnedit = ""
        ConfirmExport.h2obFinalEdit = ""
        ConfirmExport.h2obFinalUnedit = ""

    @staticmethod
    def confirm_fields(start_stop):
        ConfirmExport.confirm_method = start_stop
        top4 = tk.Toplevel()
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

            start_time = datetime.now()
            GlobalConst.start_record_time = datetime.now().strftime("%m_%d_%y_%H.%M.%S")
            # global start_timea
            # start_timea = start_time.strftime("%H:%M  %m/%d/%y")

            global start_timet
            # start_timet.set(start_time.strftime("%I:%M %p  %-m/%-d/%y"))
            start_timet.set(datetime.now().strftime("%I:%M %p"))

            ##### global variable resets #######
            global o2_dataList
            global h2o_dataList
            global a1, a2
            global cycleO2, cycleH2O

            cycleH2O = 14
            cycleO2 = 14
            o2_dataList = ''
            h2o_dataList = ''
            a1.cla()
            a2.cla()

            headerFileTitle = "Header"
            path = GlobalConst.directory + '/' + str(building.get()) + "_" + str(tool_id.get()) + "_" + str(
                location.get()) + "_" + str(
                title.get()) + "_" + GlobalConst.start_record_time
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
            top4.textbox5.insert(tk.INSERT, header_list[9])
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

            with open(f'{GlobalConst.root_path}/Header_default.csv', 'w+', newline='') as d:
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

            GlobalConst.directory = GlobalConst.dir_TGView
            if start_stop == 'stop':
                path = GlobalConst.directory + '/' + str(header_list[3]) + "_" + str(header_list[4]) + "_" + str(
                    header_list[2]) + "_" + str(header_list[0]) + "_" + GlobalConst.start_record_time
                global pathF
                os.rename(pathF, path)
                pathF = path

            if start_stop == 'manage':
                pathF = folder

            ### adjust Header_default with new field names
            with open(f'{GlobalConst.root_path}/Header_default.csv', 'w+', newline='') as d:
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
                            ConfirmExport.o2bAvgEdit
                        except:
                            ConfirmExport.o2bAvgEdit = o2bAvgUnedit
                        writer3.writerow([ConfirmExport.o2bAvgEdit])
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
                            ConfirmExport.o2bAvgEdit
                        except:
                            ConfirmExport.o2bAvgEdit = o2bAvgUnedit
                        writer3.writerow([ConfirmExport.o2bAvgEdit])
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
                                activeforeground="white", highlightbackground="orange", highlightthickness=2,
                                relief=FLAT,
                                command=update_and_generatePDF)
            button2.place(width=515, height=105, x=205, y=870)
            button2.image = reportIcon

            # button4 = tk.Button(top4, text="Generate Failed Report",bg="grey15",fg="grey75",font=LARGE_FONT, command=update_and_generateFailedPDF)
            # button4.place(x=5,y=65)

            deleteIcon = ImageTk.PhotoImage(file=f"{root_path}/delete.png", master=top4)

            button3 = tk.Button(top4, text="Delete This Report", image=deleteIcon, compound="left", padx=50,
                                bg="grey35",
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
                    label14 = tk.Label(top4, textvariable=o2bAvgEditVar, width=17, bg="grey35", fg="white",
                                       font=SMALL_FONT)
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
                    label14 = tk.Label(top4, textvariable=o2bAvgEditVar, width=17, bg="grey35", fg="white",
                                       font=SMALL_FONT)
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
                label14 = tk.Label(top4, textvariable=time_elapsedvar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
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
                label14 = tk.Label(top4, textvariable=time_elapsedvar, width=17, bg="grey35", fg="white",
                                   font=SMALL_FONT)
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
                    label14 = tk.Label(top4, textvariable=o2bAvgEditVar, width=17, bg="grey35", fg="white",
                                       font=SMALL_FONT)
                    label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                    i = i + 1.05
                if o2bAvgEdit_exists == False and start_stop == 'stop':
                    label14 = tk.Label(top4, textvariable=o2MeanValueVar, width=17, bg="grey35", fg="white",
                                       font=SMALL_FONT)
                    label14.place(x=xfield + paddx, y=160 + paddy * i + yfield)
                    i = i + 1.05
                if o2bAvgEdit_exists == True:
                    o2bAvgEditVar = StringVar(value=o2bAvgEdit)
                    label14 = tk.Label(top4, textvariable=o2bAvgEditVar, width=17, bg="grey35", fg="white",
                                       font=SMALL_FONT)
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
                        time_elapsedO2 = str(int(time_elapseHourO2)) + " hours " + str(
                            int(time_elapseMinO2)) + " minutes"
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
                label14 = tk.Label(top4, textvariable=time_elapsedvar, bg="grey35", fg="white", font=SMALL_FONT,
                                   width=17)
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
                    time_elapsedH2O = str(int(time_elapseHourH2O)) + " hours " + str(
                        int(time_elapseMinH2O)) + " minutes"
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
                label14 = tk.Label(top4, textvariable=time_elapsedvar, bg="grey35", fg="white", font=SMALL_FONT,
                                   width=17)
                label14.place(x=xfield + paddx, y=175 + paddy * i + yfield)
                i = i + 1

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
        os.chdir(GlobalConst.dir_TGView)  # -------(CHANGE THIS TO WORK WITH THE CURRENT COMPUTER)

        ConfirmExport.TestingIncValue = 1  # -------(THIS CONTROLS HOW OFTEN DATA IS COLLECTED AND PLOTTED)

        def openCSV():
            global H2Ocsv
            global O2csv
            global headercsv
            H2Ocsv = None
            O2csv = None
            headercsv = None
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
            ConfirmExport.folder = askopendirname(title='Choose Test to Edit', initialdir='/home/pi/TGView',
                                              foldercreation=False)
            print(ConfirmExport.folder)
            os.chdir(ConfirmExport.folder)
            global O2csvFound, H2OcsvFound, BothcsvFound
            O2csvFound = False
            H2OcsvFound = False
            BothcsvFound = False
            try:
                for file in os.listdir(ConfirmExport.folder):
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
            top = tk.Toplevel()
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
                tk.Button(top, text="OK", fg="white", activeforeground="white", bg="#d73a3a",
                          activebackground="#d94d4d",
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
                    ConfirmExport.confirm_fields(start_stop='manage')

                tk.Button(top, text="Generate New PDF Report", font=LARGE_FONT, bg="grey35", activebackground="orange",
                          fg="White", activeforeground="white", highlightbackground="orange", highlightthickness=2,
                          relief=tk.FLAT, command=update_and_generatePDF).place(height=90, width=500, x=520, y=620)
                tk.Button(top, text="Return to Dashboard", font=LARGE_FONT, bg="grey35", activebackground="FireBrick1",
                          fg="White", activeforeground="white", highlightbackground="FireBrick1", highlightthickness=2,
                          relief=tk.FLAT, command=BackToSelect).place(height=90, width=500, x=10, y=620)

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
                    newStartTime = oldStartTimeRH2O + timedelta(minutes=int(addStartTimeMins),
                                                                seconds=int(addStartTimeSec))
                    print(newStartTime)

                    addStopTime = str(H2Oxb[-1])
                    addStopTimeMins, addStopTimeSec = addStopTime.split(".")
                    global newStopTime
                    newStopTime = oldStartTimeRH2O + timedelta(minutes=int(addStopTimeMins),
                                                               seconds=int(addStopTimeSec))
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
                          relief=FLAT, command=BackToSelect).place(height=100, width=895, x=buttonXfield,
                                                                   y=buttonYfield)

                lineWidthEdit = 2
                markerStyle = 'o'
                pointSize = 3
                # Setting up the top H2O graph
                aa1.plot(xx1, yy1, color='DodgerBlue', linewidth=lineWidthEdit, marker=markerStyle,
                         markersize=pointSize)
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
                oldStopTimeRH2O = oldStartTimeRH2O + timedelta(hours=int(oldStopTimeHours),
                                                               minutes=int(oldStopTimeMins),
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
                    oldStopTimeRO2 = oldStartTimeRH2O + timedelta(hours=int(oldStopTimeHours),
                                                                  minutes=int(oldStopTimeMins),
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
                    newStartTime = oldStartTimeRH2O + timedelta(minutes=int(addStartTimeMins),
                                                                seconds=int(addStartTimeSec))

                    addStopTime = str(H2Oxb[-1])
                    addStopTimeMins, addStopTimeSec = addStopTime.split(".")
                    global newStopTime
                    newStopTime = oldStartTimeRH2O + timedelta(minutes=int(addStopTimeMins),
                                                               seconds=int(addStopTimeSec))

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
        QAMmd = Image.open(f'{GlobalConst.root_path}/QAM.gif')
        imgSplash = ImageTk.PhotoImage(QAMmd, master=root)
        imgg = tk.Label(root, image=imgSplash, borderwidth=0, highlightthickness=0)
        imgg.image = imgSplash
        imgg.place(x=625, y=75)

        # --------------------------------------------
        # BUTTON IMAGES
        # --------------------------------------------
        dashIcon = ImageTk.PhotoImage(file=f"{GlobalConst.root_path}/dashboard.png", master=root)
        folderIcon = ImageTk.PhotoImage(file=f"{GlobalConst.root_path}/foldersolid.png", master=root)

        tk.Button(root, text="Select Folder", font=("century gothic", 50, "bold"), fg="white", activeforeground="white",
                  bg="#ff9500", activebackground="#ffab34", image=folderIcon, compound="left", padx=30,
                  command=openCSV).place(height=150, width=880, x=75, y=495)
        tk.Button(root, text="Dashboard", font=("Century Gothic", 31, "bold"), fg="white", activeforeground="white",
                  bg="#678176", activebackground="#81a6a3", image=dashIcon, compound="left", padx=25,
                  command=root.destroy).place(height=125, width=350, x=75, y=75)
        tk.Label(root, text="Select the folder with the correct Name, ID, Test Type, and Date", fg="White", bg="Grey25",
                 font=("Century Gothic", 40, "bold"), justify="center", wraplength=850).place(x=100, y=280)

        root.mainloop()