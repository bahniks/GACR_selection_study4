from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import perf_counter, sleep

import random
import os
import urllib.request
import urllib.parse

from common import ExperimentFrame, InstructionsFrame, Measure, MultipleChoice
from gui import GUI
from constants import TESTING, URL


################################################################################
# TEXTS
instructions = """<b>Pokyny pro účastníky</b> 

Vítejte v druhé části dnešní studie. Pozorně si přečtěte pokyny, abyste porozuměli studii a své roli v ní. Vaše rozhodnutí budou mít finanční důsledky pro vás i pro dalšího účastníka.

Tato studie je o rozdělení peněz. Náhodně Vám bude přidělena jedna ze dvou rolí: hráč A nebo hráč B. Vaše role zůstane po celou dobu studie stejná a v obou kolech studie budete ve dvojici se stejným účastníkem. Vy i účastník ve dvojici budete vědět o rozhodnutích toho druhého.

<b>První kolo:</b> 
<i>Rozhodnutí hráče A:</i>
Hráč A obdrží 20 Kč. Má možnost vzít si od hráče B od 0 do 10 Kč. Uvede, jakou reakci čeká od hráče B.

<i>Odpověď hráče B:</i>
Hráč B obdrží 20 Kč. Bude mít k dispozici dvě možnosti reakce na rozhodnutí hráče A a bude moci poslat zprávu.
Reakce mohou být:
  - Nedělat nic: Pokračovat v interakci bez jakékoli akce.
  - Potrestat: Může hráče A potrestat od symbolické 0 až po 10 Kč. Za každou 1 Kč, kterou obětuje do potrestání, ztratí hráč A 1 Kč. 
  - Odpustit: Může hráče A odměnit od symbolické 0 až po 10 Kč. Za každou 1 Kč, kterou dá hráči A, dostane 1 Kč.

Reakce budou zaznamenány pro všechny možné volby hráče A (vezme 0-10 Kč).
Uskutečnění: Jakmile oba účastníci učiní svá rozhodnutí, budou provedena a hra postoupí do druhého kola, které je velmi podobné – liší se jen částky.

<b>Druhé kolo:</b>
<i>Rozhodnutí hráče A:</i>
Hráč A obdrží 20 Kč. Má možnost vzít si od hráče B od 0 do 20 Kč. 
Hráč B obdrží 20 Kč.
Oba hráči se dozví o volbě hráče A a tato část studie končí.
Budou následovat dotazníky na Vaše názory a postoje."""



# DictControl1 = 'Pokud hráč B rozhodne potrestat hráče A v prvním kole částkou 5 Kč, kolik peněz ztratí hráč A?' 
# DictAnswers1 = ['0 Kč', '5 Kč', '10 Kč', '15 Kč'] 
# DictFeedback1 = ['', '', '', '']
# Chybná odpověď. Za každou 1 Kč trestu, ztratí hráč A také 1 Kč.]
# b)  [Správná odpověď.]
# c)  [Chybná odpověď. Za každou 1 Kč trestu, ztratí hráč A také 1 Kč.] 
# d)  [Chybná odpověď. Za každou 1 Kč trestu, ztratí hráč A také 1 Kč.]

# DictControl2 = 'Pokud hráč B rozhodne "odpustit" a poslat hráči A 3 Kč v prvním kole, kolik peněz ztratí hráč B a kolik získá hráč A?'
# DictAnswers2 = ['Hráč B ztratí 3 Kč, hráč A získá 0 Kč.', 'Hráč B ztratí 6 Kč, hráč A získá 3 Kč.', 
# 'Hráč B ztratí 3 Kč, hráč A získá 3 Kč.', 'Hráč B ztratí 0 Kč, hráč A získá 3 Kč. '] 
# DictFeedback2 = ['', '', '', '']
# a)  [Chybná odpověď. Hráč B ztratí 3 Kč, hráč A získá 3 Kč.]
# b)  [Chybná odpověď. Hráč B ztratí 3 Kč, hráč A získá 3 Kč.] 
# c)  [Správná odpověď.]
# d) [Chybná odpověď. Hráč B ztratí 3 Kč, hráč A získá 3 Kč.]

# DictControl3 = 'Jaký je hlavní rozdíl mezi prvním a druhým kolem studie?' 
# DictAnswers3 = ['', '', '', ''] 
# DictFeedback3 = ['', '', '', '']
# a) V druhém kole bude druhý hráč jiný účastník studie. [Chybná odpověď. V obou kolech studie budete ve dvojici se stejným účastníkem.]
# b) V druhém kole je méně možností reakce pro hráče B.  [Chybná odpověď. V obou kolech studie má hráč B k dispozici dvě možnosti reakce na rozhodnutí hráče A.]
# c) V druhém kole obdrží oba hráči více peněz na začátku. [Správná odpověď. V prvním kole hráči obdrží úvodní přidělení 20 Kč, v druhém kole obdrží 40 Kč.]
# d) V druhém kole se mění role hráčů. [Chybná odpověď. Role hráčů zůstává po celou dobu studie stejná.]







