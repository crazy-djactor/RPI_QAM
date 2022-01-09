import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.figure import Figure
import csv
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
root.title('PDF Report Generator')
root.resizable(False, False)
root.config(bg="Grey25")
root.geometry("600x425")

global var
var = tkinter.StringVar()

global img
img = PhotoImage(file="QAM.png")

def buttonClick():
    print("Success!!")

def h2oinfo():
    print("H2O info selected")
    Label(top1, text="The information file has been attached!", font=('Century Gothic',17), fg="green2", bg="grey25").place(x=575,y=310)

def o2info():
    print("O2 info selected")
    Label(top2, text="The information file has been attached!", font=('Century Gothic',17), fg="green2", bg="grey25").place(x=575,y=310)

def h2o_selected():
    print(var.get())
    Label(root, text="Select the H2O CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="DeepSkyBlue", justify="right").place(x=69,y=108)
    Button(root, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="white", command=open1).place(height=50, width=125, x=400, y=102)
    Label(root, text="Select the O2 CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="Grey50", justify="right").place(x=75,y=188)
    Button(root, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="Grey25", state="disabled").place(height=50, width=125, x=400, y=185)

def o2_selected():
    print(var.get())
    Label(root, text="Select the O2 CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="SpringGreen3", justify="right").place(x=75,y=188)
    Button(root, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="white", command=open2).place(height=50, width=125, x=400, y=185)
    Label(root, text="Select the H2O CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="Grey50", justify="right").place(x=69,y=108)
    Button(root, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="Grey25", state="disabled").place(height=50, width=125, x=400, y=102)

def both_selected():
    print(var.get())
    Label(root, text="Select the H2O CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="DeepSkyBlue", justify="right").place(x=69,y=108)
    Button(root, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="white", command=open1).place(height=50, width=125, x=400, y=102)
    Label(root, text="Select the O2 CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="SpringGreen3", justify="right").place(x=75,y=188)
    Button(root, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="white", command=open2).place(height=50, width=125, x=400, y=185)

s1 = ttk.Style()
s1.configure("h2o.TRadiobutton", font=('Century Gothic',17,'bold'), background="#404040", foreground="#00BFFF")
s1.configure("o2.TRadiobutton", font=('Century Gothic',17,'bold'), background="#404040", foreground="#00CD66")
s1.configure("both.TRadiobutton", font=('Century Gothic',17,'bold'), background="#404040", foreground="Orange")

# Radiobuttons
rad_h2o = ttk.Radiobutton(root, text="H2O", style="h2o.TRadiobutton", variable=var, value="radH2O", command=h2o_selected).place(x=105, y=35)
rad_o2 = ttk.Radiobutton(root, text="O2", style="o2.TRadiobutton", variable=var, value="radO2", command=o2_selected).place(x=270, y=35)
rad_both = ttk.Radiobutton(root, text="Both", style="both.TRadiobutton", variable=var, value="radBoth", command=both_selected).place(x=420, y=35)

####### FILEPATH FUNCTIONS #######
# This prompts the user to open the first CSV or TXT file
def open1():
    global filepath1
    filepath1 = filedialog.askopenfilename(initialdir="/Desktop", title="Select a file", filetypes=(("csv files","*.csv"),("txt files","*.txt")))
    if filepath1:
        global top1
        top1=Toplevel()
        top1.geometry("1040x520")
        top1.resizable(False,False)
        top1.config(bg="Grey25")

        global f1
        global a1
        global x1
        global y1
        f1 = Figure(figsize=(5,5), dpi=100)
        a1 = f1.add_subplot(111)
        x1 = []
        y1 = []

        with open(filepath1) as csvfile:
            plots= csv.reader(csvfile, delimiter=',')
            for row in plots:
                x1.append(float(row[0]))
                y1.append(float(row[1]))
                
        a1.plot(x1, y1, color='blue', marker='o')
        a1.grid(True)

        canvas = FigureCanvasTkAgg(f1, master=top1)
        canvas.get_tk_widget().place(x=10,y=10)

        def confirmH2O():
            print("H2O Comfirmed!")
            if var.get() == "radH2O":
                print("Export H2O only")
                Label(root, text="Done!", font=('Century Gothic',10,'bold'), fg="green2", bg="Grey25").place(x=540, y=114)
                Button(root, text="Generate PDF", bg="IndianRed", fg="White", font=("Century Gothic", 17, "bold"), command=exportH2O).place(height=75, width=450, x=75, y=277)
            else:
                print("Export Both")
                Label(root, text="Done!", font=('Century Gothic',10,'bold'), fg="green2", bg="Grey25").place(x=540, y=114)
                Button(root, text="Generate PDF", bg="IndianRed", fg="White", font=("Century Gothic", 17, "bold"), command=exportBoth).place(height=75, width=450, x=75, y=277)
            top1.destroy()

        def cancelH2O():
            print("H2O Cancelled.")
            Label(root, text="Done!", font=('Century Gothic',10,'bold'), fg="Grey25", bg="Grey25").place(x=540, y=114)
            Button(root, text="Generate PDF", bg="Grey50", fg="White", font=("Century Gothic", 17, "bold"), state="disabled").place(height=75, width=450, x=75, y=277)
            top1.destroy()

        Button(top1, text="Cancel", fg="white", bg="IndianRed", font=('Century Gothic',17,'bold'), command=cancelH2O).place(height=100, width=250, x=520, y=410)
        Button(top1, text="Confirm", fg="white", bg="SpringGreen3", font=('Century Gothic',17,'bold'), command=confirmH2O).place(height=100, width=250, x=780, y=410)
        Label(top1, text="Ensure that you selected the correct file by checking the file path, below:", fg="Orange", bg="Grey25", font=("Century Gothic",10, "bold"), justify="center").place(x=540, y=10)
        Label(top1, text=filepath1, fg="Grey85", bg="Grey25", width=66, justify="center", wraplength=500).place(x=540, y=30)
        Label(top1, text="Attach the H2O information file:", fg="White", bg="Grey25", font=("Century Gothic",20,"bold"), wraplength="300").place(x=555, y=180)
        Button(top1, text="Open", fg="white", bg="Grey50", font=('Century Gothic',17,'bold'), command=h2oinfo).place(width=170, height=75, x=820, y=175)

    # This clears the error that would orccur if the user clicked cancel
    else:
        print("Nothing Selected.")

# This prompts the user to open the second CSV or TXT file
def open2():
    global filepath2
    filepath2 = filedialog.askopenfilename(initialdir="/Desktop", title="Select a file", filetypes=(("csv files","*.csv"),("txt files","*.txt")))
    if filepath2:
        global top2
        top2=Toplevel()
        top2.geometry("1040x520")
        top2.resizable(False,False)
        top2.config(bg="Grey25")
        
        global f2
        global a2
        global x2
        global y2
        f2 = Figure(figsize=(5,5), dpi=100)
        a2 = f2.add_subplot(111)
        x2 = []
        y2 = []

        with open(filepath2) as csvfile:
            plots= csv.reader(csvfile, delimiter=',')
            for row in plots:
                x2.append(int(row[0]))
                y2.append(int(row[1]))
        
        a2.plot(x2, y2, color='green', marker='o')
        a2.grid(True)

        canvas = FigureCanvasTkAgg(f2, master=top2)
        canvas.get_tk_widget().place(x=10,y=10)

        def confirmO2():
            print("O2 Confirmed!")
            if var.get() == "radO2":
                # This redirects to the exportO2 function so only the O2 file is used
                Label(root, text="Done!", font=('Century Gothic',10,'bold'), fg="green2", bg="Grey25").place(x=540, y=197)
                Button(root, text="Generate PDF", bg="IndianRed", fg="White", font=("Century Gothic", 17, "bold"), command=exportO2).place(height=75, width=450, x=75, y=277)
            else:
                # This redirects to the exportBoth function so both can be used
                Label(root, text="Done!", font=('Century Gothic',10,'bold'), fg="green2", bg="Grey25").place(x=540, y=197)
                Button(root, text="Generate PDF", bg="IndianRed", fg="White", font=("Century Gothic", 17, "bold"), command=exportBoth).place(height=75, width=450, x=75, y=277)
            top2.destroy()

        def cancelO2():
            print("Cancelled.")
            Button(root, text="Generate PDF", bg="Grey50", fg="White", font=("Century Gothic", 17, "bold"), state="disabled").place(height=75, width=450, x=75, y=277)
            Label(root, text="Done!", font=('Century Gothic',10,'bold'), fg="Grey25", bg="Grey25").place(x=540, y=197)
            top2.destroy()

        Button(top2, text="Cancel", fg="white", bg="IndianRed", font=('Century Gothic',17,'bold'), command=cancelO2).place(height=100, width=250, x=520, y=410)
        Button(top2, text="Confirm", fg= "white", bg="SpringGreen3", font=('Century Gothic',17,'bold'), command=confirmO2).place(height=100, width=250, x=780, y=410)
        Label(top2, text="Ensure that you selected the correct file by checking the file path, below:", fg="Orange", bg="Grey25", font=("Century Gothic",10, "bold"), justify="center").place(x=540, y=10)
        Label(top2, text=filepath2, fg="Grey85", bg="Grey25", width=66, justify="center", wraplength=500).place(x=540, y=30)
        Label(top2, text="Attach the O2 information file:", fg="White", bg="Grey25", font=("Century Gothic",20,"bold"), wraplength="300").place(x=555, y=180)
        Button(top2, text="Open", fg="white", bg="Grey50", font=('Century Gothic',17,'bold'), command=o2info).place(width=170, height=75, x=820, y=175)

    else:
        print("Nothing Selected.")

# This prompts the user to select where the PDF is to be saved.
def exportH2O():
        savepath = filedialog.asksaveasfilename(initialdir="/Desktop", title="Save the file", filetypes=(("PDF files","*.pdf"),("all files","*.*")))
        if savepath:
            # This populates the data from the CSV file into the x1 and y1 variables
            with open(filepath1) as csvfile:
                csv.reader(csvfile, delimiter=',')
            
            # This plots the data on a graph, using the matplotlib plt function
            with PdfPages(savepath) as export_pdf:
                
                # This plots the data from the H2O file
                plt.plot(x1, y1, color='blue', marker='o')
                plt.title('PPB Over Time (H2O)', fontsize=10)
                plt.xlabel('Time in minutes', fontsize=8)
                plt.ylabel('PPB', fontsize=8)
                plt.grid(True)
                export_pdf.savefig()
                plt.close()

        else:
            print("Cancelled")

def exportO2():
        savepath = filedialog.asksaveasfilename(initialdir="/Desktop", title="Save the file", filetypes=(("PDF files","*.pdf"),("all files","*.*")))
        if savepath:
            # This populates the data from the CSV file into the x2 and y2 variables
            with open(filepath2) as csvfile:
                csv.reader(csvfile, delimiter=',')
            
            # This plots the data on a graph, using the matplotlib plt function
            with PdfPages(savepath) as export_pdf:
                
                # This plots the data from the O2 file
                plt.plot(x2, y2, color='green', marker='o')
                plt.title('PPB Over Time (O2)', fontsize=10)
                plt.xlabel('Time in minutes', fontsize=8)
                plt.ylabel('PPB', fontsize=8)
                plt.grid(True)
                export_pdf.savefig()
                plt.close()
        else:
            print("Cancelled")

def exportBoth():
        savepath = filedialog.asksaveasfilename(initialdir="/Desktop", title="Save the file", filetypes=(("PDF files","*.pdf"),("all files","*.*")))
        if savepath:
            # This populates the data from the CSV file into the x1 and y1 variables
            with open(filepath1) as csvfile:
                csv.reader(csvfile, delimiter=',')

            # This populates the data from the CSV file into the x2 and y2 variables
            with open(filepath2) as csvfile:
                csv.reader(csvfile, delimiter=',')
            
            # This plots the data on a graph, using the matplotlib plt function
            with PdfPages(savepath) as export_pdf:
                
                # This plots the data from the first file
                plt.plot(x1, y1, color='blue', marker='o')
                plt.title('PPB Over Time (H2O)', fontsize=10)
                plt.xlabel('Time in minutes', fontsize=8)
                plt.ylabel('PPB', fontsize=8)
                plt.grid(True)
                export_pdf.savefig()
                plt.close()
                
                # This plots the data from the second file
                plt.plot(x2, y2, color='green', marker='o')
                plt.title('PPB Over Time (O2)', fontsize=10)
                plt.xlabel('Time in minutes', fontsize=8)
                plt.ylabel('PPB', fontsize=8)
                plt.grid(True)
                export_pdf.savefig()
                plt.close()
        else:
            print("Cancelled")

####### GUI #######
# Default, greyed out and disabled, UI
Label(root, text="Select the H2O CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="Grey50", justify="right").place(x=69,y=108)
Button(root, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="Grey25", state="disabled").place(height=50, width=125, x=400, y=102)
Label(root, text="Select the O2 CSV file:", font=("Century Gothic",20,"bold"), bg="Grey25", fg="Grey50", justify="right").place(x=75,y=188)
Button(root, text="Open", font=("Century Gothic",17,"bold"), bg="Grey50", fg="Grey25", state="disabled").place(height=50, width=125, x=400, y=185)

# Note for the user to ensure proper input
Label(root, text='NOTE: You must add ".pdf" to the end of your saved filename.', font=("Century Gothic",10, "italic"), bg="Grey25", fg="Orange", width=75, justify="center").place(x=0,y=375)

# Generate PDF default/greyed out
Button(root, text="Generate PDF", bg="Grey50", fg="White", font=("Century Gothic", 17, "bold"), state="disabled").place(height=75, width=450, x=75, y=277)

root.mainloop()