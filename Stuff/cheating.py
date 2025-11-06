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

from common import ExperimentFrame, InstructionsFrame, Measure, MultipleChoice, InstructionsAndUnderstanding, OneFrame, Question, TextArea
from gui import GUI
from constants import TESTING, URL, COEFFICIENTS, PREDICTION_BONUS, BEFORE, AFTER
from login import Login


################################################################################
# TEXTS

# PRVNÍ BLOK
intro_block_1 = """V následujícím úkolu budete hádat, jestli na virtuální kostce (generátor náhodných čísel) na Vašem počítači padne liché, nebo sudé číslo. Každé z čísel 1, 2, 3, 4, 5 a 6 může padnout se stejnou pravděpodobností. Lichá čísla jsou 1, 3 a 5. Sudá čísla jsou 2, 4 a 6. 

Úkol je rozdělen do pěti samostatných bloků a každý blok sestává z dvanácti kol. V každém kole budete hádat výsledek jednotlivých hodů kostkou. Bloky se odlišují pravidly, dle nichž budete hádat hody kostkou. Pravidla níže však platí pro všechny pět bloků.

Uhodnete-li první hod v daném bloku, získáte 3 Kč, uhodnete-li další, získáte za něj dalších 6 Kč, uhodnete-li další hod, získáte za něj dalších 9 Kč a tak dále. Za každý další uhodnutý hod získáte navíc částku o 3 Kč vyšší, než byla předchozí odměna. Pokud tedy uhodnete všech 12 hodů v daném bloku, za poslední dvanáctý uhodnutý hod získáte 36 Kč a celkem získáte 234 Kč. 

Celkové odměny za různé množství správných odhadů jsou zobrazeny v této tabulce:
<c>
Správných odhadů |   0 |   1 |   2 |   3 |   4 |   5 |   6 |   7 |   8 |   9 |  10 |  11 |  12 |
------------------------------------------------------------------------------------------------
Vaše odměna v Kč |   0 |   3 |   9 |  18 |  30 |  45 |  63 |  84 | 108 | 135 | 165 | 198 | 234 |
</c>
Po skončení studie bude jeden blok náhodně vylosován. Obdržíte peníze, které jste vydělali pouze v tomto vylosovaném bloku. Pokud správně uhodnete všech dvanáct hodů v daném bloku, a tento blok bude později vylosován, obdržíte 234 Kč. Vaše výsledky v ostatních blocích nijak neovlivní množství peněz, které obdržíte.

Abychom ověřili, že rozumíte instrukcím, odpovězte prosím na kontrolní otázky:"""


intro_control1 = 'Které tvrzení o úkolu je pravdivé?' 
intro_answers1 = ['Pravděpodobnost správného odhadu v každém kole je 50%.', 'V každém bloku úkolu učiníte deset odhadů.', 'Odměna za úkol je dána součtem správných odhadů v pěti blocích úkolu.', 'Jakmile úkol dokončíte, experimentátor Vám za něj vyplatí odměnu.'] 
intro_feedback1 = ['Ano, budete odhadovat jednu ze dvou stejně pravděpodobných možností.', 'Ne, každý blok sestává z dvanácti kol.', 'Ne, odměna závisí pouze na počtu správných odhadů v jednom náhodně vylosovaném bloku.', 'Ne, odměna bude vyplacena až za všechny části studie dohromady po jejím skončení.']

intro_control2 = 'Kolik obdržíte za úkol peněz, pokud bude vylosován blok, kde uhodnete dohromady 4 hody?' 
intro_answers2 = ['18 Kč (0 + 3 + 6 + 9)', '27 Kč (3 + 6 + 9 + 9)', '30 Kč (3 + 6 + 9 + 12)', '36 Kč (4 x 9)'] 
intro_feedback2 = ['Ne, obdželi byste 30 Kč. Za první hod 3 Kč a za každý další o 3 Kč více (tj. 3 + 6 + 9 + 12).', 'Ne, obdželi byste 30 Kč. Za první hod 3 Kč a za každý další o 3 Kč více (tj. 3 + 6 + 9 + 12).', 'Ano, obdželi byste 30 Kč.', 'Ne, obdželi byste 30 Kč. Za první hod 3 Kč a za každý další o 3 Kč více (tj. 3 + 6 + 9 + 12).']


# ÚLOHA
continuetext = "Pokračovat"
oddtext = "Liché (1, 3 nebo 5)"
eventext = "Sudé (2, 4 nebo 6)"
rolltext = "Hodit kostkou"
correcttext = "Správně"
incorrecttext = "Špatně"    
predictiontext = "Zvolil(a) jsem, jestli na kostce padne liché, nebo sudé číslo."

treatmenttext = '''Blok {}, Kolo {}

Máte za úkol uhodnout, zda na kostce padne liché, nebo sudé číslo. Nyní prosím zvolte, zda v následujícím hodu padne liché, nebo sudé číslo, zapamatujte si svoji volbu a poté klikněte na tlačítko "Hodit kostkou".
'''

