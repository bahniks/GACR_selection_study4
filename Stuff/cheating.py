#! python3
from tkinter import *
from tkinter import ttk
from time import perf_counter, sleep
from collections import defaultdict

import random
import os

from common import ExperimentFrame, InstructionsFrame, Measure
from gui import GUI
from debriefcheating import DebriefCheating
from constants import MAX_BDM_PRIZE


################################################################################
# TEXTS

continuetext = "Pokračovat"
oddtext = "Liché (1, 3 nebo 5)"
eventext = "Sudé (2, 4 nebo 6)"
rolltext = "Hodit kostkou"
correcttext = "Správně"
incorrecttext = "Špatně"    
predictiontext = "Zvolil/a jsem si, jestli na kostce padne liché, nebo sudé číslo"

treatmenttext = '''Kolo {}

Máte za úkol uhodnout, zda na kostce padne liché, nebo sudé číslo. Nyní prosím zvolte, zda v následujícím hodě padne liché, nebo sudé číslo, zapamatujte si svoji volbu a poté klikněte na tlačítko Hodit kostkou.
'''

treatmenttext2 = "Zvolte, zda jste hádali správně a vydělali v tomto kole {} Kč, nebo zda jste hádali špatně a nevydělali jste v tomto kole nic."

controltext = """Kolo {}

Máte za úkol uhodnout, zda na kostce padne liché, nebo sudé číslo. Nyní prosím zvolte, zda v následujícím hodě padne liché, nebo sudé číslo, a poté klikněte na tlačítko Hodit kostkou.
"""

controltext2 = "V tomto kole byla vaše předpověď {}"
wintext = "správná a vydělali jste {} Kč."
losstext = "špatná a nevydělali jste možných {} Kč."


# buttons
controlchoicetext = "verze PŘED"
treatmentchoicetext = "verze PO"  

intro_BDM = """
Toto je konec {{}} bloku o dvanácti kolech. Pokud bude tento blok vylosován, obdržíte {{}} Kč.

Jak jste zaznamenali, úkol měl dvě verze:

<b>Verzi “PŘED”</b>, ve které činíte předpovědi před hodem kostkou. Po zvolení možnosti vidíte výsledek hodu a dozvíte se, zda jste uhodli či nikoliv, a kolik jste vydělali.
<b>Verzi “PO”</b>, ve které uvádíte, zda jste uhodli či nikoliv a kolik jste vydělali, až poté, co vidíte výsledek hodu kostkou.

Nyní vás čeká {{}} blok s dvanácti pokusy. Pro tento blok máte možnost zvolit si jednu z uvedených verzí. <b>Volba verze “PO” je ale zpoplatněna.</b> Zvolíte-li tuto verzi, bude částka zaplacená částka odečtena od výdělku v tomto bloku. Můžete si tedy zvolit jednu z následujících možností:
- verze PO se zpoplatněním
- verze PŘED bez poplatku.

V následujícím kole budete hrát jednu z verzí úlohy.
Za verzi "PO" je nutné zaplatit poplatek, který bude náhodně určen z intervalu od 1 do {} Kč.
Do textového pole níže uveďte, kolik jste ochotni za hraní verze "PO" zaplatit.
Pokud tato částka bude vyšší nebo rovná náhodně vybranému poplatek, poplatek zaplatíte a budete hrát verzi "PO".
Pokud vámi uvedená částka bude nižší než náhodně vybraný poplatek, poplatek platit nebudete a budete hrát verzi "PŘED".
Nikdy nebudete platit více než, kolik je náhodně vybraný poplatek. I pokud uvedete, že jste ochotni zaplatit více, zaplatíte pouze výši poplatku. Je tedy pro vás rozumné uvést maximální cenu, co jste ochotni zaplatit.
Pokud uvedete hodnotu 0, budete určitě hrát verzi "PŘED". Pokud uvedete hodnotu {}, budete určitě hrát verzi "PO".
""".format("", "", "", MAX_BDM_PRIZE, MAX_BDM_PRIZE)


