#! python3
# -*- coding: utf-8 -*- 

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import perf_counter, sleep
from collections import defaultdict
from math import ceil

import random
import os
import urllib.request
import urllib.parse

from common import InstructionsFrame
from gui import GUI
from constants import TESTING, URL, PARTICIPATION_FEE, PREDICTION_BONUS, COEFFICIENTS




class Login(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = "Počkejte na spuštění experimentu", height = 3, font = 15, width = 45, proceed = False)

        self.progressBar = ttk.Progressbar(self, orient = HORIZONTAL, length = 400, mode = 'indeterminate')
        self.progressBar.grid(row = 2, column = 1, sticky = N)

    def login(self):        
        count = 0
        while True:
            self.update()
            if count % 50 == 0:            
                data = urllib.parse.urlencode({'id': self.root.id, 'round': 0, 'offer': "login"})
                data = data.encode('ascii')                  
                if URL == "TEST":
                    condition = random.choice(["low", "control", "high"])
                    information = random.choice(["yes", "no"])                   
                    winning_block = str(random.randint(1,5))                                       
                    response = "_".join(["start", condition, information, winning_block])
                    self.root.status["otherWin1"] = random.randint(1, 5)
                    self.root.status["otherWin2"] = random.randint(1, 5)
                else:
                    response = ""
                    try:
                        with urllib.request.urlopen(URL, data = data) as f:
                            response = f.read().decode("utf-8") 
                    except Exception:
                        self.changeText("Server nedostupný")
                if "start" in response:
                    info, condition, information, winning_block = response.split("_")              
                    self.root.status["condition"] = condition        
                    self.root.status["information"] = information
                    self.root.texts["block"] = self.root.status["winning_block"] = winning_block
                    self.root.status["coefficient"] = {"low": COEFFICIENTS[0], "high": COEFFICIENTS[2], "control": COEFFICIENTS[1]}[condition]                     
                    #self.create_control_question(condition) # todo
                    self.progressBar.stop()
                    self.write(response)
                    self.nextFun()                      
                    break
                elif response == "login_successful" or response == "already_logged":
                    self.changeText("Přihlášen")
                    self.root.status["logged"] = True
                elif response == "ongoing":
                    self.changeText("Do studie se již nelze připojit")
                elif response == "no_open":
                    self.changeText("Studie není otevřena")
                elif response == "closed":
                    self.changeText("Studie je uzavřena pro přihlašování")
                elif response == "not_grouped":
                    self.changeText("Nebyla Vám přiřazena žádná skupina. Zavolejte prosím experimentátora zvednutím ruky.")
            count += 1                  
            sleep(0.1)        

    def run(self):
        self.progressBar.start()
        self.login()



    # def create_control_question(self, source, condition):        
    #     condition = source + "_" + condition
    #     global answers3
    #     correctAnswer = correct_answers3[condition]
    #     answers3 += [correctAnswer]
    #     global feedback3
    #     if condition == "experimenter_divided":
    #         correctAnswer.replace("Sečte se", "se sečte")
    #     else:
    #         correctAnswer = correctAnswer[:1].lower() + correctAnswer[1:]
    #     for i in range(4):
    #         feedback3[i] += correctAnswer

    def write(self, response):
        self.file.write("Login" + "\n")
        self.file.write(self.id + response.replace("_", "\t").lstrip("start") + "\n\n")

    def gothrough(self):
        self.run()