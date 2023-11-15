from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import perf_counter, sleep

import random
import os
import urllib.request
import urllib.parse

from common import ExperimentFrame, InstructionsFrame, Measure, MultipleChoice, InstructionsAndUnderstanding
from gui import GUI
from constants import TESTING, URL


################################################################################
# TEXTS
instructions = """Vítejte v druhé části dnešní studie. Pozorně si přečtěte pokyny, abyste porozuměli studii a své roli v ní. Vaše rozhodnutí budou mít finanční důsledky pro vás a pro dalšího účastníka.

Tato studie je o rozdělení peněz. Náhodně Vám bude přidělena jedna ze dvou rolí: hráč A, nebo hráč B. Vaše role zůstane po celou dobu studie stejná a v obou kolech studie budete ve dvojici se stejným účastníkem. Vy i účastník ve dvojici budete vědět o rozhodnutích toho druhého.

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
Budou následovat dotazníky na Vaše názory a postoje.

Níže uvádíme několik otázek, které ověřují, zda studii rozumíte."""


DictControl1 = "Jaká je role hráče A a hráče B ve studii?"
DictAnswers1 = ["Hráč A rozhoduje, kolik hráči B vezme peněz. Účastníci studie jsou v obou kolech buď hráčem A nebo hráčem B (role se nemění).",
"Hráč A rozhoduje, kolik hráči B vezme peněz. Účastníci studie jsou nejprve hráčem A v druhém kole hráčem B (role se vymění).", "Hráč B rozhoduje, kolik hráči A vezme peněz. Účastníci studie jsou v obou kolech buď hráčem A nebo hráčem B (role se nemění).", "Hráč B rozhoduje, kolik hráči A vezme peněz. Účastníci studie jsou nejprve hráčem A v druhém kole hráčem B (role se vymění)."]
DictFeedback1 = ["Správná odpověď.", "Chybná odpověď. Účastníci studie jsou v obou kolech buď hráčem A nebo hráčem B (role se nemění).", "Chybná odpověď. Hráč A rozhoduje, kolik hráči B vezme peněz.", "Chybná odpověď. Hráč A rozhoduje, kolik hráči B vezme peněz. Účastníci studie jsou v obou kolech buď hráčem A nebo hráčem B (role se nemění)."]

DictControl2 = "Jaký je rozdíl mezi prvním a druhým kolem studie?"
DictAnswers2 = ["V druhém kole bude druhým hráčem jiný účastník studie.", "V druhém kole hráč B nemá možnost reakce.", "V druhém kole obdrží oba hráči více peněz na začátku.", "V druhém kole se mění role hráčů."]
DictFeedback2 = ["Chybná odpověď. V obou kolech studie budete ve dvojici se stejným účastníkem.", "Správná odpověď. V druhém kole hráč B pouze vyčkává rozhodnutí hráče A.", "Chybná odpověď. V obou kolech hráči obdrží úvodní přidělení 20 Kč.", "Níže přiřadit dle toho, jakou verzi mají randomizovanou."]

DictControl3 = 'Pokud hráč B rozhodne “potrestat” hráče A v prvním kole částkou 5 Kč, kolik peněz ztratí hráč A?'
DictAnswers3 = ["0 Kč ", "5 Kč", "10 Kč", "15 Kč"]
DictFeedback3 = ["Chybná odpověď. Za každou 1 Kč trestu, ztratí hráč A také 1 Kč.", "Správná odpověď.", "Chybná odpověď. Za každou 1 Kč trestu, ztratí hráč A také 1 Kč.", "Chybná odpověď. Za každou 1 Kč trestu, ztratí hráč A také 1 Kč."]

DictControl4 = 'Pokud hráč B rozhodne "odpustit" a poslat hráči A 3 Kč v prvním kole, kolik peněz ztratí hráč B a kolik získá hráč A?'
DictAnswers4 = ["Hráč B ztratí 3 Kč, hráč A získá 0 Kč.", "Hráč B ztratí 6 Kč, hráč A získá 3 Kč.", "Hráč B ztratí 3 Kč, hráč A získá 3 Kč.", "Hráč B ztratí 0 Kč, hráč A získá 3 Kč."]
DictFeedback4 = ["Chybná odpověď. Hráč B ztratí 3 Kč, hráč A získá 3 Kč.", "Chybná odpověď. Hráč B ztratí 3 Kč, hráč A získá 3 Kč.", "Správná odpověď.", "Chybná odpověď. Hráč B ztratí 3 Kč, hráč A získá 3 Kč."]