intro_auction = """
Před následujícím kolem byli všichni účastníci studie rozděleni do skupin o čtyřech lidech. Z každé skupiny bude v následujícím kole jeden hrát verzi "PO" a zbývající účastníci budou hrát verzi "PŘED".
Kdo z každé skupiny bude hrát verzi "PO" bude rozhodnuto na základě aukce. Všichni členové skupiny uvedou nabídku, kolik Kč jsou ochotni zaplatit ze své výhry za to, aby hráli verzi "PO". Ten, který uvede nejvyšší částku bude hrát verzi "PO" a za tuto možnost zaplatí částku rovnou druhé nejvyšší nabídce ve skupině.
Ostatní členové skupiny budou hrát verzi "PŘED".
Nyní uveďte svou nabídku, kolik jste ochotní zaplatit za možnost hrát verzi "PO" úlohy.
"""

wait_text = "Prosím počkejte než se rozhodnou ostatní členové týmu."




intro_block_1 = """
V následujícím úkolu budete hádat, jestli na virtuální kostce (generátor náhodných čísel) na vašem počítači padne liché, nebo sudé číslo. Každé z čísel 1, 2, 3, 4, 5 a 6 může padnout se stejnou pravděpodobností. Lichá čísla jsou 1, 3 a 5. Sudá čísla jsou 2, 4 a 6. 

Úkol je rozdělen do šesti samostatných bloků a každý blok sestává z dvanácti kol. V každém kole budete hádat výsledek jednoho hodu kostkou. Bloky se odlišují pravidly, dle nichž budete hádat hody kostkou. Po každém bloku bude krátká přestávka.

Uhodnete-li první hod v daném bloku, získáte 5 Kč, uhodnete-li další, získáte za něj dalších 10 Kč, uhodnete-li další hod, získáte za něj dalších 15 Kč a tak dále. Za každý další uhodnutý hod získáte navíc částku o 5 Kč vyšší, než byla předchozí odměna. Pokud tedy uhodnete všech 12 hodů v daném bloku, za poslední dvanáctý uhodnutý hod získáte 60 Kč a celkem získáte 390 Kč.

Vámi vybraná charita obdrží na začátku experimentu 100 Kč. Pokud uhodnete v rámci jednoho bloku správně 10 hodů, charita ztratí 50 Kč z tohoto počátečního příspěvku. Pokud uhodnete 11 hodů, charita ztratí dalších 100 Kč. Pokud uhodnete správně všech 12 hodů v rámci jednoho bloku, charita ztratí dalších 150 Kč. Charita tedy z počátečního příspěvku může ztratit až 300 Kč. Když je ztráta vyšší než počáteční příspěvek, tato ztráta se odečítá z příspěvku ostatních účastníků výzkumu.

Poté, co dokončíte všech šest bloků, bude jeden blok náhodně vylosován. Obdržíte pouze peníze, které jste vydělali v tomto vylosovaném bloku. Charita taktéž ztrácí peníze z počátečního příspěvku jen dle počtu správně uhodnutých hodů v rámci tohoto vylosovaného bloku. Pokud správně uhodnete všech dvanáct hodů v daném bloku, a tento blok bude později vylosován, obdržíte 390 Kč a charita ztratí ze svého počátečního příspěvku 300 Kč. Vaše výsledky v ostatních blocích nijak neovlivní množství peněz, které obdržíte vy nebo vámi vybraná charita.

Abychom ověřili, že rozumíte instrukcím, prosím odpovězte na následující otázku:
Když správně uhodnete 7 hodů z 12 v prvním bloku, 5 hodů z 12 ve druhém bloku, 2 hody z 12 ve třetím bloku a 8 hodů ve čtvrtém a pátém bloku a 4 hody v šestém bloku a poté je vylosován třetí blok, kolik peněz obdržíte?
"""

