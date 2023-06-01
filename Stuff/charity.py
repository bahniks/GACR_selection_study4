#! python3
from tkinter import *
from tkinter import ttk

import os
import random

from common import ExperimentFrame
from gui import GUI


################################################################################
# TEXTS

charities = ["Červený kříž",
             "Člověk v tísni",
             "Charita Česká republika",
             "Konto bariér"]

instructions = """
V následující úloze máte možnost získat peníze pro sebe a pro charitativní organizaci dle Vašeho výběru. 

Na výběr máte z následujících čtyř charitativních organizací:

Červený kříž: Chrání životy, zdraví, důstojnost a snižuje utrpení lidí v nouzi následkem válek, přírodních nebo technických katastrof a epidemií.

Člověk v tísni: Poskytuje okamžitou humanitární pomoc a pomáhá lidem postavit se na vlastní nohy. Podporuje vzdělávání dětí, pomáhá nejchudším a nejzranitelnějším, podporuje obránce lidských práv.

Charita Česká republika: Hlavní náplní její činnosti je pomoc potřebným v ČR, mimo to ale také organizuje humanitární pomoc a dobročinné programy pro zahraničí (např. sbírky v případě živelních katastrof nebo adopce na dálku).

Konto bariér: Pomáhá lidem s handicapem a organizacím, které o ně pečují. Jejím cílem je vracet handicapované zpět do života.


Vyberte si prosím organizaci, již byste chtěli podpořit:
"""



################################################################################


class Charity(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)          
      
        self.charity = StringVar()

        self.text = Text(self, font = "helvetica 15", relief = "flat", background = "white", height = 22,
                         wrap = "word", highlightbackground = "white", width = 80)
        self.text.grid(row = 1, column = 0, columnspan = 4)
        self.text.insert("1.0", instructions)
        self.text.config(state = "disabled")

        self.labels = {}
        self.rbuttons = {}
        for i, char in enumerate(charities):
            row = i + 4
            self.labels[i] = ttk.Label(self, text = char, background = "white", font = "helvetica 15")
            self.labels[i].grid(column = 1, row = row, pady = 2, sticky = W, padx = 20)
            self.rbuttons[i] = ttk.Radiobutton(self, text = "", variable = self.charity,
                                               value = char, command = self.checkCharity)
            self.rbuttons[i].grid(column = 2, row = row, sticky = W)

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
        ttk.Style().configure("TButton", font = "helvetica 15")

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(9, weight = 2)
        self.rowconfigure(10, weight = 2)

        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun)
        self.next["state"] = "disabled"
        self.next.grid(row = 9, column = 0, columnspan = 4, pady = 15)


    def checkCharity(self):
        self.next["state"] = "!disabled"


    def write(self):
        self.file.write("Charity\n")
        charity = self.charity.get()
        self.root.texts["charity"] = charity
        self.file.write("\t".join([self.id, charity]) + "\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Charity])
