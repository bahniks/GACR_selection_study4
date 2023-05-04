#! python3
from tkinter import *
from tkinter import ttk
from collections import deque
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame
from gui import GUI
from constants import TESTING


intro1 = """V následující úloze budete srovnávat vlasnosti různých objektů s náhodnými hodnotami.

Náhodné hodnoty jsou generovány po zmáčknutí tlačítka 'Znáhodnit' a jsou určeny hodnotami zobrazených na třech "kotoučích" s číslicemi (obrázek kotoučů lze vidět níže). Tyto hodnoty budou v rozsahu od 1 do 1000. S hodnotou 1000 budete srovnávat objekt, pokud bude na všech kotoučích zobrazeno '0'.
"""


intro2 = """V následující úloze budete odhadovat vlastnosti různých objektů.
"""



items = [["subway", "vzdálenost tratě metra mezi stanicemi metra Muzeum a Hlavní nádraží"],
         ["soccer", "délka typického fotbalového hřiště"],
         ["tree", "výška nejvyššího stromu světa"],
         ["eiffel", "výška Eiffelovy věže"],
         ["vaclav", "délka Václavského náměstí"],
         ["ship", "délka nejdelší lodě"],
         ["skyscraper", "výška nejvyššího mrakodrapu Burj Khalifa"],
         ["waterfall", "výška nejvyššího vodopádu Salto Angel"],
         ["viaduct", "výška nejvyššího mostu, viaduktu Millau,"],
         ["bridge", "délka Nuselského mostu"],
         ["pyramid", "výška nejvyšší (Chufuovy) pyramidy v Gíze"],
         ["petrin", "délka lanové dráhy na Petřín"],
         ["strahov", "délka Velkého strahovského stadionu"]
         ]

random.shuffle(items)