DictControl5 = "Pokud hráč B rozhodne “nedělat nic” v prvním kole, jaké jsou peněžní důsledky pro hráče A?" 
DictAnswers5 = ["Získá navíc 20 Kč a obdrží textovou zprávu.", "Žádné. Obdrží jen textovou zprávu.", "Získá navíc 1 Kč a obdrží textovou zprávu.", "Ztratí 20 Kč a obdrží textovou zprávu."]
DictFeedback5 = ["Chybná odpověď. Hráč A v prvním kole žádné další peníze nezíská, ani neztratí.\nObdrží jen textovou zprávu.", "Správná odpověď.", "Chybná odpověď. Hráč A v prvním kole žádné další peníze nezíská, ani neztratí.\nObdrží jen textovou zprávu.", "Chybná odpověď. Hráč A v prvním kole žádné další peníze nezíská, ani neztratí.\nObdrží jen textovou zprávu."]


wait_text = "Prosím počkejte na druhého hráče."



A1text = """Byla vám náhodně přidělena role: <b>Hráč A</b> 
Vaše role zůstává po celou dobu experimentu stejná.

Vy i hráč B jste dostali v této části studie 20 Kč.
S hráčem B budete ve dvojici pro obě kola, po které se studie koná. Oba budete znát rozhodnutí toho druhého.

Nyní budete mít příležitost se rozhodnout, kolik (0-10 Kč) si od hráče B vezmete.
Hráč B bude reagovat. Bude mít k dispozici dvě možnosti reakce na rozhodnutí hráče A a bude moci poslat textovou zprávu:
{}

<b>Rozhodněte se, kolik si chcete od hráče B vzít (0-10 Kč)</b>:
"""

ignoreText = "\n<b>Nedělat nic</b>: Pokračovat v interakci bez jakékoli akce."
punishText = "\n<b>Potrestat</b>: Může hráče A potrestat od symbolické 0 až po 10 Kč. Za každou 1 Kč, kterou obětuje do potrestání, ztratí hráč A 1 Kč."
forgiveText = "\n<b>Odpustit</b>: Může hráče A odměnit od symbolické 0 až po 10 Kč. Za každou 1 Kč, kterou dá, hráč A dostane 1 Kč." 




B1text = """Byla vám náhodně přidělena role: <b>Hráč B</b> 
Vaše role zůstává po celou dobu experimentu stejná.

Vy i hráč A jste dostali v této části studie 20 Kč.
S hráčem A budete ve dvojici pro obě kola, po které se studie koná. Oba budete znát rozhodnutí toho druhého.

Hráč A Vám může vzít 0 až 10 Kč, níže uveďte, jak budete reagovat. Máte na výběr z těchto dvou možností:
{}

<b>Níže uveďte v Kč Vaše reakci na možná rozhodnutí hráče A:</b>"""

ignoreResponse = '''<b>Nedělat nic</b>: Pokračovat v interakci bez jakékoli akce a poslat jednu ze zpráv.'''
punishResponse = '''<b>Potrestat</b>: Můžete hráče A potrestat od symbolické 0 až po 10 Kč. Za každou 1 Kč, kterou obětujete do potrestání, ztratí hráč A 1 Kč. Navíc pošlete jednu ze zpráv.'''
forgiveResponse = '''<b>Odpustit</b>: Můžete hráče A odměnit od symbolické 0 až po 10 Kč. Za každou 1 Kč, kterou dáte, hráč A dostane 1 Kč. Navíc pošlete jednu ze zpráv.'''

ignoreMessage1 = "V reakci na Vaše rozhodnutí neudělám nic a pokračuji v naší interakci."
ignoreMessage2 = "Volím možnost: Nedělat nic."
punishMessage1 = "V reakci na Vaše rozhodnutí Vás tímto trestám."
punishMessage2 = "Volím možnost: Potrestat."
forgiveMessage1 = "Je mi líto, že jste mi vzal peníze. Takto by se k sobě lidé chovat neměli. Já Vám ale odpouštím."
forgiveMessage2 = "Volím možnost: Odpustit."

################################################################################



class ScaleFrame(Canvas):
    def __init__(self, root):
        super().__init__(root, background = "white", highlightbackground = "white", highlightcolor = "white")

        self.root = root.root

        self.valueVar = StringVar()
        self.valueVar.set("0")

        ttk.Style().configure("TScale", background = "white")

        self.value = ttk.Scale(self, orient = HORIZONTAL, from_ = 0, to = 10, length = 500,
                            variable = self.valueVar, command = self.changedValue)

        if self.root.status["dictatorRole"] == "A":
            action = "Beru"
        else:
            action = "Beru" # TO DO
        self.actionLab = ttk.Label(self, text = action, font = "helvetica 15", background = "white", anchor = "w")
        self.valueLab = ttk.Label(self, textvariable = self.valueVar, font = "helvetica 15", background = "white", width = 3, anchor = "e")
        self.currencyLab = ttk.Label(self, text = "Kč", font = "helvetica 15", background = "white")

        self.value.grid(column = 1, row = 1, padx = 15)
        self.actionLab.grid(column = 2, row = 1)
        self.valueLab.grid(column = 3, row = 1)
        self.currencyLab.grid(column = 4, row = 1)


    def changedValue(self, value):                
        self.valueVar.set(str(int(round(eval(self.valueVar.get()), 0))))
        