treatmenttext2 = "Zvolte, zda jste hádali správně a vydělali v tomto kole {} Kč, nebo zda jste hádali špatně a nevydělali jste v tomto kole nic."


controltext = """Blok {}, Kolo {}

Máte za úkol uhodnout, zda na kostce padne liché, nebo sudé číslo. Nyní prosím zvolte, zda v následujícím hodu padne liché, nebo sudé číslo, a poté klikněte na tlačítko "Hodit kostkou".
"""

controltext2 = "V tomto kole byla Vaše předpověď {}"
wintext = "správná a vydělali jste {} Kč."
losstext = "špatná a nevydělali jste možných {} Kč."


# DRUHÝ BLOK
intro_block_2 = """
Toto je konec prvního bloku. Pokud bude tento blok vylosován, obdržíte {} Kč. Nyní začne druhý blok s dvanácti koly.
"""


# TŘETÍ BLOK
intro_block_3 = """<b>Pro následující tři bloky jste byli náhodně přiděleni do skupiny spolu s dalšími dvěma účastníky studie. Všichni ve skupině máte stejná pravidla.

Celková odměna, kterou v bloku získáte, bude odečtena od částky 250 Kč{} a rovnoměrně rozdělena mezi zbývající dva členy skupiny.</b>

Celkové odměny za různé množství správných odhadů jsou zobrazeny v této tabulce:
<c>
Správných odhadů |   0 |   1 |   2 |   3 |   4 |   5 |   6 |   7 |   8 |   9 |  10 |  11 |  12 |
------------------------------------------------------------------------------------------------
Vaše odměna v Kč |   0 |   3 |   9 |  18 |  30 |  45 |  63 |  84 | 108 | 135 | 165 | 198 | 234 |
------------------------------------------------------------------------------------------------
Odměna ostatních |{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|
</c>
Například uhodnete-li 6 hodů, získáte 63 Kč (“Vaše odměna v Kč”). Ostatní dle uvedených pravidel získají 250 - 63 = 187 Kč{}, rozděleno dvěma spoluhráčům znamená, že <b>každý z nich</b> dostane {} Kč (“Odměna ostatních”). 

K odměně, kterou získáte Vy ve svých odhadech, obdržíte navíc zbývající odměnu od dvou svých spoluhráčů (Vy získáte to, co u nich je v položce “Odměna ostatních”).

<b>Důležité opakování:</b> Zbývající dva členové skupiny hrají hru za stejných podmínek. Platí tedy, že čím více získáte při hraní úlohy Vy, tím méně získají ostatní. Obdobně platí, že čím více získají při hraní úlohy ostatní, tím méně získáte Vy.

Před pokračováním si odpovězte na následující kontrolní otázku."""

condition_text = ", vynásobena koeficientem {}"

q3 = "Kolik Kč dohromady získají členové Vaší skupiny dle pravidel uvedených výše,\npokud správně uhádnete 8 hodů a bude vylosován tento blok k proplacení?"
answers3 = ["{} Kč", "{} Kč", "{} Kč", "{} Kč"]
feedback3 = ["Špatná odpověď. {}", "Špatná odpověď. {}", "Špatná odpověď. {}", "Správná odpověď. {}"]
explanation3 = "Každý získá {} Kč (“Odměna ostatních”) pro 8 správných odhadů, dohromady proto získají {} × 2 = {} Kč (hrajete s dvěma účastníky)."

choice_third = """Nyní Vás čeká třetí blok s dvanácti koly. V tomto bloku si můžete vybrat, zda <b>Vy budete hrát verzi “PŘED” nebo “PO”.</b> Ostatní členové skupiny rovněž sami rozhodují, zda budou oni sami hrát verzi “PŘED” nebo “PO”.

Pro připomenutí:
Celková odměna, kterou v bloku získáte, bude odečtena od částky 250 Kč{} a rovnoměrně rozdělena mezi zbývající dva členy skupiny.

Celkové odměny za různé množství správných odhadů jsou zobrazeny v této tabulce:
<c>
Správných odhadů |   0 |   1 |   2 |   3 |   4 |   5 |   6 |   7 |   8 |   9 |  10 |  11 |  12 |
------------------------------------------------------------------------------------------------
Vaše odměna v Kč |   0 |   3 |   9 |  18 |  30 |  45 |  63 |  84 | 108 | 135 | 165 | 198 | 234 |
------------------------------------------------------------------------------------------------
Odměna ostatních |{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|
</c>
Ve <b>verzi “PŘED”</b> uvádíte předpovědi před hodem kostkou. Po zvolení možnosti vidíte výsledek hodu a dozvíte se, zda jste uhodli, či nikoliv a kolik jste vydělali.
Ve <b>verzi “PO”</b> uvádíte, zda jste uhodli, či nikoliv a kolik jste vydělali, až poté, co vidíte výsledek hodu kostkou.


Chcete, hrát verzi “PŘED” nebo “PO”?"""


