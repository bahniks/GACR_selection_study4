#! python3
from tkinter import *
from tkinter import ttk
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame, Measure
from gui import GUI




WIN = 35
CURRENCY = "Kč"



################################################################################
# TEXTS

debrieftext = """
Jak víte, úkol s kostkou měl dvě verze:

Verze “PŘED”, ve které činíte předpovědi před hodem kostkou. Po zvolení možnosti vidíte výsledek hodu a dozvíte se, zda jste uhodli či nikoliv, a kolik jste vydělali.
Verzi “PO”, ve které uvádíte, zda jste uhodli či nikoliv a kolik jste vydělali, až poté, co vidíte výsledek hodu  kostkou.
Ohodnoťte prosím do jaké míry souhlasíte či nesouhlasíte s následujícími výroky o každé verzi úkolu.
"""

debriefquest1 = "Do jaké míry souhlasíte s tím, že verze PŘED ..."
debriefquest2 = "Do jaké míry souhlasíte s tím, že verze PO ..."
debriefscale1 = "zcela nesouhlasím"
debriefscale2 = "nesouhlasím"
debriefscale3 = "souhlasím"
debriefscale4 = "zcela souhlasím"

debriefdimensions = ["... vyžadovala pozornost",
                     "... vyžadovala logické myšlení",
                     "... umožňovala podvádění",
                     "... byla zábavnější než druhá verze úkolu",
                     "... umožňovala ospravedlnit zveličení uhodnutých hodů",
                     "... sestávala z náhodně generovaných hodů kostkou"]





################################################################################

       
class DebriefCheating(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.text = Text(self, height = 8, width = 90, relief = "flat", font = "helvetica 15", wrap = "word")
        self.text.insert("1.0", debrieftext)
        self.text["state"] = "disabled"
        self.text.grid(row = 1, column = 1)

        self.frame1 = OneFrame(self, debriefquest1)
        self.frame1.grid(row = 2, column = 1)

        self.frame2 = OneFrame(self, debriefquest2)
        self.frame2.grid(row = 3, column = 1)            

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = 4, column = 1, sticky = N)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 2)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

    def check(self):
        if self.frame1.check() and self.frame2.check():
            self.next["state"] = "!disabled"
            return True

    def write(self):
        if self.check():
            self.file.write("Perception cheating\n" + self.id + "\t")
            self.frame1.write()
            self.file.write("\t")
            self.frame2.write()
            self.file.write("\n")



class OneFrame(Canvas):
    def __init__(self, root, question):
        super().__init__(root, background = "white", highlightbackground = "white",
                         highlightcolor = "white")

        self.root = root
        self.file = self.root.file

        self.answers = [debriefscale1, debriefscale2, debriefscale3, debriefscale4]
        
        self.lab1 = ttk.Label(self, text = question, font = "helvetica 15", background = "white")
        self.lab1.grid(row = 2, column = 1, pady = 10)
        self.measures = []
        for count, word in enumerate(debriefdimensions):
            self.measures.append(Measure(self, word, self.answers, "", "", function = self.root.check,
                                         labelPosition = "none"))
            self.measures[count].grid(row = count + 3, column = 1, columnspan = 2, sticky = E)

    def check(self):
        for measure in self.measures:
            if not measure.answer.get():
                return False
        else:
            return True             

    def write(self):
        for num, measure in enumerate(self.measures):
            self.file.write(str(self.answers.index(measure.answer.get()) + 1))
            if num != len(self.measures) - 1:
                self.file.write("\t")
     






if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([DebriefCheating
         ])
