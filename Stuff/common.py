from tkinter import *
from tkinter import ttk
from time import time

import os
import sys

from constants import TESTING


class ExperimentFrame(Canvas):
    def __init__(self, root):
        super().__init__(root, background = "white", highlightbackground = "white", highlightcolor = "white")
        
        self.root = root
        self.file = self.root.file
        self.id = self.root.id #os.path.basename(self.root.outputfile)

    def nextFun(self):
        if self.check():
            self.write()
            self.file.write("\n")
            self.destroy()
            self.root.nextFrame()
        else:
            self.back()

    def check(self):
        return True

    def back(self):
        pass

    def write(self):
        pass




class InstructionsFrame(ExperimentFrame):
    def __init__(self, root, text, proceed = True, firstLine = None, end = False, height = 12,
                 font = 15, space = False, width = 80, keys = None, update = None, bold = None, wait = 2):
        super().__init__(root)

        self.root = root
        self.wait = wait
        self.t0 = time()

        if update:
            updateTexts = []
            for i in update:
                updateTexts.append(self.root.texts[i])
            text = text.format(*updateTexts)       
                   
        self.text = Text(self, font = "helvetica {}".format(font), relief = "flat",
                         background = "white", width = width, height = height, wrap = "word",
                         highlightbackground = "white")
        self.text.grid(row = 1, column = 0, columnspan = 3)
        if firstLine:
            self.text.insert("1.0", text[:text.find("\n", 5)], firstLine)
            self.text.insert("end", text[text.find("\n", 5):])
            self.text.tag_configure(firstLine, font = "helvetica 20 {}".format(firstLine))
        else:
            self.text.insert("1.0", text)

        self.text.tag_configure("bold", font = "helvetica {} bold".format(font))
        i_index = "1.0"
        while True:
            i_index = self.text.search("<b>", i_index)
            if not i_index:
                break
            e_index = self.text.search("</b>", i_index)
            self.text.tag_add("bold", i_index, e_index)
            self.text.delete(e_index, e_index + "+4c")
            self.text.delete(i_index, i_index + "+3c")
            i_index = e_index
            
        self.text.config(state = "disabled")

        if proceed:
            ttk.Style().configure("TButton", font = "helvetica 15")
            self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun)
            self.next.grid(row = 2, column = 1)
        elif space:
            self.root.bind("<space>", lambda e: self.proceed())
        elif keys:
            for key in keys:
                if key in [str(i) for i in range(10)]:
                    self.root.bind("{}".format(key), lambda e: self.proceed())
                else:
                    self.root.bind("<{}>".format(key), lambda e: self.proceed())                
        else:
            self.root.bind("<g>", lambda e: self.proceed())
            self.root.bind("<G>", lambda e: self.proceed())
        self.keys = keys

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(2, weight = 3)
        self.rowconfigure(3, weight = 3)

    def changeText(self, newtext):
        self.text.config(state = "normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", newtext)
        self.text.config(state = "disabled")

    def proceed(self):
        if time() - self.t0 > self.wait:
            self.nextFun()

    def nextFun(self):
        if self.check():
            self.root.unbind("<space>")
            self.root.unbind("<g>")
            self.root.unbind("<G>")
            if self.keys:
                for key in self.keys:
                    if key in [str(i) for i in range(10)]:
                        self.root.unbind("{}".format(key))
                    else:
                        self.root.unbind("<{}>".format(key))
            self.destroy()
            self.root.nextFrame()
        else:
            self.back()



class Question(Canvas):
    def __init__(self, root, text, conditional = None, condtype = None, condtext = "", width = 80,
                 label = True, answer = "yesno", condition = "yes", where = "below"):
        super().__init__(root)
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        self.root = root

        self.yesno = answer == "yesno"
        self.condition = condition

        self.answer = StringVar()
        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 13")

        if label:
            self.label = ttk.Label(self, text = text, background = "white", font = "helvetica 15",
                                   width = width)
        else:
            self.label = Text(self, width = width, wrap = "word", font = "helvetica 15",
                              relief = "flat", height = 5, cursor = "arrow",
                              selectbackground = "white", selectforeground = "black")
            self.label.insert("1.0", text)
            self.label.config(state = "disabled")

        if answer == "yesno":
            self.yes = ttk.Radiobutton(self, text = "Ano", variable = self.answer, value = "yes",
                                       command = self.answered)
            self.no = ttk.Radiobutton(self, text = "Ne", variable = self.answer, value = "no",
                                       command = self.answered)
            self.yes.grid(column = 0, row = 1, sticky = "w", padx = 5)
            self.no.grid(column = 0, row = 2, sticky = "w", padx = 5)
        else:
            self.field = answer[0](self, textvariable = self.answer, **answer[1])
            if where == "below":
                self.field.grid(column = 0, row = 1, sticky = "w", padx = 5)
            elif where == "next":
                self.field.grid(column = 5, row = 0, sticky = "w", padx = 5)

        self.condtype = condtype
        if conditional:
            self.condvar = StringVar()
            if condtype in ("combo", "entry"):
                self.cond = conditional[0](self, textvariable = self.condvar, **conditional[1])
            else:
                self.cond = conditional[0](self, variable = self.condvar, **conditional[1])
            if condtype == "combo":
                self.cond.config(state = "readonly")
            self.cond.grid(column = 2, row = 1, sticky = "w")
            self.condtext = ttk.Label(self, text = condtext, background = "white",
                                      font = "helvetica 13")
            self.condtext.grid(column = 1, row = 1, sticky = "w", padx = 20)
            self.condtext.grid_forget()
            self.cond.grid_forget()
                        
        self.label.grid(column = 0, row = 0, columnspan = 4, sticky = "w", pady = 10)

        self.columnconfigure(3, weight = 1)


    def answered(self):
        if self.condtype:
            if self.answer.get() == self.condition:
                row = 1 if self.condition == "yes" else 2
                self.condtext.grid(column = 1, row = row, sticky = "w", padx = 20)
                self.cond.grid(column = 2, row = row, sticky = "w")
            else:
                self.condtext.grid_forget()
                self.cond.grid_forget()

    def check(self):
        return self.answer.get() and (not self.condtype or self.condvar.get()
                                      or self.answer.get() != self.condition)

    def write(self, newline = True):
        self.root.file.write(self.answer.get())
        if self.condtype and self.condvar.get():
            self.root.file.write("\t" + self.condvar.get())
        if newline:
            self.root.file.write("\n")

    def disable(self):
        if self.yesno: 
            self.yes.config(state = "disabled")
            self.no.config(state = "disabled")
        else:
            self.field.config(state = "disabled")
        if self.condtype:
            self.cond.config(state = "disabled")





