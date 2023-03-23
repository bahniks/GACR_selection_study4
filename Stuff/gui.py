from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import localtime, strftime, time
from collections import defaultdict
from uuid import uuid4

from constants import TESTING

import os


class GUI(Tk):
    def __init__(self, frames):
        super().__init__()
        
        self.title("Experiment")
        self.config(bg = "white")
        if TESTING:
            self.geometry("1680x1050")
        self.attributes("-fullscreen", not TESTING)
        self.attributes("-topmost", not TESTING)
        self.overrideredirect(not TESTING)
        self.protocol("WM_DELETE_WINDOW", lambda: self.closeFun())

        self.screenwidth = 1680 # adjust
        self.screenheight = 1050 # adjust

        os.chdir(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
        filepath = os.path.join(os.getcwd(), "Data")
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        
        writeTime = localtime()
        self.id = str(uuid4())
        self.outputfile = os.path.join("Data", strftime("%y_%m_%d_%H%M%S", writeTime) + "_" + self.id + ".txt")

        self.bind("<Escape>", self.closeFun)

        self.order = frames

        self.texts = defaultdict(str)
        self.status = defaultdict(str)
                                    
        self.count = -1

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
                      
        with open(self.outputfile, mode = "w") as self.file:
            self.nextFrame()
            self.mainloop()
        

    def nextFrame(self):
        self.file.write("time: " + str(time()) + "\n")
        self.count += 1
        if self.count >= len(self.order):
            self.destroy()
        else:
            nxt = self.order[self.count]
            if isinstance(nxt, tuple):
                self.frame = nxt[0](self, **nxt[1])
            else:
                self.frame = nxt(self)
            self.frame.grid(row = 0, column = 0, sticky = (N, S, E, W))

            if hasattr(self.frame, "run"):
                self.update()
                self.frame.run()


    def closeFun(self, event = ""):
        if TESTING:
            self.destroy()
            return
        
        message = "Jste si jistí, že chcete studii předčasně ukončit? "
        ans = messagebox.askyesno(message = message, icon = "question", parent = self,
                                  title = "Ukončit studii?")
        if ans:
            self.destroy() 