wrong_answer = "{} Kč je chybná odpověď, správná odpověď je 15 Kč. Byl vylosován třetí blok, ve kterém jste správně uhodli 2 hody. Obdržíte tedy 5 + 10 = 15 Kč."
correct_answer = "15 Kč je správná odpověď. Byl vylosován třetí blok, ve kterém jste správně uhodli 2 hody. Obdržíte tedy 5 + 10 = 15 Kč."

second_check_question = "Dříve než začnete, zkuste odhadnout, kolik hodů správně uhodnete ve vylosovaném bloku."
prediction_label = "správných předpovědí"
wrong_trials = "V jednom bloku je pouze 12 hodů!"


intro_block_2 = """
Toto je konec prvního bloku. Pokud bude tento blok vylosován, obdržíte {} Kč. Nyní začne druhý blok s dvanácti koly.
"""

endtext = """Toto je konec posledního bloku. Pokud bude tento blok vybrán, obdržíte {} Kč.

Toto je konec úkolu s kostkou.
"""

third = ("druhého", "třetí")
fourth = ("třetího", "čtvrtý")
fifth =  ("čtvrtého", "pátý")






################################################################################


class Cheating(ExperimentFrame):
    def __init__(self, root, block):
        super().__init__(root)

        #######################
        # adjustable parameters
        self.trials = 12 # change for testing
        self.pause_after_roll = 0.5
        self.pause_before_trial = 0.2
        self.displayNum = self.createDots # self.createDots or self.createText
        self.fakeRolling = True # False for testing
        self.diesize = 240
        self.rewards = [i*5 + 5 for i in range(self.trials)]
        #######################

        global conditions
        self.condition = conditions[block - 1]
        self.blockNumber = block

        self.width = self.root.screenwidth
        self.height = self.root.screenheight

        self.file.write("Cheating {}\n".format(block))

        self.upperText = Text(self, height = 5, width = 80, relief = "flat", font = "helvetica 15",
                              wrap = "word")
        self.upperButtonFrame = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                                       background = "white", height = 100)
        self.die = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                          background = "white", width = self.diesize, height = self.diesize)
        self.bottomText = Text(self, height = 3, width = 80, relief = "flat", font = "helvetica 15",
                               wrap = "word")
        self.bottomButtonFrame = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                                        background = "white", height = 100)

        self.infoWinnings = ttk.Label(self, text = "", font = "helvetica 15",
                                      background = "white", justify = "right")
        self.fillerLeft = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                                 background = "white", width = 200, height = 1)
        self.fillerRight = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                                  background = "white", width = 200, height = 1)
        self.infoWinnings.grid(row = 1, column = 2, sticky = NW)
        self.fillerLeft.grid(column = 0, row = 0)
        self.fillerRight.grid(column = 0, row = 0)

        self.upperText.grid(column = 1, row = 1)
        self.upperButtonFrame.grid(column = 1, row = 2)
        self.die.grid(column = 1, row = 3, pady = 40)
        self.bottomText.grid(column = 1, row = 4)
        self.bottomButtonFrame.grid(column = 1, row = 5)
        self._createFiller()

        self["highlightbackground"] = "white"
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 4)

        self.currentTrial = 0

        ttk.Style().configure("TButton", font = "helvetica 15")

        if not hasattr(self.root, "wins"):
            self.root.wins = defaultdict(int)            

        self.responses = []


    def run(self):
        self.bottomText["state"] = "disabled"
        self.upperText["state"] = "disabled"
        if self.currentTrial < self.trials:
            self.currentTrial += 1
            self.startTrial()
        else:
            fee = FEE if conditions[self.blockNumber - 1] == "fee_treatment" else 0
            self.root.texts["win" + str(self.blockNumber)] = sum(self.rewards[:self.root.wins[self.blockNumber]]) - fee
            if self.blockNumber == 5:
                win = random.randint(1, 5)
                self.root.texts["dice"] = self.root.texts["win{}".format(win)]
                self.root.texts["block"] = win
            self.nextFun()


    def startTrial(self):
        self.time = perf_counter()
        self.showWinnings()
        self.upperPart()


    def _createFiller(self):
        self.fillerFrame = Canvas(self.bottomButtonFrame, highlightbackground = "white",
                                  highlightcolor = "white", background = "white", height = 100, width = 1)
        self.fillerFrame.grid(column = 0, row = 0, sticky = NS)


    def upperPart(self):
        self.upperText["state"] = "normal"
        if "treatment" in self.condition:
            ttk.Style().configure("TCheckbutton", background = "white", font = "helvetica 15")
            self.predictionVar = BooleanVar()
            self.predictionVar.set(False)
            self.upperText.insert("1.0", treatmenttext.format(self.currentTrial))
            self.predictedCB = ttk.Checkbutton(self.upperButtonFrame, text = predictiontext,
                                               command = self.checkbuttoned, variable = self.predictionVar,
                                               onvalue = True, offvalue = False)
            self.predictedCB.grid(row = 0, column = 1, pady = 15)
        elif "control" in self.condition:
            ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
            self.predictionVar = StringVar()
            self.upperText.insert("1.0", controltext.format(self.currentTrial))
            self.evenButton = ttk.Radiobutton(self.upperButtonFrame, text = eventext, value = "even",
                                              variable = self.predictionVar, command = self.checked)
            self.oddButton = ttk.Radiobutton(self.upperButtonFrame, text = oddtext, value = "odd",
                                             variable = self.predictionVar, command = self.checked)
            self.evenButton.grid(row = 0, column = 2, padx = 10, pady = 15)
            self.oddButton.grid(row = 0, column = 0, padx = 10, pady = 15)

        self.rollButton = ttk.Button(self.upperButtonFrame, text = rolltext, command = self.roll,
                                     state = "disabled")
        self.rollButton.grid(row = 1, column = 1)
        self.upperText["state"] = "disabled"


    def checked(self):
        self.rollButton["state"] = "!disabled"


    def checkbuttoned(self):
        self.rollButton["state"] = "!disabled"
        self.predictedCB["state"] = "disabled"


    def bottomPart(self):
        self.bottomText["state"] = "normal"
        if "treatment" in self.condition:
            self.bottomText.insert("1.0", treatmenttext2.format(self.rewards[self.root.wins[self.blockNumber]]))
            ttk.Style().configure("Green.TButton", foreground = "green")
            ttk.Style().configure("Red.TButton", foreground = "red")
            self.winButton = ttk.Button(self.bottomButtonFrame, text = correcttext,
                                        command = lambda: self.answer("win"), width = 18, style = "Green.TButton")
            self.lossButton = ttk.Button(self.bottomButtonFrame, text = incorrecttext,
                                         command = lambda: self.answer("loss"), width= 18, style = "Red.TButton")
            self.winButton.grid(row = 0, column = 0, padx = 30)
            self.lossButton.grid(row = 0, column = 2, padx = 30)
        elif "control" in self.condition:
            win = (self.response == "odd" and self.currentRoll in (1,3,5)) or (
                self.response == "even" and self.currentRoll in (2,4,6))
            text = wintext if win else losstext
            text = text.format(self.rewards[self.root.wins[self.blockNumber]])
            if win:
                self.root.wins[self.blockNumber] += 1
            self.bottomText.insert("1.0", controltext2.format(text))
            self.continueButton = ttk.Button(self.bottomButtonFrame, text = continuetext,
                                             command = self.answer)
            self.continueButton.grid(row = 0, column = 1)
        self.bottomText["state"] = "disabled"


    def roll(self):
        self.firstResponse = perf_counter()
        if "treatment" in self.condition:
            self.response = "NA"    
        else:
            self.response = self.predictionVar.get()
            self.oddButton["state"] = "disabled"
            self.evenButton["state"] = "disabled"
        self.rollButton["state"] = "disabled"
        self.die.create_rectangle((5, 5, self.diesize - 5, self.diesize - 5),
                                  fill = "white", tag = "die", outline = "black", width = 5)
        # fake rolling
        if self.fakeRolling:
            for roll in range(random.randint(4,6)):         
                self.displayNum(self.diesize/2, self.diesize/2, random.randint(1, 6))
                self.update()
                sleep(0.2)
                self.die.delete("dots")
        self.currentRoll = random.randint(1, 6)
        self.displayNum(self.diesize/2, self.diesize/2, self.currentRoll)
        self.update()
        sleep(self.pause_after_roll)
        self.beforeSecondResponse = perf_counter()
        self.bottomPart()


    def createDots(self, x0, y0, num):
        positions = {"1": [(0,0)],
                     "2": [(-1,-1), (1,1)],
                     "3": [(-1,-1), (0,0), (1,1)],
                     "4": [(-1,-1), (-1,1), (1,-1), (1,1)],
                     "5": [(-1,-1), (-1,1), (0,0), (1,-1), (1,1)],
                     "6": [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0)]}
        for x, y in positions[str(num)]:
            d = self.diesize/4
            coords = [x0 + x*d + d/3, y0 - y*d + d/3,
                      x0 + x*d - d/3, y0 - y*d - d/3]
            self.die.create_oval(tuple(coords), fill = "black", tag = "dots")


    def createText(self, x0, y0, num):
        self.die.create_text(x0, y0, text = str(num), font = "helvetica 70", tag = "die")

    def showWinnings(self):
        fee = FEE if conditions[self.blockNumber - 1] == "fee_treatment" else 0
        self.infoWinnings["text"] = "Současná výhra:\n{} Kč".format(sum(self.rewards[:self.root.wins[self.blockNumber]]) - fee)

    def answer(self, answer = "NA"):
        t = perf_counter()
        if answer == "win":
            self.root.wins[self.blockNumber] += 1
        self.responses.append([self.blockNumber, self.currentTrial, self.condition,
                               self.currentRoll, self.response,
                               answer, t - self.time, self.firstResponse - self.time,
                               t - self.beforeSecondResponse])
        self.bottomText["state"] = "normal"
        self.upperText["state"] = "normal"
        self.die.delete("die")
        self.die.delete("dots")
        self.upperText.delete("1.0", "end")
        self.bottomText.delete("1.0", "end")
        for child in self.upperButtonFrame.winfo_children():
            child.grid_remove()
        for child in self.bottomButtonFrame.winfo_children():
            child.grid_remove()
        self._createFiller()
        self.showWinnings()
        self.update()
        sleep(self.pause_before_trial)
        self.run()
        
                   
    def write(self):
        for response in self.responses:
            begin = [self.id]
            self.file.write("\t".join(map(str, begin + response)) + "\n")

     
    