class Comparison(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Comparison\n")

        self.random = ttk.Button(self, text = "Znáhodnit", command = self.randomize)
        self.random.grid(row = 1, column = 1, columnspan = 2)

        self.slotwidth = 300
        self.slotheight = 150
        self.slot = Canvas(self, width = self.slotwidth+2, height = self.slotheight, background = "white",
                           highlightbackground = "black")
        self.slot.grid(row = 2, column = 1, columnspan = 2)

        self.instruction = 'Zmáčkněte tlačítko "Znáhodnit" pro výběr náhodného čísla'
        self.upper = Text(self, font = "helvetica 20", relief = "flat", background = "white",
                          width = 80, height = 1, pady = 7, wrap = "word")
        self.upper.grid(row = 0, column = 1, columnspan = 2, sticky = S)
        self.upper.tag_configure("center", justify = "center")
        self.upper.insert("1.0", self.instruction, "center")
        self.upper["state"] = "disabled"

        self.question = "Je {} menší nebo větší než {} m?"
        self.text = Text(self, font = "helvetica 20", relief = "flat", background = "white",
                         width = 85, height = 1, pady = 7, wrap = "word")
        self.text.grid(row = 3, column = 1, columnspan = 2, sticky = S)
        self.text.tag_configure("center", justify = "center")

        ttk.Style().configure("TButton", font = "helvetica 18")
        
        self.lower = ttk.Button(self, text = "Menší", command = self.lowerResponse)
        self.higher = ttk.Button(self, text = "Větší", command = self.higherResponse)

        self.blank = Canvas(self, height = 50, width = 1, background = "white",
                           highlightbackground = "white")
        self.blank.grid(row = 5, column = 0)

        self.columnconfigure(0, weight = 4)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 4)
        
        self.rowconfigure(0, weight = 7)
        self.rowconfigure(1, weight = 4)
        self.rowconfigure(3, weight = 5)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 2)
        self.rowconfigure(6, weight = 10)

        self.number = 0

        self.createSlots()


    def createSlots(self):          
        self.slot.create_rectangle((3, 3, self.slotwidth/3 + 3, self.slotheight), width = 3)
        self.slot.create_rectangle((self.slotwidth/3 + 3, 3, 2*self.slotwidth/3 + 3, self.slotheight), width = 3)
        self.slot.create_rectangle((2*self.slotwidth/3 + 3, 3, self.slotwidth + 3, self.slotheight), width = 3)

        self.slot.create_polygon((0, self.slotheight/2 + 10,
                                  0, self.slotheight/2 - 10,
                                  15, self.slotheight/2), fill = "black")
        self.slot.create_polygon((self.slotwidth + 5, self.slotheight/2 + 10,
                                  self.slotwidth + 5, self.slotheight/2 - 10,
                                  self.slotwidth - 10, self.slotheight/2), fill = "black")

        self.numbers = []
        
        self.one = random.randint(0, 9)
        self.two = random.randint(0, 9)
        self.three = random.randint(0, 9)

        for i in range(-4, 6):
            self.numbers.append((self.slot.create_text((self.slotwidth/6 + 5, 13*i*self.slotheight/30 + self.slotheight/2),
                                                       text = (self.one+i) % 10, font = "helvetica 45"), 1, (self.one+i) % 10))
            self.numbers.append((self.slot.create_text((3*self.slotwidth/6 + 5, 13*i*self.slotheight/30 + self.slotheight/2),
                                                       text = (self.two+i) % 10, font = "helvetica 45"), 2, (self.two+i) % 10))
            self.numbers.append((self.slot.create_text((5*self.slotwidth/6 + 5, 13*i*self.slotheight/30 + self.slotheight/2),
                                                       text = (self.three+i) % 10, font = "helvetica 45"), 3, (self.three+i) % 10))


    def randomize(self):
        self.random["state"] = "disabled"
        self.upper["state"] = "normal"
        self.upper.delete("1.0", "end")
        self.upper["state"] = "disabled"
        
        self.starttime = perf_counter()
        self.time0 = self.starttime
        self.time = self.time0
        duration = random.randint(5, 6) if not TESTING else 0.2
        self.endtime = self.time + duration

        ends = [1,2,3]
        random.shuffle(ends)
        self.anchor = random.randint(1, 1000)
        stranchor = "{:03d}".format(self.anchor)
        ends[0] += (int(stranchor[-3]) - self.one)/20
        ends[1] += (int(stranchor[-2]) - self.two)/20
        ends[2] += (int(stranchor[-1]) - self.three)/20

        distances = [(duration - ends[i])*1300 for i in range(3)]
        endPositions = {}
        endPositions[1] = [((i - int(stranchor[-3]) + 9)%10 - 8)*self.slotheight*13/30 + self.slotheight/2 for i in range(10)]
        endPositions[2] = [((i - int(stranchor[-2]) + 9)%10 - 8)*self.slotheight*13/30 + self.slotheight/2 for i in range(10)]
        endPositions[3] = [((i - int(stranchor[-1]) + 9)%10 - 8)*self.slotheight*13/30 + self.slotheight/2 for i in range(10)]
        
        while self.time < self.endtime:
            self.time = perf_counter()
            for obj in self.numbers:
                x, y = self.slot.coords(obj[0])
                if distances[obj[1]-1] < 0:
                    y = endPositions[obj[1]][obj[2]-1]
                else:
                    y += (self.time - self.time0) * 1300
                    if y > 1.2*self.slotheight:
                        y -= self.slotheight*13*10/30
                self.slot.coords(obj[0], x, y)
            distances = [i - (self.time - self.time0) * 1300 for i in distances]
            self.time0 = self.time
            self.update()
        
        self.one = int(stranchor[-3])
        self.two = int(stranchor[-2])
        self.three = int(stranchor[-1])
            
        self.displayQuestion()
        

    def lowerResponse(self):
        self.response("lower")

    def higherResponse(self):
        self.response("higher")        

    def displayQuestion(self):
        self.text["state"] = "normal"
        self.text.insert("end", self.question.format(items[self.number][1], self.anchor), "center")
        self.text["state"] = "disabled"

        self.lower.grid(row = 5, column = 1, sticky = E, padx = 20)
        self.higher.grid(row = 5, column = 2, sticky = W, padx = 20)
        self.lower["state"] = "!disabled"
        self.higher["state"] = "!disabled"
        self.t0 = perf_counter()


    def response(self, answer):
        self.file.write("\t".join([self.id, items[self.number][0], str(self.anchor), answer, str(perf_counter() - self.t0)]) + "\n")
        self.number += 1
        self.proceed()

    def proceed(self):
        if self.number == len(items):
            self.nextFun()
        else:
            self.text["state"] = "normal"
            self.text.delete("1.0", "end")
            self.text["state"] = "disabled"
            self.lower.grid_forget()
            self.higher.grid_forget()
            self.lower["state"] = "disabled"
            self.higher["state"] = "disabled"
            self.random["state"] = "normal"
            self.upper["state"] = "normal"
            self.upper.insert("1.0", self.instruction, "center")
            self.upper["state"] = "disabled"