prediction_third = """Toto je konec druhého bloku o dvanácti kolech. Pokud bude tento blok vylosován, obdržíte {} Kč.

Jak jste zaznamenali, úkol měl dvě verze:
<b>Verzi “PŘED”</b>, ve které uvádíte předpovědi před hodem kostkou. Po zvolení možnosti vidíte výsledek hodu a dozvíte se, zda jste uhodli, či nikoliv a kolik jste vydělali.
<b>Verzi “PO”</b>, ve které uvádíte, zda jste uhodli, či nikoliv a kolik jste vydělali, až poté, co vidíte výsledek hodu kostkou.

Podobně jako jste hráli tato dvě kola úlohy Vy, hráli ji v dřívější studii za stejných podmínek jiní účastníci studie.

Odhadněte, kolik správných předpovědí u hodu kostkou průměrně učinili tito účastníci studie v “PŘED” verzi úkolu a kolik nahlásili průměrně správných předpovědí v “PO” verzi úkolu. Pokud se ani jeden z Vašich odhadů nebude od skutečné průměrné hodnoty lišit o více než 0,2, dostanete k dnešní odměně navíc {} Kč.

Odhad musí být v rozmezí od 0 do 12 a je možné používat desetinná místa.

Odhad uveďte pro každou z verzí níže:
"""


intro_block_4 = """Toto je konec třetího bloku o dvanácti kolech. Pokud bude tento blok vylosován, obdržíte {} Kč a oba zbývající členové skupiny po {} Kč.

Nyní Vás čeká čtvrtý blok s dvanácti koly. 

<b>Zde je důležitá změna:</b> V tomto bloku můžete vybrat, zda <b>všichni členové Vaší skupiny</b> mají hrát verzi “PŘED” nebo “PO”. Všichni následně budete hrát verzi úlohy, pro kterou hlasovali dva nebo více členů Vaší skupiny. 

Oproti předchozímu bloku nevolíte verzi úlohy pro sebe, ale pro všechny členy skupiny. Může se stát, že nebudete hrát Vámi zvolenou verzi úlohy, pokud oba zbývající členové skupiny budou hlasovat pro druhou z verzí.

Před pokračováním odpovězte na následující kontrolní otázku."""

q4 = "Co se stane, pokud vyberete verzi „PO“ a jeden ze zbývajících dvou členů skupiny také hlasuje pro tuto verzi?"
answers4 = ["Všichni budete hrát verzi „PO”.", "Všichni budete hrát verzi „PŘED”.", "Verze bude zvolena pro všechny náhodně.", "Každý člen skupiny bude hrát svou vybranou verzi."]
feedback4 = ["Správná odpověď. Jste ve skupině tří osob, pakliže Vy a další člen hlasujete pro “PO” verzi, pak většina zvolila “PO” verzi. “PO” verzi budete hrát všichni.", "Špatná odpověď. Jste ve skupině tří osob, pakliže Vy a další člen hlasujete pro “PO” verzi, pak většina zvolila “PO” verzi. “PO” verzi budete hrát všichni.", "Špatná odpověď. Jste ve skupině tří osob, pakliže Vy a další člen hlasujete pro “PO” verzi, pak většina zvolila “PO” verzi. “PO” verzi budete hrát všichni.", "Špatná odpověď. Jste ve skupině tří osob, pakliže Vy a další člen hlasujete pro “PO” verzi, pak většina zvolila “PO” verzi. “PO” verzi budete hrát všichni."]

choice_fourth = """Nyní můžete vybrat, jestli chcete, aby <b>všichni členové Vaší skupiny</b> hráli verzi “PŘED” nebo “PO”. Všichni následně budete hrát verzi úlohy, pro kterou hlasovali dva nebo více členů skupiny. 

Pro připomenutí:
Ve <b>verzi “PŘED”</b> uvádíte předpovědi před hodem kostkou. Po zvolení možnosti vidíte výsledek hodu a dozvíte se, zda jste uhodli, či nikoliv a kolik jste vydělali.
Ve <b>verzi “PO”</b> uvádíte, zda jste uhodli, či nikoliv a kolik jste vydělali, až poté, co vidíte výsledek hodu kostkou.

Stále platí, že celková odměna, kterou v bloku získáte, bude odečtena od částky 250 Kč{} a rovnoměrně rozdělena mezi zbývající dva členy skupiny. Zbývající dva členové skupiny hrají hru za stejných podmínek.

Chcete, aby Vaše skupina hrála verzi “PŘED” nebo “PO”?"""


