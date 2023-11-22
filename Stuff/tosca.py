#! python3
from tkinter import *
from tkinter import ttk
from collections import defaultdict
from copy import deepcopy

import os
import random

from common import ExperimentFrame, InstructionsFrame
from gui import GUI

from constants import BONUS, TESTING
from quest import Likert


################################################################################
# TEXTS
questintro = """Níže jsou uvedeny situace, které lidé často zažívají v běžném životě, následované typickými reakcemi na tyto situace. Při čtení každé situace se zkuste vcítit do dané situace. Poté uveďte, jak pravděpodobně byste v dané situaci reagovali popsaným způsobem."""

################################################################################



class QuestionFrame(Canvas):
    def __init__(self, root):
        super().__init__(root, background = "white", highlightbackground = "white", highlightcolor = "white")
        self.root = root
        self.file = self.root.file
        self.id = self.root.id

    def check(self):
        self.root.check()


class TOSCA(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.left = "málo pravděpodobné"
        self.right = "velmi pravděpodobné"
        self.options = 5

        self.file.write("TOSCA\n")

        self.instructions = Text(self, height = 6, relief = "flat", width = 80,
                                    font = "helvetica 15", wrap = "word")
        self.instructions.grid(row = 1, column = 0, columnspan = 3)
        self.instructions.insert("1.0", questintro)
        
        self.instructions.tag_config("text", justify = "center") 
        self.instructions["state"] = "disabled"

        self.questions = []
        with open(os.path.join("Stuff", "tosca.txt"), encoding = "utf-8") as f:
            for line in f:
                self.questions.append(line.strip())

        self.questFrame = QuestionFrame(self)
        self.questFrame.grid(row = 2, column = 0, columnspan = 3, sticky = NSEW)
        self.questFrame.rowconfigure(0, weight = 1)
        self.questFrame.rowconfigure(1, weight = 1)
        self.questFrame.rowconfigure(2, weight = 1)
        self.questFrame.columnconfigure(0, weight = 1)
        self.questFrame.columnconfigure(2, weight = 1)

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun, state = "disabled")
        self.next.grid(row = 3, column = 1)

        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 2)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

        self.mnumber = 0
        
        self.createQuestions()


    def createQuestions(self):
        self.situation = ttk.Label(self.questFrame, text = self.questions[self.mnumber*3], background = "white", font = "helvetica 15")        
        self.first = Likert(self.questFrame, self.questions[self.mnumber*3 + 1], shortText = str(self.mnumber + 1) + "a",
                       left = self.left, right = self.right, options = self.options)
        self.second = Likert(self.questFrame, self.questions[self.mnumber*3 + 2], shortText = str(self.mnumber + 1) + "b",
                       left = self.left, right = self.right, options = self.options)
        
        self.situation.grid(column = 1, row = 0)        
        self.first.grid(column = 1, row = 1)
        self.second.grid(column = 1, row = 2)
            
        self.mnumber += 1
        

    def nextFun(self):
        self.first.write()
        self.second.write()
        self.situation.grid_forget()
        self.first.grid_forget()
        self.second.grid_forget()
        if self.mnumber == len(self.questions)//3:
            self.file.write("\n")            
            self.destroy()
            self.root.nextFrame()
        else:
            self.next["state"] = "disabled"
            self.createQuestions()


    def check(self):
        if self.first.answer.get() and self.second.answer.get():                
            self.next["state"] = "!disabled"





if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([TOSCA])
