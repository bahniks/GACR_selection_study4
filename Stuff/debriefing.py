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

intro = "V této a následující části máme zájem zjistit vaše názory na tento experiment. Prosím, napište svůj názor v několika bodech či větách."
q1 = "Máte nějaké připomínky k průběhu experimentu? (Například: nejasné pokyny, nepřehledné uživatelské rozhraní, problematické chování experimentátorů nebo jiných účastníků, cokoliv, co byste udělali jinak apod.)"
q2 = "Jaký byl podle vašeho názoru výzkumný záměr v úkolu, ve kterém jste museli předpovídat, zda na kostce padne liché, nebo sudé číslo?"
q3 = "Myslíte si, že jste správně odhadli, jaký je výzkumný záměr experimentátorů v  úkolu s hádáním strany u kostky?"
q3b = "Snažili jste se vyjít vstříc výzkumnému záměru experimentátorů v úkolu s hádáním hodu u kostky nebo jste se naopak chovali opačně?"
q3bvalues = ["nezvažoval(a) jsem záměr experimentátorů", "chtěl(a) jsem vyjít vstříc experimentátorům", "nechtěl(a) jsem vyjít vstříc experimentátorům"]
q4 = 'Myslíte si, že by bylo nemorální ve verzi "PO" uvádět větší počet správně uhodnutých hodů, abyste vydělali více peněz? Uveďte prosím také důvod své odpovědi.'
q5 = "Myslíte si, že byly všechny informace, jež jste během experimentu dostali, pravdivé?"
q5values = ["ano", "nejsem si jist/a", "ne"]




q1 = "Uveďte v několika bodech či větách, jak jste se rozhodovali při stanovení maximální ceny, co jste byli ochotni zaplatit za verzi PŘED úlohy:"
q2 = "Uveďte v několika bodech či větách, jak jste se rozhodovali při dražbě verze PŘED úlohy:"


q3 = "Ohodnoťte do jaké míry jste zvažovali při dražbě verze PŘED úlohy následující faktory:"
q4 = "Ohodnoťte do jaké míry jste zvažovali při stanovení maximální ceny,\nco jste byli ochotni zaplatit za verzi PŘED úlohy následující faktory:"

debriefscale1 = "Vůbec ne"
debriefscale2 = "Jen trochu"
debriefscale3 = "Do určité míry"
debriefscale4 = "Spíše hodně"
debriefscale5 = "Velmi"

debriefdimensions = ["svůj očekávaný peněžní výdělek",
                     "ztrátu peněz, kterou mohu způsobit charitě",
                     "ztrátu peněz, kterou mohou způsobit charitě ostatní členové týmu",
                     "částku, kterou nabídnou ostatní členové týmu",
                     "počet správných předpovědí, které uvedou ostatní členové týmu ve verzi PŘED",
                     "nakolik je zábavné hrát obě verze úlohy",
                     "nakolik je jednoduché hrát obě verze úlohy",
                     "schopnost ovlivnit velikost svého peněžního výdělku",
                     "schopnost ovlivnit velikost ztráty charity",
                     "snaha být vítězem",
                     "snaha překonat ostatní"]



       
class DebriefCheating1(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Debriefing1\n")

        self.question1 = Question(self, q1, alines = 5, qlines = 2, width = 60)
        self.question2 = Question(self, q2, alines = 5, width = 60)

        self.question1.grid(row = 1, column = 1)
        self.question2.grid(row = 2, column = 1)
        
        ttk.Style().configure("TButton", font = "helvetica 16")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun)
        self.next.grid(row = 3, column = 1)

        self.warning = ttk.Label(self, text = "Odpovězte prosím na všechny otázky.",
                                 background = "white", font = "helvetica 16", foreground = "white")
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