intro_block_5 = """Toto je konec čtvrtého bloku o dvanácti kolech. Pokud bude tento blok vylosován, obdržíte {} Kč a oba zbývající členové skupiny získají od Vás po {} Kč.{}

Nyní Vás čeká pátý blok s dvanácti koly. V tomto bloku opět můžete hlasovat, jestli chcete, aby <b>Vaše skupina hrála verzi “PŘED” nebo “PO”.</b> Všichni následně budete hrát verzi úlohy, pro kterou hlasovali dva nebo více členů skupiny. 

Stále platí, že celková odměna, kterou v bloku získáte, bude odečtena od částky 250 Kč{} a rovnoměrně rozdělena mezi zbývající dva členy skupiny. Zbývající dva členové skupiny hrají hru za stejných podmínek.

Pro připomenutí:
Ve <b>verzi “PŘED”</b> uvádíte předpovědi před hodem kostkou. Po zvolení možnosti vidíte výsledek hodu a dozvíte se, zda jste uhodli, či nikoliv a kolik jste vydělali.
Ve <b>verzi “PO”</b> uvádíte, zda jste uhodli, či nikoliv a kolik jste vydělali, až poté, co vidíte výsledek hodu kostkou.

Chcete, aby Vaše skupina hrála verzi “PŘED” nebo “PO”?
"""


from_others_text = " <b>Od zbývajících dvou hráčů byste v tomto kole získal(a) dohromady {} Kč, pokud by byl pro oba tento blok vylosován.</b>"


prediction_later = """Odhadněte, kolik správných odpovědí průměrně učiní zbývající dva členové Vaší skupiny v následujícím bloku, pokud bude Vaše skupina hrát “PŘED” verzi úkolu, kde se předpověď uvádí před hodem kostky, a kolik si myslíte, že průměrně nahlásí správných odpovědí, pokud bude Vaše skupina hrát “PO” verzi úkolu, kde se předpověď uvádí až po hodu kostkou.

Odhad musí být v rozmezi od 0 do 12 a je možné používat desetinná místa.

Odhad uveďte pro každou z verzí níže:"""

prediction_self =  "Následně odhadněte, kolik správných odpovědí učiníte v každé z verzí Vy.\n"


# INFORMACE O ZVOLENÉ VERZI
info_condition = "Vaše skupina zvolila verzi {}"
after_voted = "“PO”, ve které uvádíte, zda jste uhodli, či nikoliv a kolik jste vydělali, až poté, co vidíte výsledek hodu kostkou."
before_voted = "“PŘED”, ve které uvádíte předpovědi před hodem kostkou. Po zvolení možnosti vidíte výsledek hodu a dozvíte se, zda jste uhodli, či nikoliv a kolik jste vydělali."


# ČEKÁNÍ
wait_text = "Prosím počkejte na ostatní účastníky studie."


# KONEC
endtext = """Toto je konec posledního bloku. Pokud bude tento blok vylosován, obdržíte {} Kč a oba zbývající členové skupiny po {} Kč.

Toto je konec úkolu s kostkou.
"""


# buttons
controlchoicetext = "PŘED"
treatmentchoicetext = "PO"


endText = "V úloze s házením kostek byl náhodně vybrán blok {}. V úkolu s kostkou jste tedy vydělal(a) {} Kč."  
additional = "Na základě voleb ostatních hráčů v této úloze jste obdržel(a) navíc {} Kč"
correct_prediction = "Oba Vaše odhady počtu správných odhadů v úloze s kostkou účastníků dřívější studie byly správné a získal(a) jste za správné odhady {} Kč.".format(PREDICTION_BONUS)
incorrect_prediction = "Alespoň jeden z Vašich odhadů počtu správných odhadů v úloze s kostkou účastníků dřívější studie byl špatný a za odhady jste nezískal(a) nic."


################################################################################