class CheatingInstructions(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = intro_block_1, height = 23, font = 15)

        self.predictionVar = StringVar()
        self.checkVar = StringVar()
        self.vcmd = (self.register(self.onValidate), '%P')
        self.checkFrame = Canvas(self, background = "white", highlightbackground = "white",
                                 highlightcolor = "white")
        self.checkFrame.grid(row = 2, column = 1)
        self.entry = ttk.Entry(self.checkFrame, textvariable = self.checkVar, width = 10, justify = "right",
                               font = "helvetica 15", validate = "key", validatecommand = self.vcmd)
        self.entry.grid(row = 2, column = 1, padx = 6)
        self.currencyLabel = ttk.Label(self.checkFrame, text = "Kč", font = "helvetica 16",
                                       background = "white")
        self.currencyLabel.grid(row = 2, column = 2, sticky = NSEW)

        self.lowerText = Text(self, font = "helvetica 15", relief = "flat", background = "white",
                              width = 90, height = 3, wrap = "word", highlightbackground = "white")
        self.lowerText.grid(row = 3, column = 1, pady = 15)
        self.lowerText["state"] = "disabled"

        self.bottomText = Text(self, font = "helvetica 15", relief = "flat", background = "white",
                               width = 90, height = 2, wrap = "word", highlightbackground = "white",
                               state = "disabled")
        self.bottomText.grid(row = 4, column = 1)
        self.bottomAnswers = Canvas(self, height = 40, background = "white", highlightbackground = "white",
                                    highlightcolor = "white")
        self.bottomAnswers.grid(row = 5, column = 1)
        self.predictionsLab = ttk.Label(self.bottomAnswers, text = prediction_label, font = "helvetica 15",
                                        background = "white", foreground = "white")
        self.predictionsLab.grid(row = 0, column = 1, sticky = NSEW, pady = 12)
        self.bottomMistakes = Text(self, font = "helvetica 15", relief = "flat", background = "white",
                                   width = 90, height = 1, wrap = "word", highlightbackground = "white",
                                   state = "disabled", foreground = "red")
        self.bottomMistakes.tag_config("centered", justify = "center")
        self.bottomMistakes.grid(row = 6, column = 1, pady = 10)
        
        self.next.grid(row = 7, column = 1)
        self.next["state"] = "disabled"
        self.text.grid(row = 1, column = 1, columnspan = 1)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 0)
        self.rowconfigure(7, weight = 1)
        self.rowconfigure(8, weight = 2)

        self.checked = False
        
    def onValidate(self, P):
        try:
            if int(P) >= 0:
                self.next["state"] = "!disabled"
            else:
                self.next["state"] = "disabled"
        except Exception as e:
            self.next["state"] = "disabled"
        return True
    
    def nextFun(self):
        if self.checked:
            if int(self.predictionVar.get()) > 12:
                self.bottomMistakes["state"] = "normal"
                self.bottomMistakes.delete("1.0", "end")
                self.bottomMistakes.insert("1.0", wrong_trials, "centered")
                self.bottomMistakes["state"] = "disabled"
                return
            self.write()
            super().nextFun()
        else:
            answer = int(self.checkVar.get())
            if answer == 15:
                text = correct_answer.format(answer)
            else:
                text = wrong_answer.format(answer)
            self.lowerText["state"] = "normal"
            self.lowerText.insert("1.0", text)
            self.lowerText["state"] = "disabled"
            self.next["state"] = "disabled"
            self.checked = True
            self.bottomText["state"] = "normal"
            self.bottomText.insert("1.0", second_check_question)
            self.bottomText["state"] = "disabled"
            self.vcmd2 = (self.register(self.onValidate), '%P')
            self.predictionsEntry = ttk.Entry(self.bottomAnswers, textvariable = self.predictionVar, width = 10,
                                              justify = "right", font = "helvetica 16", validate = "key",
                                              validatecommand = self.vcmd2)
            self.predictionsLab["foreground"] = "black"
            self.predictionsEntry.grid(row = 0, column = 0, padx = 6)

    def write(self):
        self.file.write("Cheating estimates\n")
        self.file.write(self.id + "\t" + self.predictionVar.get() + "\n\n")