class Absolute(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Abolute\n")

        self.answerVar = StringVar()
        
        self.question = "Jaká je {} v metrech?"
        self.text = Text(self, font = "helvetica 20", relief = "flat", background = "white",
                         width = 80, height = 1, pady = 7, wrap = "word")
        self.text.grid(row = 1, column = 1, columnspan = 2, sticky = S)
        self.text.tag_configure("center", justify = "center")

        self.answer = ttk.Entry(self, textvariable = self.answerVar, font = "helvetica 20", width = 8)
        self.answer.grid(row = 2, column = 1, sticky = E, pady = 10)

        self.meters = ttk.Label(self, text = "m", font = "helvetica 20", background = "white")
        self.meters.grid(row = 2, column = 2, sticky = W, pady = 10, padx = 5)

        self.warning = ttk.Label(self, text = "Odpověď musí být kladné číslo!\n(pro desetinná místa použijte tečku)", font = "helvetica 20",
                                 background = "white", foreground = "white", justify = "center", state = "disabled")
        self.warning.grid(row = 4, column = 1, columnspan = 2)

        ttk.Style().configure("TButton", font = "helvetica 18")        
        self.next = ttk.Button(self, text = "Pokračovat", command = self.proceed)
        self.next.grid(row = 3, column = 1, columnspan = 2, pady = 50)

        self.columnconfigure(0, weight = 4)
        self.columnconfigure(3, weight = 4)
        
        self.rowconfigure(0, weight = 7)
        self.rowconfigure(4, weight = 4)
        self.rowconfigure(5, weight = 4)

        self.number = 0

        self.displayQuestion()
        

    def displayQuestion(self):
        self.warning["foreground"] = "white"
        self.answerVar.set("")
        self.text["state"] = "normal"
        self.text.delete("1.0", "end")
        self.text.insert("1.0", self.question.format(items[self.number][1]), "center")
        self.text["state"] = "disabled"
        self.t0 = perf_counter()
        

    def proceed(self):
        try:
            float(self.answerVar.get())
            if float(self.answerVar.get()) < 0:
                self.warning["foreground"] = "red"
                return
        except:
            self.warning["foreground"] = "red"
            return

        self.file.write("\t".join([self.id, items[self.number][0], self.answerVar.get(), str(perf_counter() - self.t0)]) + "\n")
        
        self.number += 1
        
        if self.number == len(items):
            self.nextFun()
        else:
            self.displayQuestion()



class SlotInstructions(InstructionsFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.slotwidth = 300
        self.slotheight = 150
        self.slot = Canvas(self, width = self.slotwidth+2, height = self.slotheight, background = "white",
                           highlightbackground = "black")
        self.slot.grid(row = 2, column = 1)

        self.next.grid(row = 3, column = 1)

        self.createSlots()

        self.rowconfigure(4, weight = 2)


    def createSlots(self):          
        self.slot.create_rectangle((3, 3, self.slotwidth/3 + 3, self.slotheight), width = 3)
        self.slot.create_rectangle((self.slotwidth/3 + 3, 3, 2*self.slotwidth/3 + 3, self.slotheight), width = 3)
        self.slot.create_rectangle((2*self.slotwidth/3 + 3, 3, self.slotwidth + 3, self.slotheight), width = 3)

        self.slot.create_polygon((0, self.slotheight/2 + 10,
                                  0, self.slotheight/2 - 10,
                                  15, self.slotheight/2), fill = "black")
        self.slot.create_polygon((self.slotwidth + 5, self.slotheight/2 + 10,
                                  self.slotwidth + 5, self.slotheight/2 - 10,
                                  self.slotwidth - 10, self.slotheight/2), fill = "black")

        self.numbers = []
        
        self.number = random.randint(1, 999)

        self.text.config(state = "normal")
        self.text.insert("end", "\nKotouče níže například ukazují číslo {}.".format(self.number))
        self.text.config(state = "disabled")

        self.number = "{:03d}".format(self.number)

        for i in range(-4, 6):
            self.numbers.append((self.slot.create_text((self.slotwidth/6 + 5, 13*i*self.slotheight/30 + self.slotheight/2),
                                                       text = (int(str(self.number)[0])+i) % 10, font = "helvetica 45"), 1, (int(str(self.number)[0])+i) % 10))
            self.numbers.append((self.slot.create_text((3*self.slotwidth/6 + 5, 13*i*self.slotheight/30 + self.slotheight/2),
                                                       text = (int(str(self.number)[1])+i) % 10, font = "helvetica 45"), 2, (int(str(self.number)[1])+i) % 10))
            self.numbers.append((self.slot.create_text((5*self.slotwidth/6 + 5, 13*i*self.slotheight/30 + self.slotheight/2),
                                                       text = (int(str(self.number)[2])+i) % 10, font = "helvetica 45"), 3, (int(str(self.number)[2])+i) % 10))



    

AnchoringInstructions1 = (SlotInstructions, {"text": intro1, "height": 7, "font": 20})
AnchoringInstructions2 = (InstructionsFrame, {"text": intro2, "height": 2, "font": 20, "width": 60})

      

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([AnchoringInstructions1,
         Comparison,
         AnchoringInstructions2,
         Absolute])
