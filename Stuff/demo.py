#! python3
from tkinter import *
from tkinter import ttk

import os

from math import ceil

from common import ExperimentFrame
from gui import GUI
from constants import BONUS


class Demographics(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)
       
        self.sex = StringVar()
        self.language = StringVar()
        self.age = StringVar()
        self.student = StringVar()
        self.field = StringVar()
        self.field.set("Nestuduju VŠ")

        self.lab1 = ttk.Label(self, text = "Pohlaví:", background = "white",
                              font = "helvetica 15")
        self.lab1.grid(column = 1, row = 1, pady = 2, sticky = W, padx = 2)
        self.lab2 = ttk.Label(self, text = "Věk:", background = "white",
                              font = "helvetica 15")
        self.lab2.grid(column = 1, row = 2, pady = 2, sticky = W, padx = 2)        
        self.lab3 = ttk.Label(self, text = "Mateřský jazyk:  ", background = "white",
                              font = "helvetica 15")
        self.lab3.grid(column = 1, row = 3, pady = 2, sticky = W, padx = 2)
        self.lab5 = ttk.Label(self, text = "Studujete VŠ?  ", background = "white",
                              font = "helvetica 15")
        self.lab5.grid(column = 1, row = 5, pady = 2, sticky = W, padx = 2)
        self.lab6 = ttk.Label(self, text = "Pokud ano, jaký obor? ", background = "white",
                              font = "helvetica 15")
        self.lab6.grid(column = 1, row = 6, pady = 2, sticky = W, padx = 2)
        
        self.male = ttk.Radiobutton(self, text = "muž", variable = self.sex, value = "male",
                                    command = self.checkAllFilled)
        self.female = ttk.Radiobutton(self, text = "žena", variable = self.sex,
                                      value = "female", command = self.checkAllFilled)

        self.czech = ttk.Radiobutton(self, text = "český", variable = self.language,
                                     value = "czech", command = self.checkAllFilled)
        self.slovak = ttk.Radiobutton(self, text = "slovenský", variable = self.language,
                                     value = "slovak", command = self.checkAllFilled)
        self.other = ttk.Radiobutton(self, text = "jiný", variable = self.language,
                                     value = "other", command = self.checkAllFilled)

        self.yes = ttk.Radiobutton(self, text = "ano", variable = self.student,
                                     value = "student", command = self.checkAllFilled)
        self.no = ttk.Radiobutton(self, text = "ne", variable = self.student,
                                    value = "nostudent", command = self.checkAllFilled)

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
        ttk.Style().configure("TButton", font = "helvetica 15")

        self.ageCB = ttk.Combobox(self, textvariable = self.age, width = 6, font = "helvetica 14",
                                  state = "readonly")
        self.ageCB["values"] = tuple([""] + [str(i) for i in range(18, 80)])
        self.ageCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())

        self.fieldCB = ttk.Combobox(self, textvariable = self.field, width = 15,
                                    font = "helvetica 14", state = "readonly")
        self.fieldCB["values"] = ["Nestuduji VŠ",
                                  "Ekonomie / management",
                                  "Jazyky / mezinárodní studia",
                                  "Kultura / umění",
                                  "Medicína / farmacie",
                                  "Právo / veřejná správa",
                                  "Přírodní vědy",
                                  "Technika / informatika",
                                  "Učitelství / sport",
                                  "Zemědělství / veterina",
                                  "Humanitní / společenské vědy",
                                  "Jiné"]
        self.fieldCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())

        self.male.grid(column = 2, row = 1, pady = 7, padx = 7, sticky = W)
        self.female.grid(column = 3, row = 1, pady = 7, padx = 7, sticky = W)
        self.czech.grid(column = 2, row = 3, pady = 7, padx = 7, sticky = W)
        self.slovak.grid(column = 3, row = 3, pady = 7, padx = 7, sticky = W)
        self.other.grid(column = 4, row = 3, pady = 7, padx = 45, sticky = W)
        self.ageCB.grid(column = 2, row = 2, pady = 7, padx = 7, sticky = W)
        self.yes.grid(column = 2, row = 5, pady = 7, padx = 7, sticky = W)
        self.no.grid(column = 3, row = 5, pady = 7, padx = 7, sticky = W)
        self.fieldCB.grid(column = 2, columnspan = 2, row = 6, pady = 7, padx = 7, sticky = W)

        self.columnconfigure(5, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(8, weight = 1)

        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = 7, column = 2, pady = 15)


    def checkAllFilled(self, _ = None):
        if all([v.get() for v in [self.language, self.age, self.sex,
                                  self.field, self.student]]):
            self.next["state"] = "!disabled"


    # def writeWinnings(self):
    #     options = os.path.join(os.path.dirname(os.path.dirname(__file__)), "options.txt")
    #     if os.path.exists(options):
    #         with open(options, mode = "r") as f:
    #             directory = f.readline().strip()
    #             station = f.readline().strip()
    #         if not os.path.exists(directory):
    #             directory = os.path.dirname(self.root.outputfile)
    #     else:
    #         directory = os.path.dirname(self.root.outputfile)
    #         station = "UNKNOWN"
    #     self.root.texts["station"] = station
    #     filename = os.path.splitext(os.path.basename(self.root.outputfile))[0]
    #     output = os.path.join(directory, filename + "_STATION_" + str(station) + ".txt")
    #     if all([key in self.root.texts for key in ["dice", "lottery_win", "attention_checks"]]):
    #         if self.root.texts["attention_checks"] > 0:
    #             self.root.texts["attention1"] = "Neodpověděli"
    #             self.root.texts["attention2"] = "nevydělali"
    #         else:
    #             self.root.texts["attention1"] = "Odpověděli"
    #             self.root.texts["attention2"] = "vydělali"
    #         self.root.texts["bonus"] = BONUS
    #         dice = self.root.texts["dice"]
    #         lottery = self.root.texts["lottery_win"]
    #         bonus = 0 if self.root.texts["attention_checks"] else BONUS
    #         with open(output, mode = "w", encoding = "utf-8") as infile:
    #             reward = dice + lottery + bonus + 50
    #             self.root.texts["reward"] = reward
    #             reward = int(ceil(reward/10)*10)
    #             self.root.texts["rounded_reward"] = reward
    #             infile.write("reward: " + str(reward) + "Kč\n\n")
    #         self.file.write("Winnings\n")
    #         self.file.write(self.id + "\t" + str(reward) + "\n")


    def write(self):
        self.file.write("Demographics\n")
        self.file.write("\t".join([self.id, self.sex.get(), self.age.get(), self.language.get(),
                                   self.student.get(), self.field.get()]) + "\n\n")
        # self.writeWinnings()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Demographics])
