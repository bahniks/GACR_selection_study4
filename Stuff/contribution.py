#! python3
from tkinter import *
from tkinter import ttk

import os
import random

from collections import OrderedDict

from common import InstructionsFrame
from gui import GUI



options = (1,2,3,4,6,8,10)
BASE = 10

instructions = f"""V následujícím úkolu uděláte 7 nezávislých rozhodnutí mezi dvěma možnostmi. Pokud zvolíte první možnost, nic se nestane. Pokud zvolíte druhou možnost, ztratíte {BASE} Kč ze své výhry. Jiný účastník studie, se kterým jste ještě nebyli spárováni, obdrží částku, která je u této možnosti napsána. Jiný účastník bude podobně dělat rozhodnutí, která mohou ovlivnit Vaši odměnu.

Až tuto úlohu dokončíte, bude vybráno náhodně jedno z rozhodnutí (každé se stejnou pravděpodobností) a nestane se nic nebo ztratíte {BASE} Kč a jiný účastník obdrží částku uvedenou u daného rozhodnutí. I když učiníte 7 rozhodnutí, pouze jedno z nich bude tedy rozhodovat o tom, jak bude ovlivněna Vaše odměna a odměna dalšího účastníka. Výsledek se dozvíte na konci studie.

V každém z 7 řádků se rozhodněte a vyberte prosím, zda preferujete jistou odměnu nebo loterii."""

noneResult = f"V úloze, kde jste volil(a), zda přispět jinému účastníkovi studie, jste mohl(a) zvolit, zda tento účastník obdrží {{0}} Kč a vy ztratíte {BASE} Kč. Zvolil(a) jste možnost 'Nic'. Neztratíte tedy žádné peníze a druhý účastník nic nedostane."

donationResult = f"V úloze, kde jste volil(a), zda přispět jinému účastníkovi studie, jste mohl(a) zvolit, zda tento účastník obdrží {{0}} Kč a vy ztratíte {BASE} Kč. Zvolil(a) jste možnost 'Darování'. Ztratil(a) jste tedy {BASE} Kč a jiný účastník obdržel {{0}} Kč."


class Contribution(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = instructions, proceed = True, height = "auto", savedata = True)
        self.text.grid(row = 1, column = 0, columnspan = 4)
        self.options = options           

        self.leftLabel = ttk.Label(self, text = "Nic", font = "helvetica 15 bold", background = "white")
        self.leftLabel.grid(row = 3, column = 1, pady = 10)
        self.rightLabel = ttk.Label(self, text = "Darování", font = "helvetica 15 bold", background = "white")
        self.rightLabel.grid(row = 3, column = 2, pady = 10)

        self.variables = OrderedDict()
        self.rbuttonsL = {}
        self.rbuttonsR = {}
        for i in range(7):
            row = i + 4
            self.variables[i] = StringVar()
            self.rbuttonsL[i] = ttk.Radiobutton(self, text = "Beze změn odměn",
                                                variable = self.variables[i], value = str(i+1) + "none",
                                                command = self.checkAllFilled)
            self.rbuttonsL[i].grid(column = 1, row = row, sticky = W, padx = 30)
            self.rbuttonsR[i] = ttk.Radiobutton(self, variable = self.variables[i], value = str(i+1) + "donation",
                                                text = f"Vy: -{BASE} Kč   Další účastník: +{options[i] * BASE} Kč",
                                                command = self.checkAllFilled)
            self.rbuttonsR[i].grid(column = 2, row = row, sticky = W, padx = 30)

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
        ttk.Style().configure("TButton", font = "helvetica 15")

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 0)
        self.columnconfigure(2, weight = 0)
        self.columnconfigure(3, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 0)
        self.rowconfigure(4, weight = 0)
        self.rowconfigure(11, weight = 1)
        self.rowconfigure(12, weight = 1)

        self.next.grid(row = 11, column = 0, columnspan = 4, pady = 15)
        self.next["state"] = "disabled"
        

    def checkAllFilled(self):
        if all([var.get() for var in self.variables.values()]):
            self.next["state"] = "!disabled"


    def write(self):
        selected = random.randint(1, 7)
        #self.root.texts["contribution_selected"] = selected
        if "donation" in self.variables[selected - 1].get():
            #self.root.texts["contribution_chosen"] = "donation"
            self.root.status["results"] += [donationResult.format(self.options[selected - 1] * BASE)]
            self.root.status["reward"] -= BASE            
        else:
            #self.root.texts["contribution_chosen"] = "none"
            self.root.status["results"] += [noneResult.format(self.options[selected - 1] * BASE)]
        self.file.write("Contribution\n")     
        print(self.root.status["results"])        
        self.file.write("\t".join([self.id] + [var.get() for var in self.variables.values()] + [str(selected)]) + "\n")




if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Contribution])