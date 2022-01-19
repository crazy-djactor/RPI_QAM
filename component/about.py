import tkinter as tk
from PIL import ImageTk
from datetime import datetime, timedelta
from GlobalConst import root_path, QAM_GREEN


###### About TG View Window
# Displays relevant info such as the current version/build number

start_time = datetime.now()
start_timeez = start_time.strftime("%m/%d/%y @ %I:%M %p")

def about_window():
    # CURRENT VERSION/BUILD NUMBER
    # Adjust this when changes are made
    global version_num
    version_num = "v1.8.0"

    aboutFont = "lato"

    paddx = 15
    paddy = 15
    topA = tk.Toplevel()
    # topA.attributes('-type', 'Dock')
    topA.title("Program Infomation")
    topA.configure(background="grey25")
    # Width and height for the Tk root window
    w = 720
    h = 465
    # This gets the current screen width and height
    ws = topA.winfo_screenwidth()
    hs = topA.winfo_screenheight()
    # Calculate the x and y coordinates based on the current screen size
    sx = (ws / 2) - (w / 2)
    sy = (hs / 2) - (h / 2)
    # Open the root window in the middle of the screen
    # topA.overrideredirect(True)
    topA.geometry('%dx%d+%d+%d' % (w, h, sx, sy))
    paddy = 5

    ## Button image
    likeIcon = ImageTk.PhotoImage(file=f"{root_path}/like.png", master=topA)

    ### Dispaly the time that the program was opened to ensure testing validity
    label4 = tk.Label(topA, text="Application opened:", bg="grey25", fg='orange', font=(aboutFont, 40, 'bold'))
    label4.place(relx=.5, rely=.12, anchor="center")

    label4 = tk.Label(topA, text=start_timeez, bg="grey25", fg='white', font=(aboutFont, 40, 'bold'))
    label4.place(relx=.5, rely=.26, anchor="center")

    ##### equipment controls title
    label1 = tk.Label(topA, text="Build Number:", bg="grey25", fg=QAM_GREEN, font=(aboutFont, 40, 'bold'))
    label1.place(relx=.5, rely=.43, anchor="center")

    label2 = tk.Label(topA, text=version_num, bg="grey25", fg="white", font=(aboutFont, 40, 'bold'))
    label2.place(relx=.5, rely=.56, anchor="center")

    label3 = tk.Label(topA, text="Developed by Joel Taylor and Joshua Hoover", bg="grey25", fg="white",
                      font=(aboutFont, 14))
    label3.place(relx=.5, rely=.95, anchor="center")

    # QAM dark green: #678277
    button1 = tk.Button(topA, text="Got it!", image=likeIcon, compound="left", padx=40, activebackground="#678277",
                        bg="grey35", highlightbackground="#678277", highlightthickness=2, relief="flat",
                        activeforeground="white", fg="White", font=(aboutFont, 37, 'bold'), borderwidth='1',
                        command=topA.destroy)
    button1.place(width=305, height=95, relx=.5, rely=.8, anchor="center")
    button1.image = likeIcon