class Measure(Canvas):
    def __init__(self, root, text, values, left, right, shortText = "", function = None,
                 questionPosition = "next", labelPosition = "above", middle = "",
                 funconce = False, filler = 0):
        super().__init__(root)

        self.root = root
        self.text = shortText
        self.answer = StringVar()
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 14")

        if text:        
            if questionPosition == "next":
                self.question = ttk.Label(self, text = text, background = "white", anchor = "e", font = "helvetica 14")
                self.question.grid(column = 0, row = 2, sticky = E, padx = 5)
            elif questionPosition == "above":
                self.question = ttk.Label(self, text = text, background = "white", anchor = "center",
                                          font = "helvetica 14")
                self.question.grid(column = 0, row = 0, columnspan = 4, pady = 5)

        if labelPosition != "none":
            self.left = ttk.Label(self, text = "{:>15}".format(left), background = "white",
                                  font = "helvetica 14")
            self.right = ttk.Label(self, text = "{:<15}".format(right), background = "white",
                                   font = "helvetica 14")
        if labelPosition == "above":
            self.left.grid(column = 1, row = 1, sticky = W)
            self.right.grid(column = 2, row = 1, sticky = E)
        elif labelPosition == "next":
            self.left.grid(column = 0, row = 2, sticky = E)
            self.right.grid(column = 3, row = 2, sticky = W)

        if middle:
            self.middle = ttk.Label(self, text = middle, background = "white",
                                    font = "helvetica 14")
            self.middle.grid(column = 1, row = 1, columnspan = 2)
            self.question["font"] = "helvetica 16"

        self.scale = Canvas(self, background = "white", highlightbackground = "white",
                            highlightcolor = "white")
        self.scale.grid(column = 1, row = 2, sticky = EW, columnspan = 2, padx = 40)

        self.radios = []
        for col, value in enumerate(values):
            padx = 4 if not middle else 18
            self.radios.append(ttk.Radiobutton(self.scale, text = str(value), value = value,
                                               command = self.func, variable = self.answer))
            self.radios[col].grid(row = 0, column = col, padx = padx)
            self.scale.columnconfigure(col, weight = 1)
        if filler:
            self.filler = Canvas(self.scale, background = "white", width = filler, height = 1,
                                 highlightbackground = "white", highlightcolor = "white")
            self.filler.grid(column = 0, row = 1, columnspan = len(values), sticky = EW)
            
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(3, weight = 1)

        self.function = function            
        self.functionProcessed = False
        self.funconce = funconce


    def func(self):
        if not self.funconce or not self.functionProcessed:
            if self.function:
                self.function()
                self.functionProcessed = True


    def write(self):
        if self.text:
            ans = "{}\t{}".format(self.text, self.answer.get())
        else:
            ans = self.answer.get()
        self.root.file.write(ans)



class MultipleChoice(Canvas):
    def __init__(self, root, text, answers, feedback):
        super().__init__(root, background = "white", highlightbackground = "white", highlightcolor = "white")

        self.root = root.master
        self.answer = StringVar()
        self.feedbackTexts = feedback
        
        
        self.question = ttk.Label(self, text = text, background = "white", anchor = "center",
                                          font = "helvetica 15 bold")
        self.question.grid(column = 0, row = 0, pady = 5, sticky = W)

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
        self.radios = []
        for row, answer in enumerate(answers):            
            self.radios.append(ttk.Radiobutton(self, text = answer, value = row + 1,
                                               command = self.answerFunction, variable = self.answer))
            self.radios[row].grid(row = row + 1, column = 0, pady = 3, sticky = W)

        self.filler = ttk.Label(self, text = " \n\n ", background = "white", anchor = "center",
                                          font = "helvetica 15", wraplength = 1000)
        self.filler.grid(column = 0, row = len(answers) + 1, pady = 5, sticky = NW)
        self.feedback = ttk.Label(self, text = " \n ", background = "white", anchor = "center",
                                          font = "helvetica 15", wraplength = 950)
        self.feedback.grid(column = 0, row = len(answers) + 1, pady = 5, sticky = NW)
        self.rowconfigure(len(answers) + 1, weight = 1)


    def answerFunction(self):
        self.feedback["text"] = self.feedbackTexts[int(self.answer.get()) - 1]
        for radio in self.radios:
            radio["state"] = "disabled"
        self.root.next["state"] = "normal"
        
        




def read_all(file, encoding = "utf-8"):
    text = ""
    with open(os.path.join(os.path.dirname(__file__), file), encoding = encoding) as f:
        for line in f:
            text += line.rstrip(" \t")
    return text