class PaymentFrame(InstructionsFrame):
    def __init__(self, root, text, name):
        super().__init__(root, text = text, height = 8, font = 15)

        self.name = name

        self.offerVar = StringVar()
        self.vcmd = (self.register(self.onValidate), '%P')
        self.offerFrame = Canvas(self, background = "white", highlightbackground = "white",
                                 highlightcolor = "white")
        self.offerFrame.grid(row = 2, column = 1)
        self.entry = ttk.Entry(self.offerFrame, textvariable = self.offerVar, width = 10, justify = "right",
                               font = "helvetica 15", validate = "key", validatecommand = self.vcmd)
        self.entry.grid(row = 2, column = 1, padx = 6)
        self.currencyLabel = ttk.Label(self.offerFrame, text = "Kč", font = "helvetica 16",
                                       background = "white")
        self.currencyLabel.grid(row = 2, column = 2, sticky = NSEW)
               
        self.next.grid(row = 4, column = 1)
        self.next["state"] = "disabled"        

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)        
      
    def onValidate(self, P):
        try:
            if int(P) >= 0:
                self.next["state"] = "!disabled"
            else:
                self.next["state"] = "disabled"
        except Exception as e:
            self.next["state"] = "disabled"
        return True
  
    def write(self):
        self.file.write(self.name + "\n")
        self.file.write(self.id + "\t" + self.offerVar.get() + "\n\n")

    def nextFun(self):
        self.write()
        super().nextFun()   



