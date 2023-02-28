from tkinter import *
from tkinter import ttk
from collections import deque
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame, Question, Measure, read_all
from gui import GUI



darktriadintro = """
Níže uvedená tvrzení popisují postoje, vnímání a chování v různých situacích.
Ohodnoťte je dle toho, jak s nimi souhlasíte nebo nesouhlasíte pomocí uvedené stupnice.
"""






class Questionnaire(ExperimentFrame):
    def __init__(self, root, words, question = "", labels = None, blocksize = 4, values = 7, text = True,
                 filetext = "", fontsize = 13, labelwidth = None):
        super().__init__(root)
        if filetext:
            self.file.write(filetext + "\n")

        if type(words) == str and os.path.exists(os.path.join(os.path.dirname(__file__), words)):
            self.words = read_all(os.path.join(os.path.dirname(__file__), words)).split("\n")
        else:
            self.words = words

        self.buttons = {}
        self.variables = {}
        self.labels = {}

        self.frame = Canvas(self)
        self.frame.grid(column = 1, row = 1, sticky = NSEW)
        self.frame["highlightbackground"] = "white"
        self.frame["background"] = "white"
        self.frame["highlightcolor"] = "white"

        maxwidth = max(map(len, self.words))

        for count, word in enumerate(self.words, 1):
            self.variables[word] = StringVar()
            for i in range(1, values+1):
                if word not in self.buttons:
                    self.buttons[word] = {}
                valuetext = str(i) if text else ""
                self.buttons[word][i] = ttk.Radiobutton(self.frame, text = valuetext, value = i,
                                                        command = self.clicked,
                                                        variable = self.variables[word])
                self.buttons[word][i].grid(column = i, row = count + (count-1)//blocksize, padx = 15)
            self.labels[word] = ttk.Label(self.frame, text = word, background = "white",
                                          font = "helvetica {}".format(fontsize+1), justify = "left",
                                          width = maxwidth/1.2)
            self.labels[word].grid(column = 0, row = count + (count-1)//blocksize, padx = 15,
                                   sticky = W)
            if not count % blocksize:
                self.frame.rowconfigure(count + count//blocksize, weight = 1)

        ttk.Label(self.frame, text = "s"*int(maxwidth/1.05), background = "white", font = "helvetica {}".format(fontsize+1),
                  foreground = "white", justify = "left", width = maxwidth/1.2).grid(
                      column = 0, padx = 15, sticky = W, row = count + 1 + (count-1)//blocksize)

        self.texts = []
        if not labels:
            labels = [""]*values
        elif len(labels) != values:
            labels = [labels[0]] + [""]*(values - 2) + [labels[-1]]

        for count, label in enumerate(labels):
            self.texts.append(ttk.Label(self.frame, text = labels[count], background = "white",
                                        font = "helvetica {}".format(fontsize), anchor = "center",
                                        justify = "center"))
            if labelwidth:
                self.texts[count]["width"] = labelwidth,
            self.texts[count].grid(column = count+1, row = 0, sticky = W, pady = 4, padx = 3)

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 14")

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun,
                               state = "disabled")
        self.next.grid(column = 1, row = 2)

        self.question = ttk.Label(self, text = question, background = "white",
                                  font = "helvetica 15")
        self.question.grid(column = 1, row = 0, sticky = S, pady = 10)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 2)
        self.rowconfigure(3, weight = 1)


    def clicked(self):
        end = True
        for word in self.words:
            if not self.variables[word].get():
                end = False
            else:
                self.labels[word]["font"] = "helvetica 10"
        if end:
            self.next["state"] = "!disabled"

    def write(self):
        for word in self.words:
            self.file.write(self.id + "\t" + word + "\t" + self.variables[word].get() + "\n")



DarkTriad1 = (Questionnaire,
             {"words": "darktriad1.txt",
              "question": darktriadintro,
              "labels": ["Zcela\nnesouhlasím",
                         "Částečně\nnesouhlasím",
                         "Něco\nmezi",
                         "Částečně\nsouhlasím",
                         "Zcela\nsouhlasím"],
              "values": 5,
              "labelwidth": 12,
              "text": False,
              "fontsize": 13,
              "blocksize": 3,
              "filetext": "Dark Triad"})
DarkTriad2 = (Questionnaire,
             {"words": "darktriad2.txt",
              "question": darktriadintro,
              "labels": ["Zcela\nnesouhlasím",
                         "Částečně\nnesouhlasím",
                         "Něco\nmezi",
                         "Částečně\nsouhlasím",
                         "Zcela\nsouhlasím"],
              "values": 5,
              "labelwidth": 12,
              "text": False,
              "fontsize": 13,
              "blocksize": 3,
              "filetext": "Dark Triad"})





if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([DarkTriad1,
         DarkTriad2])
