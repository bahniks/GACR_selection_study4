#! python3

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import time, localtime, strftime, sleep

import random
import os.path
import os

from common import ExperimentFrame, InstructionsFrame, read_all, Measure
from gui import GUI



##################################################################################################################
# TEXTS #
#########
debriefingIntro = "V následující části se Vás zeptáme na Váš pohled na předchozí úlohu a na Vaše rozhodování v ní."


q1 = "Uveďte v několika bodech či větách, jak jste se rozhodovali při volbě, jakou budete hrát verzi úlohy ve třetím kole, kde jste se rozhodoval(a) pouze o tom, jakou verzi úlohy budete hrát Vy:"
q2 = "Uveďte v několika bodech či větách, jak jste se rozhodovali při volbě, jakou budete hrát verzi úlohy ve čtvrtém a pátém kole, kde jste se rozhodoval(a) o tom, jakou verzi úlohy bude hrát celá Vaše skupina:"


##################################################################################################################



class DebriefCheating(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Debriefing1\n")

        self.question1 = Question(self, q1, alines = 6, qlines = 3, width = 60)
        self.question2 = Question(self, q2, alines = 6, qlines = 3, width = 60)

        self.question1.grid(row = 1, column = 1)
        self.question2.grid(row = 2, column = 1)
        
        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun)
        self.next.grid(row = 3, column = 1)

        self.warning = ttk.Label(self, text = "Odpovězte prosím na všechny otázky.",
                                 background = "white", font = "helvetica 15", foreground = "white")
        self.warning.grid(row = 4, column = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 2)

        
    def check(self):
        return self.question1.check() and self.question2.check()

    def back(self):
        self.warning.config(foreground = "red")

    def write(self):
        self.file.write(self.id + "\t")
        self.question1.write(newline = False)
        self.file.write("\t")
        self.question2.write(newline = False)
        self.file.write("\n")

    def gothrough(self):
        self.question1.field.insert("1.0", "Testovací odpověď na otázku 1.")
        self.question2.field.insert("1.0", "Testovací odpověď na otázku 2.")
        self.next.invoke()



class Question(Canvas):
    def __init__(self, root, text, width = 80, qlines = 2, alines = 5):
        super().__init__(root)
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        self.root = root

        self.answer = StringVar()

        self.label = Text(self, width = width, wrap = "word", font = "helvetica 15",
                          relief = "flat", height = qlines, cursor = "arrow",
                          selectbackground = "white", selectforeground = "black")
        self.label.insert("1.0", text)
        self.label.config(state = "disabled")
        self.label.grid(column = 0, row = 0)

        self.field = Text(self, width = int(width*1.2), wrap = "word", font = "helvetica 15",
                          height = alines, relief = "solid")
        self.field.grid(column = 0, row = 1, pady = 6)

        self.columnconfigure(0, weight = 1)


    def check(self):
        return self.field.get("1.0", "end").strip()

    def write(self, newline = True):
        self.root.file.write(self.field.get("1.0", "end").replace("\n", "  ").replace("\t", " "))
        if newline:
            self.root.file.write("\n")

    def disable(self):
        self.field.config(state = "disabled")




DebriefingInstructions = (InstructionsFrame, {"text": debriefingIntro, "height": 3})


def main():
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([DebriefingInstructions,
         DebriefCheating])


if __name__ == "__main__":
    main()