class Auction(PaymentFrame):
    def __init__(self, root):
        super().__init__(root, text = intro_auction, name = "Auction")
  
    def write(self):
        super().write()

        filepath = os.path.join(os.getcwd(), "Data", "Auction")
        if not os.path.exists(filepath):
            os.mkdir(filepath)

        with open(os.path.join(filepath, "Auction" + self.id), mode = "w") as self.infile:
            self.infile.write(self.id + "\t" + self.offerVar.get() + "\t" + str(random.random()))



class BDM(PaymentFrame):
    def __init__(self, root):
        super().__init__(root, text = intro_BDM, name = "BDM")



class Wait(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = wait_text, height = 8, font = 15, proceed = False)

        self.timer = 0
    

    def checkOffers(self):
        # timer display
        self.timer += 1
        if self.timer > 15:
            self.timer = 1
        self.text.config(state = "normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", wait_text + "\n")
        self.text.insert("2.0", "."*self.timer)
        self.update()
        self.text.config(state = "disabled")

        offerfiles = os.listdir(os.path.join(os.getcwd(), "Data", "Auction"))
        if len(offerfiles) == 4:
            interested = []
            maxoffer = 0
            for file in offerfiles:
                with open(os.path.join(os.getcwd(), "Data", "Auction", file), mode = "r") as infile:
                    text = infile.readline()
                    participant, offer, random_number = text.split("\t")
                    offer = int(offer)
                    random_number = float(random_number)
                    if offer > maxoffer:
                        interested = [participant, random_number]
                    elif offer == maxoffer:
                        if not interested:
                            interested = [participant, random_number]
                        else:
                            if random_number > interested[1]:
                                interested = [participant, random_number]
            # change
            global conditions            
            conditions[0] = "treatment" if self.id == interested[0] else "control"
            self.nextFun()  
        else:
            print(self.timer) #
            self.update()       
            sleep(1)
            self.checkOffers()

    def run(self):
        self.checkOffers()
            


       

        
