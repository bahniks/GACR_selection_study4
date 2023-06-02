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


q1 = "Uveďte v několika bodech či větách, jak jste se rozhodovali při stanovení maximální ceny, co jste byli ochotni zaplatit za verzi PŘED úlohy:"
q2 = "Uveďte v několika bodech či větách, jak jste se rozhodovali při dražbě verze PŘED úlohy:"


q3 = "Ohodnoťte do jaké míry jste zvažovali při stanovení maximální ceny,\nco jste byli ochotni zaplatit za verzi PŘED úlohy následující faktory:"
q4 = "Ohodnoťte do jaké míry jste zvažovali při dražbě verze PŘED úlohy následující faktory:"

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
                     "snahu být vítězem",
                     "snahu překonat ostatní"]


q5 = "Jak moc souhlasíte nebo nesouhlasíte s následujícími tvrzeními:"
dimensions2 = ["Stanovení maximální ceny za verzi PŘED bylo nespravedlivé.",
               "Stanovení maximální ceny za verzi PŘED bylo riskantní.",
               "Nerozuměl jsem účelu stanovení maximální ceny za verzi PŘED.",
               "Stanovení maximální ceny za verzi PŘED mi připadalo komplikované.",
               "Dražba verze PŘED byla nespravedlivá.",
               "Dražba verze PŘED byla riskantní.",
               "Nerozuměl jsem účelu dražeb.",
               "Dražba verze PŘED mi připadala komplikovaná."]
ds1 = "rozhodně\nnesouhlasím"
ds2 = "nesouhlasím"
ds3 = "spíše\nnesouhlasím"
ds4 = "spíše\nsouhlasím"
ds5 = "souhlasím"
ds6 = "rozhodně\nsouhlasím"


q6 = "Jak moc se podle Vás účastníci z Vaší skupiny zajímali o to,\nkolik charitativní organizace v experimentu ztratily?"
q7 = "Jak moc Vám záleželo na tom, kolik charitativní organizace v experimentu ztratily?"
dsb1 = "Vůbec ne"
dsb2 = "Jen trochu"
dsb3 = "Do určité míry"
dsb4 = "Spíše hodně"
dsb5 = "Velmi"

q8 = "Napadlo Vás, že je možné ve verzi PŘED podvádět; tedy stanovit,\nže jste uhodli hod kostky, i když jste jej neuhodli."
q9 = "Napadlo Vás, že je možné vydražit možnost hrát verzi PŘED, abyste zabránili\nostatním účastníkům brát peníze od charitativních organizací?"
q10 = "Napadlo Vás, že je možné vydražit možnost hrát verzi PŘED, abyste mohli nahlásit,\nže jste neuhodli hod kostky, když byste jinak mohli způsobit ztrátu charitě?"
yes = "Ano, napadlo mě to"
no = "Ne, nenapadlo mě to"

##################################################################################################################


       
class DebriefCheating1(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Debriefing1\n")

        self.question1 = Question(self, q1, alines = 5, qlines = 2, width = 60)
        self.question2 = Question(self, q2, alines = 5, width = 60)

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


class DebriefCheating2(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        items = debriefdimensions
        scale = [debriefscale1, debriefscale2, debriefscale3, debriefscale4, debriefscale5]

        self.frame1 = OneFrame(self, q3, items, scale)
        self.frame1.grid(row = 1, column = 1)

        self.frame2 = OneFrame(self, q4, items, scale)
        self.frame2.grid(row = 2, column = 1)            

        ttk.Style().configure("TButton", font = "helvetica 15")
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


class DebriefCheating3(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)       
        self.frame = OneFrame(self, q5, dimensions2, [ds1, ds2, ds3, ds4, ds5, ds6], wrap = 300)
        self.frame.grid(row = 1, column = 1)            

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun, state = "disabled")
        self.next.grid(row = 2, column = 1)

        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 1)        
        self.rowconfigure(2, weight = 2)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

    def check(self):
        if self.frame.check():
            self.next["state"] = "!disabled"
            return True

    def write(self):
        if self.check():
            self.file.write("Debriefing3\n" + self.id + "\t")
            self.frame.write()
            self.file.write("\n")



class OneFrame(Canvas):
    def __init__(self, root, question, items, scale, wrap = 480):
        super().__init__(root, background = "white", highlightbackground = "white", highlightcolor = "white")

        self.root = root
        self.file = self.root.file

        self.answers = scale
        
        self.lab1 = ttk.Label(self, text = question, font = "helvetica 15", background = "white")
        self.lab1.grid(row = 2, column = 1, pady = 10, columnspan = 2)
        self.measures = []
        for count, word in enumerate(items):
            self.measures.append(Measure(self, word, self.answers, "", "", function = self.root.check,
                                         labelPosition = "none"))
            self.measures[count].grid(row = count + 3, column = 1, columnspan = 2, sticky = E)
            self.measures[count].question["wraplength"] = wrap
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




class DebriefCheating4(ExperimentFrame):
    # smazat
    def __init__(self, root):
        super().__init__(root)

        self.question1 = Measure(self, q6, values = [dsb1, dsb2, dsb3, dsb4, dsb5], questionPosition = "above", left = "", right = "", labelPosition = "next", filler = 700)        
        self.question2 = Measure(self, q7, values = [dsb1, dsb2, dsb3, dsb4, dsb5], questionPosition = "above", left = "", right = "", labelPosition = "next", filler = 700)
        self.question3 = Measure(self, q8, values = [yes, no], questionPosition = "above", left = "", right = "", labelPosition = "next", filler = 650)
        self.question4 = Measure(self, q9, values = [yes, no], questionPosition = "above", left = "", right = "", labelPosition = "next", filler = 650)
        self.question5 = Measure(self, q10, values = [yes, no], questionPosition = "above", left = "", right = "", labelPosition = "next", filler = 650)        

        self.question1.question["font"] = "helvetica 15"
        self.question2.question["font"] = "helvetica 15"
        self.question3.question["font"] = "helvetica 15"
        self.question4.question["font"] = "helvetica 15"
        self.question5.question["font"] = "helvetica 15"

        self.question1.grid(row = 1, column = 1)
        self.question2.grid(row = 2, column = 1)
        self.question3.grid(row = 3, column = 1)        
        self.question4.grid(row = 4, column = 1)
        self.question5.grid(row = 5, column = 1)
        
        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun)
        self.next.grid(row = 6, column = 1)

        self.warning = ttk.Label(self, text = "Odpovězte prosím na všechny otázky.",
                                 background = "white", font = "helvetica 15", foreground = "white")
        self.warning.grid(row = 7, column = 1)

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
        self.rowconfigure(8, weight = 2)

        
    def check(self):
        return self.question1.answer.get() and self.question2.answer.get() and \
               self.question3.answer.get() and self.question4.answer.get() and \
               self.question5.answer.get()

    def back(self):
        self.warning.config(foreground = "red")

    def write(self):
        self.file.write("Debriefing4\n")
        self.file.write(self.id + "\t" + "\t".join([self.question1.answer.get(), self.question2.answer.get(), self.question3.answer.get(), self.question4.answer.get(), self.question5.answer.get()]))
        self.file.write("\n")


DebriefingInstructions = (InstructionsFrame, {"text": debriefingIntro, "height": 3})


def main():
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([DebriefingInstructions,
         DebriefCheating1, 
         DebriefCheating2, 
         DebriefCheating3, 
         DebriefCheating4])


if __name__ == "__main__":
    main()

