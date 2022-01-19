import sys
import tkinter as tk
from PIL import ImageTk
from PIL import Image
import csv
from tkinter import ttk

from GlobalConst import root_path, LARGEST_FONT, SMALL_FONT, QAM_GREEN
from TGView import PageOne
from component.about import about_window
from component.equipment_control import equipment_controls
from modules.AdjustFigure import AdjustFigure
from datetime import datetime

###### Close TG View
def close_program():
    sys.exit()


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
        testingStatusMessageMeeco = tk.StringVar(value="")
        global testingStatusMessageDeltaf
        testingStatusMessageDeltaf = tk.StringVar(value="")

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

        # start_time = datetime.now()
        # start_timee = start_time.strftime("%m_%d_%y_%I.%M.%S")
        # pathstart = f'{root_path}/TGView/' + str(client) + "_" + str(location) + "_" + str(title) + "_" + start_timee

        ### var2 determines which analyzer is talking
        global var2
        var2 = tk.StringVar()
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
                     foreground=QAM_GREEN, indicatoron=0, relief=tk.FLAT)
        s1.configure("h2o.TRadiobutton", font=('Century Gothic', 21, 'bold'), background="#404040",
                     foreground="#00BFFF", indicatoron=0, relief=tk.FLAT)
        s1.configure("o2.TRadiobutton", font=('Century Gothic', 21, 'bold'), background="#404040", foreground="#00CD66",
                     indicatoron=0, relief=tk.FLAT)
        radioFont = ('Century Gothic', 21, 'bold')
        pax = 620
        pay = 460
        padx = 220
        rad_both = tk.Radiobutton(self, text="O2 & H2O", width=11, font=radioFont, variable=var2, selectcolor=QAM_GREEN,
                                  activebackground=QAM_GREEN, background="grey35", \
                                  highlightbackground=QAM_GREEN, activeforeground="white", foreground="white",
                                  indicatoron=0, value="radBoth", relief=tk.FLAT, command=both_selected).place(
            x=padx + pax, y=130)  # (x=padx*2+pax,y=200+pay)
        rad_o2 = tk.Radiobutton(self, text="O2", width=11, font=radioFont, variable=var2, selectcolor="#00CD66",
                                activebackground="#00CD66", background="grey35", \
                                highlightbackground="#00CD66", activeforeground="white", foreground="white",
                                indicatoron=0, value="radO2", relief=tk.FLAT, command=o2_selected).place(x=pax,
                                                                                                         y=130)  # (x=pax,y=200+pay)
        rad_h2o = tk.Radiobutton(self, text="H2O", width=11, font=radioFont, variable=var2, selectcolor="#00BFFF",
                                 activebackground="#00BFFF", background="grey35", \
                                 highlightbackground="#00BFFF", activeforeground="white", foreground="white",
                                 indicatoron=0, value="radH2O", relief=tk.FLAT, command=h2o_selected).place(
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
        img_o2 = tk.Label(self, image=imgSplash, bg="grey25")
        img_o2.image = imgSplash
        img_o2.place(x=20, y=200)
        #
        global img_h2o
        try:
            gambar2 = Image.open(f'{root_path}/TGView/graphH2O.png')
        except:
            gambar2 = Image.open(f'{root_path}/graph1.png')
        imgSplash2 = ImageTk.PhotoImage(gambar2)
        img_h2o = tk.Label(self, image=imgSplash2, bg="grey25")
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
                            relief=tk.FLAT, activeforeground="white", fg="White", font=('calibri', 32, 'bold'),
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
        currento2 = tk.StringVar(value=0)
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
        currenth2o = tk.StringVar(value=0)
        if int(currenth2o.get()) < 0:
            currenth2o = 0
        labelH2O_value = tk.Label(self, textvariable=currenth2o, width=6, bg="grey35", fg="#00BFFF",
                                  font=('calibri', 20, 'bold'))
        labelH2O_value.place(x=h2o_position['value_x'], y=h2o_position['value_y'])