conditions = ["treatment", "control"]
random.shuffle(conditions)


Instructions1 = CheatingInstructions
Instructions2 = (InstructionsFrame, {"text": intro_block_2, "height": 5, "update": ["win1"]})
# Auction4 = (Auction, {"roundNum": 4, "update": ["win3"]})
# Auction5 = (Auction, {"roundNum": 5, "update": ["win4"]})
# Auction6 = (Auction, {"roundNum": 6})

BlockOne = (Cheating, {"block": 1})
BlockTwo = (Cheating, {"block": 2})
BlockThree = (Cheating, {"block": 3})
BlockFour = (Cheating, {"block": 4})
BlockFive = (Cheating, {"block": 5})
BlockSix = (Cheating, {"block": 6})

EndCheating = (InstructionsFrame, {"text": endtext, "height": 5, "update": ["win6"]})




if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([BDM, #!
         Auction, #!
         Wait, #!
         Instructions1,
         BlockOne,
         Instructions2,
         BlockTwo,
         BDM,
         BlockThree,
         Auction,
         #Auction4,
         Wait,
         BlockFour,
         Auction,
         #Auction5,
         Wait,
         BlockFive,
         Auction,
         #Auction6,
         Wait,
         BlockSix,
         EndCheating,
         DebriefCheating
         ])