class Question(Canvas):
    def __init__(self, root, text, width = 80, qlines = 2, alines = 5):
        super().__init__(root)
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        self.root = root

        self.answer = StringVar()

        self.label = Text(self, width = width, wrap = "word", font = "helvetica 16",
                          relief = "flat", height = qlines, cursor = "arrow",
                          selectbackground = "white", selectforeground = "black")
        self.label.insert("1.0", text)
        self.label.config(state = "disabled")
        self.label.grid(column = 0, row = 0)

        self.field = Text(self, width = int(width*1.2), wrap = "word", font = "helvetica 16",
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


class DebriefCheating2(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)
        self.frame1 = OneFrame(self, q3)
        self.frame1.grid(row = 1, column = 1)

        self.frame2 = OneFrame(self, q4)
        self.frame2.grid(row = 2, column = 1)            

        ttk.Style().configure("TButton", font = "helvetica 16")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = 3, column = 1)

        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 2)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

    def check(self):
        if self.frame1.check() and self.frame2.check():
            self.next["state"] = "!disabled"
            return True

    def write(self):
        if self.check():
            self.file.write("Debriefing2\n" + self.id + "\t")
            self.frame1.write()
            self.file.write("\t")
            self.frame2.write()
            self.file.write("\n")



class OneFrame(Canvas):
    def __init__(self, root, question):
        super().__init__(root, background = "white", highlightbackground = "white", highlightcolor = "white")

        self.root = root
        self.file = self.root.file

        self.answers = [debriefscale1, debriefscale2, debriefscale3, debriefscale4, debriefscale5]
        
        self.lab1 = ttk.Label(self, text = question, font = "helvetica 16", background = "white")
        self.lab1.grid(row = 2, column = 1, pady = 10, columnspan = 2)
        self.measures = []
        for count, word in enumerate(debriefdimensions):
            self.measures.append(Measure(self, word, self.answers, "", "", function = self.root.check,
                                         labelPosition = "none"))
            self.measures[count].grid(row = count + 3, column = 1, columnspan = 2, sticky = E)
            self.measures[count].question["wraplength"] = 480
            self.measures[count].question["justify"] = "right"


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


class Debriefing(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Debriefing\n")

        self.text = Text(self, font = "helvetica 15", relief = "flat",
                         background = "white", width = 80, height = 3, wrap = "word",
                         highlightbackground = "white")
        self.text.grid(row = 0, column = 1, sticky = S)
        self.text.insert("1.0", intro)
        self.text["state"] = "disabled"

        self.question1 = Question(self, q1, alines = 2, qlines = 3)
        self.question2 = Question(self, q2, alines = 2)
        self.question3 = Question(self, q3, alines = 2)
        self.question3b = Measure(self, q3b, values = q3bvalues, questionPosition = "above",
                                 left = "", right = "", labelPosition = "next")
        self.question3b.question["font"] = "helvetica 15"
        self.question4 = Question(self, q4, alines = 2)
        self.question5 = Measure(self, q5, values = q5values, questionPosition = "above",
                                 left = "", right = "", labelPosition = "next", filler = 550)
        self.question5.question.grid(column = 0, row = 0, columnspan = 2, pady = 6)
        self.question5.question["font"] = "helvetica 15"

        self.question1.grid(row = 1, column = 1)
        self.question2.grid(row = 2, column = 1)
        self.question3.grid(row = 3, column = 1)
        self.question3b.grid(row = 4, column = 1)
        self.question4.grid(row = 5, column = 1)
        self.question5.grid(row = 6, column = 1)
        
        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun)
        self.next.grid(row = 7, column = 1)

        self.warning = ttk.Label(self, text = "Odpovězte prosím na všechny otázky.",
                                 background = "white", font = "helvetica 15", foreground = "white")
        self.warning.grid(row = 8, column = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 1)
        self.rowconfigure(7, weight = 1)
        self.rowconfigure(8, weight = 1)
        self.rowconfigure(9, weight = 2)

        
    def check(self):
        return self.question1.check() and self.question2.check() and \
               self.question3.check() and self.question4.check() and \
               self.question3b.answer.get() and self.question5.answer.get()

    def back(self):
        self.warning.config(foreground = "red")

    def write(self):
        self.file.write(self.id + "\t")
        self.question1.write(newline = False)
        self.file.write("\t")
        self.question2.write(newline = False)
        self.file.write("\t")
        self.question3.write(newline = False)
        self.file.write("\t")
        self.question3b.write()
        self.file.write("\t")
        self.question4.write(newline = False)
        self.file.write("\t")
        self.question5.write()
        self.file.write("\n")

       



            

def main():
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([DebriefCheating2])


if __name__ == "__main__":
    main()