class ResponseFrame(Canvas):
    def __init__(self, root, value):
        super().__init__(root, background = "white", highlightbackground = "white", highlightcolor = "white")
        self.root = root.root

        conditions = {"ignore": ["Neudělám nic", ignoreMessage1, ignoreMessage2], 
                      "punish": ["Potrestám", punishMessage1, punishMessage2],
                      "forgive": ["Odpustím", forgiveMessage1, forgiveMessage2]}
        self.conditions = conditions

        c1, c2 = self.root.status["dictatorCondition"].split("-")

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 14")

        self.valueLab = ttk.Label(self, text = "Hráč A vezme " + str(value) + " Kč:  ", font = "helvetica 14", background = "white", anchor = "e")

        self.responseVar = StringVar()
        self.responseBut1 = ttk.Radiobutton(self, text = conditions[c1][0], value = c1, command = self.response, variable = self.responseVar)
        self.responseBut2 = ttk.Radiobutton(self, text = conditions[c2][0], value = c2, command = self.response, variable = self.responseVar)

        self.valueLab.grid(column = 0, row = 1)
        self.responseBut1.grid(column = 1, row = 1, sticky = W)
        self.responseBut2.grid(column = 1, row = 2, sticky = W)

        self.columnconfigure(0, weight = 2)
        self.columnconfigure(3, weight = 2)

    def response(self):
        c1, c2 = self.root.status["dictatorCondition"].split("-")

        self.messageVar = StringVar()        
        self.messageBut1 = ttk.Radiobutton(self, text = self.conditions[c1][1], value = "1", command = self.message, variable = self.messageVar)
        self.messageBut2 = ttk.Radiobutton(self, text = self.conditions[c2][2], value = "2", command = self.message, variable = self.messageVar)

        self.messageBut1.grid(column = 2, row = 1, sticky = W)
        self.messageBut2.grid(column = 2, row = 2, sticky = W)

    def message(self):
        pass


class DictatorDecision(InstructionsFrame):
    def __init__(self, root, round = 1):
        if root.status["dictatorRole"] == "A":
            text = A1text
            text = text.format({"forgive-ignore": forgiveText + "\n" + ignoreText, 
                                "punish-ignore": punishText + "\n" + ignoreText, 
                                "forgive-punish": forgiveText + "\n" + punishText}[root.status["dictatorCondition"]])
            height = 19
            width = 80
        else:
            text = B1text
            text = text.format({"forgive-ignore": forgiveResponse + "\n" + ignoreResponse, 
                    "punish-ignore": punishResponse + "\n" + ignoreResponse, 
                    "forgive-punish": forgiveResponse + "\n" + punishResponse}[root.status["dictatorCondition"]])
            height = 13
            width = 100

        super().__init__(root, text = text, height = height, font = 15, width = width)

        if self.root.status["dictatorRole"] == "A":
            self.scaleFrame = ScaleFrame(self)       
            self.scaleFrame.grid(column = 1, row = 3, pady = 10)        
            self.next.grid(column = 1, row = 4)
            self.rowconfigure(4, weight = 1)
        else:
            frames = {}
            for i in range(11):
                frames[i] = ResponseFrame(self, i)
                frames[i].grid(column = 0, row = 3 + i, pady = 3)
            self.next.grid(column = 1, row = 15)          
            self.rowconfigure(15, weight = 1)
      
       
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 0)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 0)
        self.rowconfigure(16, weight = 2)




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
                        condition = random.choice(["forgive-ignore", "punish-ignore", "forgive-punish"])
                        role = "B"
                        #role = random.choice(["A", "B"])                        
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





controlTexts1 = [[DictControl1, DictAnswers1, DictFeedback1], [DictControl2, DictAnswers2, DictFeedback2], [DictControl3, DictAnswers3, DictFeedback3], [DictControl4, DictAnswers4, DictFeedback4], [DictControl5, DictAnswers5, DictFeedback5]]
InstructionsDictator = (InstructionsAndUnderstanding, {"text": instructions, "height": 31, "width": 110, "randomize": False, "controlTexts": controlTexts1})


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([WaitDictator,
         DictatorDecision,
         InstructionsDictator
         ])