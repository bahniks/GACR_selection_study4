#! python3
from tkinter import *
from tkinter import ttk

import os
import random
import urllib.request
import urllib.parse

from collections import OrderedDict
from time import sleep

from common import InstructionsFrame
from gui import GUI
from constants import URL, TESTING, GOTHROUGH


options = (1,2,3,4,6,8,10)
BASE = 10

################################################################################
# TEXTS

instructions = f"""V následujícím úkolu uděláte 7 nezávislých rozhodnutí mezi dvěma možnostmi. Pokud zvolíte první možnost, nic se nestane. Pokud zvolíte druhou možnost, ztratíte {BASE} Kč ze své výhry. Jiný účastník studie, se kterým jste ještě nebyli spárováni, obdrží částku, která je u této možnosti napsána. Další účastník bude podobně dělat rozhodnutí, která mohou ovlivnit Vaši odměnu. Svou identitu navzájem nebudete znát.

Až tuto úlohu dokončíte, bude vybráno náhodně jedno ze 7 rozhodnutí (každé se stejnou pravděpodobností) a, podle Vaší volby v daném rozhodnutí, se nestane nic nebo ztratíte {BASE} Kč a jiný účastník obdrží částku uvedenou u daného rozhodnutí. I když učiníte 7 rozhodnutí, pouze jedno z nich bude tedy rozhodovat o tom, jak bude ovlivněna Vaše odměna a odměna dalšího účastníka. Výsledek se dozvíte na konci studie.

V každém z 7 řádků se rozhodněte a vyberte prosím, zda preferujete "Nic" nebo "Darování"."""

noneResult = f"V úloze, kde jste volil(a), zda přispět jinému účastníkovi studie, jste mohl(a) zvolit, zda tento účastník obdrží {{0}} Kč a vy ztratíte {BASE} Kč. Zvolil(a) jste možnost 'Nic'. Neztratíte tedy žádné peníze a druhý účastník nic nedostane."

donationResult = f"V úloze, kde jste volil(a), zda přispět jinému účastníkovi studie, jste mohl(a) zvolit, zda tento účastník obdrží {{0}} Kč a vy ztratíte {BASE} Kč. Zvolil(a) jste možnost 'Darování'. Ztratil(a) jste tedy {BASE} Kč a jiný účastník obdržel {{0}} Kč."

wait_text = "Prosím počkejte na ostatní účastníky studie."
################################################################################

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
        self.labels = {}
        for i in range(7):
            row = i + 4
            self.variables[i] = StringVar()
            self.rbuttonsL[i] = ttk.Radiobutton(self, text = "Žádné změny odměn",
                                                variable = self.variables[i], value = str(i+1) + "none",
                                                command = self.checkAllFilled)
            self.rbuttonsL[i].grid(column = 1, row = row, sticky = W, padx = 30, pady = 5)
            self.rbuttonsR[i] = ttk.Radiobutton(self, variable = self.variables[i], value = str(i+1) + "donation",
                                                text = f"Vy: -{BASE} Kč   Další účastník: +{options[i] * BASE} Kč",
                                                command = self.checkAllFilled)
            self.rbuttonsR[i].grid(column = 2, row = row, sticky = W, padx = 30, pady = 5)
            self.labels[i] = ttk.Label(self, text = f"{i+1})", font = "helvetica 15", background = "white")
            self.labels[i].grid(column = 0, row = row, sticky = NE, padx = 10, pady = 5)

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
            other = self.options[selected - 1] * BASE
        else:
            #self.root.texts["contribution_chosen"] = "none"
            self.root.status["results"] += [noneResult.format(self.options[selected - 1] * BASE)]
            other = 0
        self.file.write("Contribution\n")  
        self.file.write("\t".join([self.id] + [var.get() for var in self.variables.values()] + [str(selected)]) + "\n\n")
        data = {'id': self.id, 'round': "contribution", 'offer': other}
        self.sendData(data)


    def gothrough(self):
        for i in range(7):
            if random.random() < 0.5:
                self.rbuttonsL[i].invoke()
            else:
                self.rbuttonsR[i].invoke()        
        self.update()
        sleep(0.5)
        self.next.invoke()




class WaitContribution(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = wait_text, height = 3, font = 15, proceed = False, width = 45)        
        self.progressBar = ttk.Progressbar(self, orient = HORIZONTAL, length = 400, mode = 'indeterminate')
        self.progressBar.grid(row = 2, column = 1, sticky = N)

    def checkOffers(self):
        count = 0
        while True:
            self.update()
            if count % 50 == 0:
                data = urllib.parse.urlencode({'id': self.id, 'round': "contribution_received", 'offer': "check"})
                data = data.encode('ascii')
                if URL == "TEST":
                    response = random.choice([str(i * 10) for i in options] + ["0", "0", "0", "0", "0"])
                else:
                    try:
                        with urllib.request.urlopen(URL, data = data) as f:
                            response = f.read().decode("utf-8")       
                    except Exception as e:
                        if TESTING:
                            print(e)
                            continue
                        else:
                            continue
                if response:
                    self.root.status["reward"] += int(response)
                    if response == "0":
                        additional = "V úloze, kde Vám jiný účastník mohl darovat peníze se pro náhodně vybranou volbu rozhodl nepřispět. Nezískal(a) jste tedy žádné další peníze."
                    else:
                        additional = "V úloze, kde Vám jiný účastník mohl darovat peníze se pro náhodně vybranou volbu rozhodl Vám přispět. Získal(a) jste tedy {} Kč.".format(response)
                    self.root.status["results"] += [additional]
                    self.write(response)
                    self.progressBar.stop()
                    self.nextFun()  
                    return
            count += 1
            sleep(0.1)

    def run(self):
        self.progressBar.start()
        self.checkOffers()

    def write(self, response):
        self.file.write("Contribution Result" + "\n")
        self.file.write(self.id + "\t" + response + "\n\n")        

    def gothrough(self):
        self.run()






if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Contribution])