class Cheating(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        #######################
        # adjustable parameters
        self.trials = 12 if not TESTING else 2
        self.pause_after_roll = 0.5
        self.pause_before_trial = 0.2
        self.displayNum = self.createDots # self.createDots or self.createText
        self.fakeRolling = not TESTING
        self.diesize = 240
        self.rewards = [i*3 + 3 for i in range(self.trials)]
        #######################

        self.otherrewards = [250 - i*3 + 3 for i in range(self.trials)]

        if not "block" in self.root.status:
            self.root.status["block"] = 1
            conditions = ["treatment", "control"]
            random.shuffle(conditions)  
            self.root.status["conditions"] = conditions
        self.blockNumber = self.root.status["block"]      
        
        self.condition = self.root.status["conditions"][self.blockNumber - 1]

        self.width = self.root.screenwidth
        self.height = self.root.screenheight

        self.file.write("Cheating {}\n".format(self.blockNumber))

        self.upperText = Text(self, height = 5, width = 60, relief = "flat", font = "helvetica 15",
                              wrap = "word")
        self.upperButtonFrame = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                                       background = "white", height = 100)
        self.die = Canvas(self, highlightbackground = "white", highlightcolor = "white",
                          background = "white", width = self.diesize, height = self.diesize)
        self.bottomText = Text(self, height = 3, width = 60, relief = "flat", font = "helvetica 15",
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
        self.fillerRight.grid(column = 2, row = 0)

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
            win = sum(self.rewards[:self.root.wins[self.blockNumber]])
            self.root.texts["win" + str(self.blockNumber)] = win            
            coefficient = {"low": COEFFICIENTS[0], "high": COEFFICIENTS[2], "control": COEFFICIENTS[1]}[self.root.status["condition"]]
            self.root.texts["otherwin" + str(self.blockNumber)] = ceil(round(((250 - win) * coefficient) / 2, 1))
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
            self.upperText.insert("1.0", treatmenttext.format(self.blockNumber, self.currentTrial))
            self.predictedCB = ttk.Checkbutton(self.upperButtonFrame, text = predictiontext,
                                               command = self.checkbuttoned, variable = self.predictionVar,
                                               onvalue = True, offvalue = False)
            self.predictedCB.grid(row = 0, column = 1, pady = 15)
        elif "control" in self.condition:
            ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
            self.predictionVar = StringVar()
            self.upperText.insert("1.0", controltext.format(self.blockNumber, self.currentTrial))
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
            reward = self.rewards[self.root.wins[self.blockNumber]]
            text = treatmenttext2.format(reward)
            self.bottomText.insert("1.0", text)
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
            if win:
                text = wintext.format(self.rewards[self.root.wins[self.blockNumber]])
                self.root.wins[self.blockNumber] += 1
            else:
                text = losstext.format(self.rewards[self.root.wins[self.blockNumber]])
            self.bottomText.insert("1.0", controltext2.format(text))
            self.showWinnings()
            self.continueButton = ttk.Button(self.bottomButtonFrame, text = continuetext, command = self.answer)
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
        if not TESTING:
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
        wins = self.root.wins[self.blockNumber]        
        self.infoWinnings["text"] = "Počet správných odhadů:\n{}".format(wins)        
        self.infoWinnings["text"] += "\n\nVaše současná výhra:\n{} Kč".format(sum(self.rewards[:wins]))

    def answer(self, answer = "NA"):
        t = perf_counter()
        if answer == "win":
            self.root.wins[self.blockNumber] += 1
        self.responses.append([self.blockNumber, self.currentTrial, self.condition, self.root.status["source"], 
                               self.root.status["condition"], self.currentRoll, self.response, answer, 
                               sum(self.rewards[:self.root.wins[self.blockNumber]]), t - self.time, self.firstResponse - self.time,
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
        self.root.status["block"] += 1
        for response in self.responses:
            begin = [self.id]
            self.file.write("\t".join(map(str, begin + response)) + "\n")

    
    def nextFun(self):
        if self.root.status["winning_block"] == self.blockNumber:
            self.root.status["reward"] += reward
            self.root.status["results"] += [endText.format(self.blockNumber, reward)]
        if self.blockNumber >= 3: # send the results of the after version in the fourth to fifth round            
            wins = self.root.wins[self.blockNumber]
            reward = sum(self.rewards[:self.root.wins[self.blockNumber]])
            outcome = "|".join(["outcome", str(wins), str(reward)])
            while True:
                data = urllib.parse.urlencode({'id': self.id, 'round': self.blockNumber, 'offer': outcome})
                data = data.encode('ascii')
                if URL == "TEST":
                    response = "ok"
                else:
                    try:
                        with urllib.request.urlopen(URL, data = data) as f:
                            response = f.read().decode("utf-8")       
                    except Exception:
                        continue
                if response == "ok":                    
                    super().nextFun()  
                    return            
                sleep(0.1)
        else:
            super().nextFun()  


    def gothrough(self):
        # nefunguje :(
        self.run()
       
        if "treatment" in self.condition:
            self.predictedCB.invoke()
            self.after(200, self.rollButton.invoke)
            self.after(200, self.winButton.invoke)
            #self.root.update()
            #self.after(500, self.update)
            #answer = random.choice([self.winButton, self.lossButton])
            #self.after(700, answer.invoke)
        elif "control" in self.condition:
            answer = random.choice([self.evenButton, self.oddButton])
            answer.invoke()            
            self.after(200, self.rollButton.invoke)
            self.update()
            self.after(200, self.continueButton.invoke)
            #self.root.update()
            #self.after(700, self.continueButton.invoke)



class Selection(InstructionsFrame):
    def __init__(self, root, text, **kwargs):

        if TESTING and "block" not in root.status: # REMOVE
            root.status["block"] = 3            

        if root.status["block"] == 3:
            self.update_intro(root.status["condition"], root)
            text = root.texts["introtext"]

        super().__init__(root, text = text, proceed = False, savedata = True, **kwargs)

        ttk.Style().configure("TButton", font = "helvetica 15", width = 16)

        self.control = ttk.Button(self, text = controlchoicetext,
                                  command = lambda: self.response("control"))
        self.treatment = ttk.Button(self, text = treatmentchoicetext,
                                    command = lambda: self.response("treatment"))
        self.control.grid(row = 2, column = 0)
        self.treatment.grid(row = 2, column = 2)        

    def response(self, choice):
        self.choice = choice
        self.nextFun()
 
    def update_intro(self, condition, root):   
        conditionText = {"low": condition_text.format(str(COEFFICIENTS[0]).replace(".", ",")), "high": condition_text.format(str(COEFFICIENTS[2]).replace(".", ",")), "control": ""}[condition]
        root.texts["conditionText"] = conditionText
        # global intro_block_3        
        otherRewards = ["{num: >4} ".format(num = ceil((250 - (1.5 * i) * (i + 1))*root.status["coefficient"] / 2)) for i in range(13)]        
        coef = str(root.status["coefficient"]).replace(".", ",")
        if coef != "1":
             coefText  = " × {} = {} Kč".format(coef, int(otherRewards[6])*2)
        else:
             coefText = ""
        root.texts["introtext"] = choice_third.format(conditionText, *otherRewards)

    def write(self):
        #self.root.texts["votingResponse"] = self.voteVar.get()
        self.file.write("Selection\n")       
        self.file.write(self.id + "\t" + str(self.root.status["block"]) + "\t" + self.choice + "\n\n")

        if self.root.status["block"] == 3:
            self.root.status["conditions"].append(self.choice)
            return

        data = urllib.parse.urlencode({'id': self.id, 'round': self.root.status["block"], 'offer': self.choice})
        data = data.encode('ascii')
        if URL != "TEST":
            for i in range(60):
                try: 
                    with urllib.request.urlopen(URL, data = data) as f:
                        if f.getcode() != 200 or f.read().decode("utf-8").strip() != "ok":
                            self.root.config(cursor = "wait")
                            self.root.update()
                            sleep(1)
                        else:
                            self.root.config(cursor = "")
                            break
                except Exception:
                    continue
            else:
                messagebox.showinfo(message = "Zavolejte prosím experimentátora.", icon = "error", parent = self.root, 
                                  detail = "Pravděpodobně je problém se serverem.", title = "Problém")
        else:
            self.root.status["TESTvote"] = self.choice



class Prediction(InstructionsFrame):
    def __init__(self, root):    
        if root.status["block"] == 3:    
            text = prediction_third.format(root.texts["win2"], PREDICTION_BONUS)  
            #height = 21
        else:
            text = prediction_later
            #height = 10

        super().__init__(root, text = text, height = "auto", font = 15, savedata = True)

        self.checkVar1 = StringVar()
        self.checkVar2 = StringVar()

        self.vcmd = (self.register(self.onValidate), '%P', "1")
        self.vcmd2 = (self.register(self.onValidate), '%P', "2")

        self.textBefore = ttk.Label(self, text = "PŘED verze:", background = "white", font = "helvetica 15")
        self.textBefore.grid(row = 2, column = 1, pady = 10, sticky = E, padx = 10)
        self.entryBefore = ttk.Entry(self, textvariable = self.checkVar1, width = 7, justify = "right",
                               font = "helvetica 15", validate = "key", validatecommand = self.vcmd)
        self.entryBefore.grid(row = 2, column = 2, pady = 10)

        self.textAfter = ttk.Label(self, text = "PO verze:", background = "white", font = "helvetica 15")
        self.textAfter.grid(row = 3, column = 1, pady = 10, sticky = E, padx = 10)
        self.entryAfter = ttk.Entry(self, textvariable = self.checkVar2, width = 7, justify = "right",
                               font = "helvetica 15", validate = "key", validatecommand = self.vcmd2)
        self.entryAfter.grid(row = 3, column = 2, pady = 10)

        self.vars = [self.checkVar1, self.checkVar2]

        if self.root.status["block"] != 3:
            self.checkVar3 = StringVar()
            self.checkVar4 = StringVar()
            self.vcmd3 = (self.register(self.onValidate), '%P', "3")
            self.vcmd4 = (self.register(self.onValidate), '%P', "4")
            self.label = ttk.Label(self, text = prediction_self, background = "white", font = "helvetica 15")
            self.label.grid(row = 4, column = 0, columnspan = 4, pady = 10, sticky = "S")

            self.textBefore2 = ttk.Label(self, text = "PŘED verze:", background = "white", font = "helvetica 15")
            self.textBefore2.grid(row = 5, column = 1, pady = 10, sticky = E, padx = 10)
            self.entryBefore2 = ttk.Entry(self, textvariable = self.checkVar3, width = 7, justify = "right",
                                font = "helvetica 15", validate = "key", validatecommand = self.vcmd3)
            self.entryBefore2.grid(row = 5, column = 2, pady = 10)

            self.textAfter2 = ttk.Label(self, text = "PO verze:", background = "white", font = "helvetica 15")
            self.textAfter2.grid(row = 6, column = 1, pady = 10, sticky = E, padx = 10)
            self.entryAfter2 = ttk.Entry(self, textvariable = self.checkVar4, width = 7, justify = "right",
                                font = "helvetica 15", validate = "key", validatecommand = self.vcmd4)
            self.entryAfter2.grid(row = 6, column = 2, pady = 10)

            self.next.grid(row = 7, column = 1, columnspan = 2)        
            self.rowconfigure(7, weight = 1)
            self.rowconfigure(8, weight = 1)
            self.vars += [self.checkVar3, self.checkVar4]
        else:
            self.next.grid(row = 4, column = 1, columnspan = 2)            
            self.rowconfigure(5, weight = 1)

        self.next["state"] = "disabled"        

        self.text.grid(row = 1, column = 0, columnspan = 4)
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 0)
        self.rowconfigure(4, weight = 1)

        self.columnconfigure(2, weight = 0)
        self.columnconfigure(3, weight = 1)

    def onValidate(self, P, entry):
        try:
            float(P.replace(",", "."))
        except Exception:            
            if P != "":
                return False
        self.next["state"] = "!disabled"
        for i, var in enumerate(self.vars, 1):
            if i != int(entry):
                current = var.get().replace(",", ".")
            else:
                current = P.replace(",", ".")
            if current == "":
                self.next["state"] = "disabled"
            else:
                if float(current) >= 0 and float(current) <= 12:
                    continue           
                else:
                    self.next["state"] = "disabled"
        return True

    def write(self):
        self.file.write("Prediction\n")    
        self.file.write(self.id + "\t" + str(self.root.status["block"]) + "\t" + "\t".join([i.get() for i in self.vars]) + "\n\n")        
        if self.root.status["block"] == 3:
            if abs(float(self.checkVar1.get().replace(",", ".")) - BEFORE) <= 0.2 and abs(float(self.checkVar2.get().replace(",", ".")) - AFTER) <= 0.2:
                self.root.status["prediction"] = "correct"
            else:
                self.root.status["prediction"] = "incorrect"
 

class Wait(InstructionsFrame):
    def __init__(self, root, what = "voting"):
        super().__init__(root, text = wait_text, height = 3, font = 15, proceed = False, width = 45)
        self.what = what
        self.progressBar = ttk.Progressbar(self, orient = HORIZONTAL, length = 400, mode = 'indeterminate')
        self.progressBar.grid(row = 2, column = 1, sticky = N)

    def checkOffers(self):
        count = 0
        while True:
            self.update()
            if count % 50 == 0:
                data = urllib.parse.urlencode({'id': self.id, 'round': self.root.status["block"], 'offer': self.what})                
                data = data.encode('ascii')
                if URL == "TEST":
                    if self.what == "voting":
                        myvote = 1 if self.root.status["TESTvote"] == "treatment" else 0                        
                        othervote1 = random.randint(0, 1)
                        othervote2 = random.randint(0, 1)                        
                        response = "treatment" if myvote + othervote1 + othervote2 > 1 else "control"        
                    elif self.what == "result":
                        response = "result"
                        outcome1 = random.randint(0,12)   
                        outcome2 = random.randint(0,12)   
                        reward1 = ceil((250 - (1.5 * outcome1) * (outcome1 + 1))*self.root.status["coefficient"] / 2)  
                        reward2 = ceil((250 - (1.5 * outcome2) * (outcome2 + 1))*self.root.status["coefficient"] / 2) 
                        otherReward = 0
                        if self.root.status["block"] >= 3:
                            if self.root.status["block"] == self.root.status["otherWin1"]:
                                otherReward += reward1
                            if self.root.status["block"] == self.root.status["otherWin2"]:
                                otherReward += reward2                        
                        response += "_" + str(reward1 + reward2) + "_" + str(otherReward)
                        response += "_True"
                else:
                    try:
                        with urllib.request.urlopen(URL, data = data) as f:
                            response = f.read().decode("utf-8")       
                    except Exception as e:
                        continue
                if response:              
                    if self.what == "voting":
                        condition = response
                        self.root.status["conditions"].append(condition)
                        self.root.texts["voted_condition"] = after_voted if condition == "treatment" else before_voted
                        self.write(response)
                    elif self.what == "result":   
                        if not response.endswith("True"):
                            continue
                        else:
                            block = str(self.root.status["block"])
                            fromOthers = response.split("_")[1]
                            if not "fromOthers" in self.root.status:
                                self.root.status["fromOthers"] = int(response.split("_")[2])
                            else:
                                self.root.status["fromOthers"] += int(response.split("_")[2])                            
                            if self.root.status["block"] == 5:
                                self.root.status["reward"] += self.root.status["fromOthers"]
                                self.root.status["results"] += [additional.format(self.root.status["fromOthers"])]
                            self.root.texts["information" + block] = from_others_text.format(fromOthers) if self.root.status["information"] == "yes" else ""                  
                    self.progressBar.stop()
                    self.nextFun()  
                    return
            count += 1
            sleep(0.1)

    def run(self):
        self.progressBar.start()
        self.checkOffers()

    # def updateResults(self, maxvotes, votes):                
    #     if maxvotes == self.root.status["number"]:
    #         self.root.texts["voting_result_text"] = voting_you + members[int(votes) - 1]
    #     else:
    #         self.root.texts["voting_result_text"] = voting_other.format(maxvotes) + members[int(votes) - 1]

    def write(self, response):
        self.file.write("Voting Result" + "\n")
        self.file.write(self.id + "\t" + str(self.root.status["block"]) + "\t" + response + "\n\n")        







class Instructions3Check(InstructionsAndUnderstanding):
    def __init__(self, root):

        self.controlTexts = controlTexts3[0]
        self.update_intro(root.status["condition"], root)
        text = root.texts["introtext"]

        super().__init__(root, text = text, controlTexts = [self.controlTexts], name = "Cheating Round 3 Control Questions", height = 25, width = 110)

        ttk.Style().configure("TButton", font = "helvetica 15", width = 16)
 
    def update_intro(self, condition, root):   
        conditionText = {"low": condition_text.format(str(COEFFICIENTS[0]).replace(".", ",")), "high": condition_text.format(str(COEFFICIENTS[2]).replace(".", ",")), "control": ""}[condition]
        root.texts["conditionText"] = conditionText       
        otherRewards = ["{num: >4} ".format(num = ceil((250 - (1.5 * i) * (i + 1))*root.status["coefficient"] / 2)) for i in range(13)]        
        coef = str(root.status["coefficient"]).replace(".", ",")
        if coef != "1":
             coefText  = " × {} = {} Kč".format(coef, int(otherRewards[6])*2)
        else:
             coefText = ""
        root.texts["introtext"] = intro_block_3.format(conditionText, *otherRewards, coefText, otherRewards[6].strip())
        self.controlTexts[1][0] = self.controlTexts[1][0].format(108)
        self.controlTexts[1][1] = self.controlTexts[1][1].format(otherRewards[8].strip())
        self.controlTexts[1][2] = self.controlTexts[1][2].format(216)
        self.controlTexts[1][3] = self.controlTexts[1][3].format(int(otherRewards[8].strip()) * 2)
        explanation = explanation3.format(int(otherRewards[8].strip()), int(otherRewards[8].strip()), int(otherRewards[8].strip()) * 2)
        self.controlTexts[2] = [i.format(explanation) for i in self.controlTexts[2]]





controlTexts1 = [[intro_control1, intro_answers1, intro_feedback1], [intro_control2, intro_answers2, intro_feedback2]]
controlTexts3 = [[q3, answers3, feedback3]]
controlTexts4 = [[q4, answers4, feedback4]]

Instructions1 = (InstructionsAndUnderstanding, {"text": intro_block_1, "height": "auto", "width": 110, "fillerHeight": 1, "name": "Cheating Instructions Control Questions", "randomize": False, "controlTexts": controlTexts1})
Instructions2 = (InstructionsFrame, {"text": intro_block_2, "height": "auto", "update": ["win1"]})
Instructions3 = (Selection, {"text": "", "height": "auto", "width": 110})
Instructions4Check = (InstructionsAndUnderstanding, {"text": intro_block_4, "update": ["win3", "otherwin3", "conditionText"], "height": "auto", "width": 80, "fillerHeight": 1, "name": "Cheating Round 4 Control Questions", "randomize": False, "controlTexts": controlTexts4})
Instructions4 = (Selection, {"text": choice_fourth, "update": ["conditionText"], "height": "auto"})
Instructions5 = (Selection, {"text": intro_block_5, "update": ["win4", "otherwin4", "information4", "conditionText"], "height": "auto"})
ConditionInformation = (InstructionsFrame, {"text": info_condition, "update": ["voted_condition"]})

#Instructions3Check = (InstructionsAndUnderstanding, {"text": intro_block_3, "height": 35, "width": 110, "name": "Cheating Round 3 Control Questions", "update": ["win2", "condition", "source"], "controlTexts": controlTexts3})
EndCheating = (InstructionsFrame, {"text": endtext, "height": "auto", "update": ["win5", "otherwin5"]})
OutcomeWait = (Wait, {"what": "result"})


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Login,
         Instructions1,
         Cheating,
         Instructions2,
         Cheating,
         Prediction,
         Instructions3Check,
         Instructions3,         
         Cheating,
         OutcomeWait, 
         Instructions4Check,
         Instructions4,
         Prediction,
         Wait,
         ConditionInformation,
         Cheating,         
         OutcomeWait,
         Instructions5,
         Prediction,
         Wait,
         ConditionInformation,
         Cheating,     
         OutcomeWait,  
         EndCheating
         ])
