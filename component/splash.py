import tkinter as tk
from GlobalConst import root_path
from PIL import ImageTk
from PIL import Image


####First Toplevel frame to appear is Splash. RPiReader initializes after splash####
class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent, bg='grey25')
        # w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        # self.geometry("%dx%d%+d%+d" % (1920, 1080, 0, 0))
        self.attributes('-type', 'splash')
        self.geometry("%dx%d%+d%+d" % (1920, 1080, -2, 30))
        self.title("  Trace Gas View  ")

        self.myIcon = ImageTk.PhotoImage(file=f'{root_path}/TGViewClean.png')
        self.iconphoto(True, self.myIcon)

        ####### REPLACED the time, date, and logo image with a splash screen image #######
        splashXField = 550
        splashYField = 180
        splashXPadding = 25
        splashYPadding = 170

        ### Splash Logo
        self.gambar = Image.open(f'{root_path}/SplashScreen2021.png')
        self.imgSplash = ImageTk.PhotoImage(self.gambar)
        self.img = tk.Label(self, image=self.imgSplash, bg="grey25")
        self.img.image = self.imgSplash
        # self.img.place(x=splashXField+splashXPadding*4,y=splashYField+splashYPadding)
        self.img.place(x=0, y=0)

        self.update()
