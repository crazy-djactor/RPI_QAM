import tkinter as tk


class PopupWindow:
    def __init__(self, params):
        self.window = tk.Toplevel()
        self.params = params
        self.popup_window(self.window, params)

    def confirm_yes(self):
        self.params['command_yes']()
        self.window.destroy()

    def popup_window(self, window, params):
        confirm_font = "lato"
        window.title(params['title'])
        window.configure(background="grey25")

        w = 720
        h = 465

        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        # Calculate the x and y coordinates based on the current screen size
        sx = (ws / 2) - (w / 2)
        sy = (hs / 2) - (h / 2)
        # Open the root window in the middle of the screen
        # topA.overrideredirect(True)
        window.geometry('%dx%d+%d+%d' % (w, h, sx, sy))
        paddy = 5
        # Ask the question
        label4 = tk.Label(window, text=params['text_yes'], bg="grey25", fg='white',
                          font=(confirm_font, 20, 'bold'), wraplength=550)
        label4.place(relx=.5, rely=.29, anchor="center")

        # YES button
        button1 = tk.Button(window, text="Yes", compound="left", padx=30, activebackground="#678277", bg="grey35",
                            highlightbackground="#678277", highlightthickness=2, relief="flat",
                            activeforeground="white",
                            fg="White", font=(confirm_font, 37, 'bold'), borderwidth='1',
                            command=self.confirm_yes)
        button1.place(width=270, height=95, relx=.3, rely=.72, anchor="center")

        # NO button
        button2 = tk.Button(window, text="No", compound="left", padx=30, activebackground="IndianRed", bg="grey35",
                            highlightbackground="IndianRed", highlightthickness=2, relief="flat",
                            activeforeground="white",
                            fg="White", font=(confirm_font, 37, 'bold'), borderwidth='1', command=window.destroy)
        button2.place(width=270, height=95, relx=.7, rely=.72, anchor="center")