DictControl1 = "Zda budete hrát v následujícím kole verzi PO úlohy závisí na kterých faktorech:"
DictAnswers1 = ["náhodně vybrané částce a částce, kterou uvedete, že jste ochotni zaplatit.",
"náhodně vybrané částce a částce, kterou jsou ochotni zaplatit ostatní účastníci výzkumu.",
"částce, kterou uvedete, že jste ochotni zaplatit, a částce, kterou jsou ochotni zaplatit ostatní účastníci výzkumu."]
DictFeedback1 = ["Ano, zda budete hrát v následujícím kole verzi PO úlohy závisí na tom, zda je částka, kterou uvedete, že jste ochotni zaplatit, vyšší než náhodně vybraná částka.", 
"Ne, zda budete hrát v následujícím kole verzi PO úlohy závisí na tom, zda je částka, kterou uvedete, že jste ochotni zaplatit, vyšší než náhodně vybraná částka.", 
"Ne, zda budete hrát v následujícím kole verzi PO úlohy závisí na tom, zda je částka, kterou uvedete, že jste ochotni zaplatit, vyšší než náhodně vybraná částka."]



wait_text = "Prosím počkejte na druhého hráče."


################################################################################


class InstructionsDictator(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = instructions, height = 33, font = 15, width = 100)

        # control question frame

        self.controlTexts = [[DictControl1, DictAnswers1, DictFeedback1]]

        self.controlFrame = Canvas(self, background = "white", highlightbackground = "white",
                                 highlightcolor = "white")
        self.filler2 = Canvas(self.controlFrame, background = "white", width = 1, height = 255,
                                highlightbackground = "white", highlightcolor = "white")
        self.filler2.grid(column = 1, row = 0, rowspan = 10, sticky = NS)
                     
        self.next.grid(row = 5, column = 1, sticky = N)
   
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 2)        

        self.controlNum = 0
        self.createQuestion()


    def createQuestion(self):
        self.next["state"] = "disabled"     
        if self.controlNum < len(self.controlTexts):            
            self.createControlQuestion()            
            self.controlFrame.grid(row = 2, column = 1)
        else:
            self.file.write("\n")
            self.controlFrame.grid_forget()
            #self.offerFrame.grid(row = 2, column = 1)

    def createControlQuestion(self):
        if self.controlNum:
            self.controlQuestion.grid_forget()
        texts = self.controlTexts[self.controlNum]
        self.controlQuestion = MultipleChoice(self.controlFrame, text = texts[0], answers = texts[1], feedback = texts[2])
        self.controlQuestion.grid(row = 0, column = 0)
        self.controlNum += 1
        self.controlstate = "answer"

  
    def write(self):
        self.file.write(self.name + "\n")
        self.file.write(self.id + "\t" + str(self.root.status["block"]) + "\n\n")

    def nextFun(self):        
        if (not self.controlQuestions) or (self.controlNum == len(self.controlTexts)):
            self.write()
            super().nextFun()   
        else:
            if self.controlstate == "answer":
                self.controlQuestion.showFeedback()
                self.controlstate = "feedback"
            else:                
                self.file.write(self.id + "\t" + str(self.controlNum) + "\t" + self.controlQuestion.answer.get() + "\n")
                self.createQuestion()




class WaitDictator(InstructionsFrame):
    def __init__(self, root, what = "pairing"):
        super().__init__(root, text = wait_text, height = 3, font = 15, proceed = False, width = 45)
        self.what = what
        self.progressBar = ttk.Progressbar(self, orient = HORIZONTAL, length = 400, mode = 'indeterminate')
        self.progressBar.grid(row = 2, column = 1, sticky = N)

    def checkUpdate(self):
        count = 0
        while True:
            self.update()
            if count % 50 == 0:
                if self.what == "pairing":
                    data = urllib.parse.urlencode({'id': self.id, 'round': "dictator", 'offer': "pairing"})
                elif self.what == "decision":
                    data = urllib.parse.urlencode({'id': self.id, 'round': "dictator", 'offer': "decision"})
                data = data.encode('ascii')
                if URL == "TEST":
                    if self.what == "pairing":
                        condition = random.choice(["forgive_ignore", "punish_ignore", "forgive_punish"])
                        role = random.choice(["A", "B"])                        
                        pair = random.randint(1,20)
                        response = str(pair) + "_" + role + "_" + condition
                    elif self.what == "decision":                                                                        
                        response = ""  # TO DO
                else:
                    try:
                        with urllib.request.urlopen(URL, data = data) as f:
                            response = f.read().decode("utf-8")       
                    except Exception as e:
                        pass
                if response:                  
                    if self.what == "pairing":
                        pair, role, condition = response.split("_")                                 
                        self.root.status["dictatorCondition"] = condition
                        self.root.status["dictatorRole"] = role
                        self.root.status["dictatorPair"] = pair                        
                        self.write(response)
                    elif self.what == "decision":   
                        pass # TO DO
                    self.progressBar.stop()
                    self.nextFun()  
                    return
            count += 1
            sleep(0.1)

    def run(self):
        self.progressBar.start()
        self.checkUpdate()

    def write(self, response):
        self.file.write("Pairing" + "\n")
        self.file.write(self.id + "\t" + response.replace("_", "\t") + "\n\n") 


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([WaitDictator,
         InstructionsDictator
         ])