#! python3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import perf_counter, sleep
from collections import defaultdict

import random
import os
import urllib.request
import urllib.parse

from common import ExperimentFrame, InstructionsFrame, Measure, MultipleChoice
from gui import GUI
from debriefcheating import DebriefCheating
from constants import MAX_BDM_PRIZE, TESTING, URL, CONDITION_LOW, CONDITION_HIGH


################################################################################
# TEXTS

continuetext = "Pokračovat"
oddtext = "Liché (1, 3 nebo 5)"
eventext = "Sudé (2, 4 nebo 6)"
rolltext = "Hodit kostkou"
correcttext = "Správně"
incorrecttext = "Špatně"    
predictiontext = "Zvolil/a jsem, jestli na kostce padne liché nebo sudé číslo"

treatmenttext = '''Kolo {}

Máte za úkol uhodnout, zda na kostce padne liché nebo sudé číslo. Nyní prosím zvolte, zda v následujícím hodě padne liché nebo sudé číslo, zapamatujte si svoji volbu a poté klikněte na tlačítko Hodit kostkou.
'''

treatmenttext2 = "Zvolte, zda jste hádali správně a vydělali v tomto kole {} Kč nebo zda jste hádali špatně a nevydělali jste v tomto kole nic."

controltext = """Kolo {}

Máte za úkol uhodnout, zda na kostce padne liché nebo sudé číslo. Nyní prosím zvolte, zda v následujícím hodě padne liché nebo sudé číslo, a poté klikněte na tlačítko Hodit kostkou.
"""

controltext2 = "V tomto kole byla vaše předpověď {}"
wintext = "správná a vydělali jste {} Kč."
losstext = "špatná a nevydělali jste možných {} Kč."


# buttons
controlchoicetext = "verze PŘED"
treatmentchoicetext = "verze PO"  

intro_BDM = f"""
Toto je konec {{}} bloku o dvanácti kolech. Pokud bude tento blok vylosován, obdržíte {{}} Kč a Vámi vybraná charita {{}} Kč.

Jak jste zaznamenali, úkol měl dvě verze:

<b>Verzi “PŘED”</b>, ve které činíte předpovědi před hodem kostkou. Po zvolení možnosti vidíte výsledek hodu a dozvíte se, zda jste uhodli či nikoliv, a kolik jste vydělali.
<b>Verzi “PO”</b>, ve které uvádíte, zda jste uhodli či nikoliv a kolik jste vydělali, až poté, co vidíte výsledek hodu kostkou.

Nyní vás čeká třetí blok s dvanácti pokusy. Pro tento blok máte možnost zvolit si jednu z uvedených verzí. <b>Volba verze “PO” je ale zpoplatněna.</b> Zvolíte-li tuto verzi, bude zaplacená částka odečtena od výdělku v tomto bloku. Můžete si tedy zvolit jednu z následujících možností:
- verze PO se zpoplatněním
- verze PŘED bez poplatku.

V následujícím kole budete hrát jednu z verzí úlohy.
Za verzi "PO" je nutné zaplatit poplatek, jehož výše bude náhodně určena z intervalu od 1 do {MAX_BDM_PRIZE} Kč.
Do textového pole níže uveďte, kolik jste ochotni za hraní verze "PO" zaplatit.

Pokud tato částka bude vyšší nebo rovná náhodně vybrané velikosti poplatku, poplatek zaplatíte a budete hrát verzi "PO".

Pokud Vámi uvedená částka bude nižší než náhodně vybraná velikost poplatku, platit jej nebudete a budete hrát verzi "PŘED".

Nikdy nebudete platit více než, kolik je výše poplatku. I pokud uvedete, že jste ochotni zaplatit více, zaplatíte pouze výši poplatku. Je tedy pro vás rozumné uvést maximální cenu, kterou jste ochotni zaplatit. Nejvýše je možné uvést cenu {MAX_BDM_PRIZE} Kč.

Pokud uvedete hodnotu 0, budete určitě hrát verzi "PŘED". Pokud uvedete hodnotu {MAX_BDM_PRIZE}, budete určitě hrát verzi "PO".
"""


intro_BDM2 = f"""
Toto je konec {{}} bloku o dvanácti kolech. Pokud bude tento blok vylosován, obdržíte {{}} Kč a Vámi vybraná charita {{}} Kč.

Nyní vás čeká poslední blok s dvanácti pokusy. Pro tento blok máte opět možnost zvolit si jednu z uvedených verzí. <b>Volba verze “PO” je ale zpoplatněna.</b> Zvolíte-li tuto verzi, bude zaplacená částka odečtena od výdělku v tomto bloku. Můžete si tedy zvolit jednu z následujících možností:
- verze PO se zpoplatněním
- verze PŘED bez poplatku.

V následujícím kole budete hrát jednu z verzí úlohy.
Za verzi "PO" je nutné zaplatit poplatek, jehož výše bude náhodně určena z intervalu od 1 do {MAX_BDM_PRIZE} Kč.
Do textového pole níže uveďte, kolik jste ochotni za hraní verze "PO" zaplatit.

Pokud tato částka bude vyšší nebo rovná náhodně vybrané velikosti poplatku, poplatek zaplatíte a budete hrát verzi "PO".

Pokud Vámi uvedená částka bude nižší než náhodně vybraná velikost poplatku, platit jej nebudete a budete hrát verzi "PŘED".

Nikdy nebudete platit více než, kolik je výše poplatku. I pokud uvedete, že jste ochotni zaplatit více, zaplatíte pouze výši poplatku. Je tedy pro vás rozumné uvést maximální cenu, kterou jste ochotni zaplatit. Nejvýše je možné uvést cenu {MAX_BDM_PRIZE} Kč.

Pokud uvedete hodnotu 0, budete určitě hrát verzi "PŘED". Pokud uvedete hodnotu {MAX_BDM_PRIZE}, budete určitě hrát verzi "PO".
"""


bdm_result = """
Byl náhodně vybrán poplatek {} Kč. Byli jste ochotni zaplatit {} Kč. V následujícím kole tedy budete hrát verzi "{}" a {}.
"""

bdm_after = "z vaší výhry bude poplatek odečten"
bdm_before = "nezaplatíte žádný poplatek"

decisionText = "Nyní se rozhodněte, kolik jste ochotni zaplatit za verzi PŘED úlohy."
offerText = "Jsem ochoten/ochotna zaplatit:"

intro_auction = f"""
Toto je konec {{}} bloku o dvanácti kolech. Pokud bude tento blok vylosován, obdržíte {{}} Kč a Vámi vybraná charita {{}} Kč.

Před následujícím kolem byli všichni účastníci studie rozděleni do skupin o čtyřech lidech. Z každé skupiny bude v následujícím kole jeden hrát verzi "PO" a zbývající účastníci budou hrát verzi "PŘED".
Kdo z každé skupiny bude hrát verzi "PO" bude rozhodnuto na základě aukce. Všichni členové skupiny uvedou nabídku, kolik korun jsou ochotni zaplatit ze své výhry za to, aby hráli verzi "PO". Ten, který uvede nejvyšší částku bude hrát verzi "PO" a za tuto možnost zaplatí částku rovnou druhé nejvyšší nabídce ve skupině.
Ostatní členové skupiny budou hrát verzi "PŘED".
Nyní uveďte svou nabídku, kolik jste ochotní zaplatit za možnost hrát verzi "PO" úlohy. Nejvýše je možné nabídnout {MAX_BDM_PRIZE} Kč.
"""

auction_info = """
Hráč, který hrál verzi “PO” v minulém kole, uvedl, že správně uhodl {} hodů kostkou a vyhrál tedy {} Kč a charita ztratila z přiděleného příspěvku {} Kč.
"""

auction_prediction = 'Pokud nebudete hrát "PO" verzi úlohy Vy, kolik očekáváte,\nže nahlásí správných předpovědí člen týmu, který bude hrát verzi "PO"?'



block_numbers = ["prvního", "druhého", "třetího", "čtvrtého", "pátého", "šestého", "sedmého"]

wait_text = "Prosím počkejte na ostatní členy týmu."


auction_result = 'Za verzi "PO" jste nabídli {} Kč. {}.'


auction_after = 'Druhá nejvyšší nabídka byla {} Kč. Budete tedy hrát verzi "PO" a z Vaší výhry bude odečteno {} Kč'
auction_after_same = 'Druhá nejvyšší nabídka byla také {} Kč. Verze hry byly tedy mezi Vámi a členem skupiny, který nabídl stejnou částku, rozřazeny náhodně. Budete hrát verzi "PO" a z Vaší výhry bude odečteno {} Kč'
auction_before = 'Nejvyšší nabídka byla {} Kč. Budete tedy hrát verzi "PŘED" a nezaplatíte žádný poplatek'
auction_before_same = 'Druhá nejvyšší nabídka byla také {} Kč. Verze hry byly tedy mezi Vámi a členem skupiny, který nabídl stejnou částku, rozřazeny náhodně. Budete hrát verzi "PŘED" a nezaplatíte žádný poplatek'


intro_block_1 = """
V následujícím úkolu budete hádat, jestli na virtuální kostce (generátor náhodných čísel) na Vašem počítači padne liché nebo sudé číslo. Každé z čísel 1, 2, 3, 4, 5 a 6 může padnout se stejnou pravděpodobností. Lichá čísla jsou 1, 3 a 5. Sudá čísla jsou 2, 4 a 6. 

Úkol je rozdělen do sedmi samostatných bloků a každý blok sestává z dvanácti kol. V každém kole budete hádat výsledek jednoho hodu kostkou. Bloky se odlišují pravidly, dle nichž budete hádat hody kostkou. Po každém bloku bude krátká přestávka.

Uhodnete-li první hod v daném bloku, získáte 5 Kč, uhodnete-li další, získáte za něj dalších 10 Kč, uhodnete-li další hod, získáte za něj dalších 15 Kč a tak dále. Za každý další uhodnutý hod získáte navíc částku o 5 Kč vyšší, než byla předchozí odměna. Pokud tedy uhodnete všech 12 hodů v daném bloku, za poslední dvanáctý uhodnutý hod získáte 60 Kč a celkem získáte 390 Kč.

Charita, kterou jste dříve vybrali, obdrží na začátku experimentu 100 Kč. Pokud uhodnete v rámci jednoho bloku správně 10 hodů, charita ztratí {} Kč z tohoto počátečního příspěvku. Pokud uhodnete 11 hodů, charita ztratí dalších {} Kč. Pokud uhodnete správně všech 12 hodů v rámci jednoho bloku, charita ztratí dalších {} Kč. Charita tedy z počátečního příspěvku může ztratit až {} Kč ({}+{}+{}). Když je ztráta vyšší než počáteční příspěvek, který charita obdržela díky Vaší volbě, tato ztráta se odečte z příspěvků, které obdrží od ostatních účastníků výzkumu.

Poté, co dokončíte všech sedm bloků, bude jeden blok náhodně vylosován. Obdržíte peníze, které jste vydělali pouze v tomto vylosovaném bloku. Charita taktéž ztrácí peníze z počátečního příspěvku jen dle počtu správně uhodnutých hodů v rámci tohoto vylosovaného bloku. Pokud správně uhodnete všech dvanáct hodů v daném bloku, a tento blok bude později vylosován, obdržíte 390 Kč a charita ztratí ze svého počátečního příspěvku 300 Kč. Vaše výsledky v ostatních blocích nijak neovlivní množství peněz, které obdržíte Vy nebo Vámi vybraná charita.

Abychom ověřili, že rozumíte instrukcím, prosím odpovězte na následující otázku:
Když správně uhodnete 7 hodů z 12 v prvním bloku, 5 hodů z 12 ve druhém bloku, 2 hody z 12 ve třetím bloku a 8 hodů ve čtvrtém a pátém bloku, 4 hody v šestém bloku a 11 hodů v sedmém bloku a poté je vylosován třetí blok, kolik peněz obdržíte?
"""

wrong_answer = "{} Kč je chybná odpověď, správná odpověď je 15 Kč. Byl vylosován třetí blok, ve kterém jste správně uhodli 2 hody. Obdržíte tedy 5 + 10 = 15 Kč."
correct_answer = "15 Kč je správná odpověď. Byl vylosován třetí blok, ve kterém jste správně uhodli 2 hody. Obdržíte tedy 5 + 10 = 15 Kč."



intro_block_2 = """
Toto je konec prvního bloku. Pokud bude tento blok vylosován, obdržíte {} Kč a Vámi vybraná charita {} Kč. Nyní začne druhý blok s dvanácti koly.
"""

endtext = """Toto je konec posledního bloku. Pokud bude tento blok vybrán, obdržíte {} Kč a Vámi vybraná charita {} Kč.

Toto je konec úkolu s kostkou.
"""


BDMcontrol1 = "Zda budete hrát v následujícím kole verzi PŘED úlohy závisí na kterých faktorech:"
BDManswers1 = ["Náhodně vybrané částce a částce, kterou uvedete, že jste ochotni zaplatit",
"Náhodně vybrané částce a částce, kterou jsou ochotni zaplatit ostatní účastníci výzkumu",
"Částce, kterou uvedete, že jste ochotni zaplatit, a částce, kterou jsou ochotni zaplatit ostatní účastníci výzkumu"]
BDMfeedback1 = ["Ano, zda budete hrát v následujícím kole verzi PŘED úlohy závisí na tom, zda je částka, kterou uvedete, že jste ochotni zaplatit, vyšší než náhodně vybraná částka.", 
"Ne, zda budete hrát v následujícím kole verzi PŘED úlohy závisí na tom, zda je částka, kterou uvedete, že jste ochotni zaplatit, vyšší než náhodně vybraná částka.", 
"Ne, zda budete hrát v následujícím kole verzi PŘED úlohy závisí na tom, zda je částka, kterou uvedete, že jste ochotni zaplatit, vyšší než náhodně vybraná částka."]

BDMcontrol2 = "Pokud jste ochotni zaplatit až X Kč za to, že budete hrát verzi PŘED úlohy, tak platí, že:"
BDManswers2 = ["Se Vám vyplatí nabídnout částku nižší než X, neboť pak můžete zaplatit méně, než X.",
"Se Vám vyplatí nabídnout částku X, neboť pak budete hrát verzi PŘED, kdykoli bude náhodně vybraná částka nižší,\nnež nakolik si hraní verze PŘED ceníte, či stejná.",
"Se Vám vyplatí nabídnout částku vyšší, neboť to zvyšuje šanci, že budete hrát verzi PŘED."]
BDMfeedback2 = ["Ne, vyplatí se Vám nabídnout maximální částku, kterou jste ochotni zaplatit za hraní verze PŘED úlohy. Nikdy nebudete platit více než náhodně vybranou částku.",
"Ano, vyplatí se Vám nabídnout maximální částku, kterou jste ochotni zaplatit za hraní verze PŘED úlohy.",
"Ne, pokud nabídnete vyšší částku, může se stát, že zaplatíte za hraní verze PŘED úlohy více, než nakolik si ji ceníte."]

AuctionControl1 = "Zda budete hrát v následujícím kole verzi PŘED úlohy závisí na kterých faktorech:"
AuctionAnswers1 = ["Náhodně vybrané částce a částce, kterou uvedete, že jste ochotni zaplatit",
"Náhodně vybrané částce a částce, kterou jsou ochotni zaplatit ostatní účastníci výzkumu",
"Částce, kterou uvedete, že jste ochotni zaplatit, a částce, kterou jsou ochotni zaplatit ostatní účastníci výzkumu"]
AuctionFeedback1 = ["Ne, zda budete hrát v následujícím kole verzi PŘED úlohy závisí na tom, zda je částka, kterou uvedete, že jste ochotni zaplatit, vyšší než částka, kterou jsou ochotni zaplatit ostatní členové Vaší skupiny.",
"Ne, zda budete hrát v následujícím kole verzi PŘED úlohy závisí na tom, zda je částka, kterou uvedete, že jste ochotni zaplatit, vyšší než částka, kterou jsou ochotni zaplatit ostatní členové Vaší skupiny.",
"Ano, zda budete hrát v následujícím kole verzi PŘED úlohy závisí na tom, zda je částka, kterou uvedete, že jste ochotni zaplatit, vyšší než částka, kterou jsou ochotni zaplatit ostatní členové Vaší skupiny."]

AuctionControl2 = "Pokud jste ochotni zaplatit až X Kč za to, že budete hrát verzi PŘED úlohy, tak platí, že:"
AuctionAnswers2 = ["Se Vám vyplatí nabídnout částku nižší než X, neboť pak můžete zaplatit méně, než X.",
"Se Vám vyplatí nabídnout částku X, neboť pak budete hrát verzi PŘED, kdykoli bude částka nabídnutá ostatními\nčleny Vaší skupiny nižší než X.",
"Se Vám vyplatí nabídnout částku vyšší, neboť to zvyšuje šanci, že budete hrát verzi PŘED."]
AuctionFeedback2 = ["Ne, vyplatí se Vám nabídnout maximální částku, kterou jste ochotni zaplatit za hraní verze PŘED úlohy. Jinak je možné, že jiný člen Vaší skupiny zaplatí více než Vy, ale méně než X, a tudíž byste mohli hrát verzi PŘED za částku nižší než X, pokud byste ji nabídli.",
"Ano, vyplatí se Vám nabídnout maximální částku, kterou jste ochotni zaplatit za hraní verze PŘED úlohy.",
"Ne, pokud nabídnete vyšší částku, může se stát, že zaplatíte za hraní verze PŘED úlohy více, než nakolik si ji ceníte."]


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
        self.rewards = [i*5 + 5 for i in range(self.trials)]
        charityRewards = CONDITION_HIGH if "high" in self.root.status["condition"] else CONDITION_LOW
        self.charityRewards = [charityRewards[i-10] if i > 9 else 0 for i in range(self.trials)] 
        self.charityEndowment = 100
        #######################

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
        if not hasattr(self.root, "fees"):
            self.root.fees = defaultdict(int)

        self.responses = []


    def run(self):
        self.bottomText["state"] = "disabled"
        self.upperText["state"] = "disabled"
        if self.currentTrial < self.trials:
            self.currentTrial += 1
            self.startTrial()
        else:
            fee = self.root.fees[self.blockNumber]
            self.root.texts["win" + str(self.blockNumber)] = sum(self.rewards[:self.root.wins[self.blockNumber]]) - fee
            self.root.texts["charity" + str(self.blockNumber)] = sum(self.charityRewards[:self.root.wins[self.blockNumber]])  + self.charityEndowment
            if self.blockNumber == 7:
                win = random.randint(1, 7)
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
        fee = self.root.fees[self.blockNumber]
        self.infoWinnings["text"] = "Vaše současná výhra:\n{} Kč".format(sum(self.rewards[:self.root.wins[self.blockNumber]]) - fee)
        self.infoWinnings["text"] += "\n\nPříspěvek charitě:\n{} Kč".format(sum(self.charityRewards[:self.root.wins[self.blockNumber]]) + self.charityEndowment)

    def answer(self, answer = "NA"):
        t = perf_counter()
        if answer == "win":
            self.root.wins[self.blockNumber] += 1
        self.responses.append([self.blockNumber, self.currentTrial, self.condition, self.root.status["condition"],
                               self.currentRoll, self.response, answer, 
                               sum(self.rewards[:self.root.wins[self.blockNumber]]) - self.root.fees[self.blockNumber],
                               sum(self.charityRewards[:self.root.wins[self.blockNumber]]) + self.charityEndowment,
                               t - self.time, self.firstResponse - self.time,
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
        if self.blockNumber > 3 and self.blockNumber < 6:            
            wins = self.root.wins[self.blockNumber]
            reward = sum(self.rewards[:self.root.wins[self.blockNumber]])
            charity = sum(self.charityRewards[:self.root.wins[self.blockNumber]])
            outcome = "outcome_" + "_".join([str(wins), str(reward), str(charity)]) 
            while True:
                data = urllib.parse.urlencode({'id': self.id, 'round': self.blockNumber, 'offer': outcome})
                data = data.encode('ascii')
                if URL == "TEST":
                    self.root.texts["testOutcome"] = outcome                   
                    response = "ok"
                else:
                    try:
                        with urllib.request.urlopen(URL, data = data) as f:
                            response = f.read().decode("utf-8")       
                    except Exception:
                        pass
                if response:                    
                    super().nextFun()  
                    return            
                sleep(0.1)
        else:
            super().nextFun()  
    
    

class CheatingInstructions(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = root.texts["intro_block_1"], height = 31, font = 15, width = 100)

        self.checkVar = StringVar()
        self.vcmd = (self.register(self.onValidate), '%P')
        self.checkFrame = Canvas(self, background = "white", highlightbackground = "white",
                                 highlightcolor = "white")
        self.checkFrame.grid(row = 2, column = 1)
        self.entry = ttk.Entry(self.checkFrame, textvariable = self.checkVar, width = 10, justify = "right",
                               font = "helvetica 15", validate = "key", validatecommand = self.vcmd)
        self.entry.grid(row = 2, column = 1, padx = 6)
        self.currencyLabel = ttk.Label(self.checkFrame, text = "Kč", font = "helvetica 15",
                                       background = "white")
        self.currencyLabel.grid(row = 2, column = 2, sticky = NSEW)

        self.lowerText = Text(self, font = "helvetica 15", relief = "flat", background = "white",
                              width = 90, height = 3, wrap = "word", highlightbackground = "white")
        self.lowerText.grid(row = 3, column = 1, pady = 15)
        self.lowerText["state"] = "disabled"
        
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
            self.checked = True



class PaymentFrame(InstructionsFrame):
    def __init__(self, root, text, name, height = 10):
        # for testing
        if not "block" in root.status: 
            root.status["block"] = 1

        block_num = str(root.status["block"] - 1)
        root.texts["previousBlockText"] = block_numbers[root.status["block"] - 2]
        update = ["previousBlockText", "win" + block_num, "charity" + block_num]
        super().__init__(root, text = text, height = height, font = 15, width = 100, update = update)

        self.name = name

        # offer frame
        self.offerVar = StringVar()
        self.vcmd = (self.register(self.onValidate), '%P')
        self.offerFrame = Canvas(self, background = "white", highlightbackground = "white", highlightcolor = "white")
        self.filler1 = Canvas(self.offerFrame, background = "white", width = 1, height = 250,
                                highlightbackground = "white", highlightcolor = "white")
        self.filler1.grid(column = 1, row = 0, rowspan = 10, sticky = NS)
        if self.controlQuestions:
            self.decisionTextLab = ttk.Label(self.offerFrame, text = decisionText, font = "helvetica 15", background = "white")
            self.decisionTextLab.grid(row = 1, column = 0, columnspan = 3, pady = 10)        
        self.offerInnerFrame = Canvas(self.offerFrame, background = "white", highlightbackground = "white", highlightcolor = "white")
        self.offerInnerFrame.grid(row = 2, column = 0, columnspan = 3, sticky = EW)
        self.offerTextLab = ttk.Label(self.offerInnerFrame, text = offerText, font = "helvetica 15", background = "white")
        self.offerTextLab.grid(row = 2, column = 1, padx = 6, sticky = E)
        self.entry = ttk.Entry(self.offerInnerFrame, textvariable = self.offerVar, width = 10, justify = "right",
                               font = "helvetica 15", validate = "key", validatecommand = self.vcmd)
        self.entry.grid(row = 2, column = 2, sticky = E, padx = 5)
        self.currencyLabel = ttk.Label(self.offerInnerFrame, text = "Kč", font = "helvetica 15", background = "white")
        self.currencyLabel.grid(row = 2, column = 3, sticky = W)
        self.offerInnerFrame.columnconfigure(0, weight = 1)
        self.offerInnerFrame.columnconfigure(4, weight = 1)
        
        self.problem = ttk.Label(self.offerFrame, text = "", font = "helvetica 15", background = "white", foreground = "red")
        self.problem.grid(row = 4, column = 0, columnspan = 3, pady = 10)

        # control question frame
        self.controlFrame = Canvas(self, background = "white", highlightbackground = "white",
                                 highlightcolor = "white")
        self.filler2 = Canvas(self.controlFrame, background = "white", width = 1, height = 250,
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
        if self.controlQuestions and self.controlNum < len(self.controlTexts):            
            self.createControlQuestion()            
            self.controlFrame.grid(row = 2, column = 1)
        else:
            self.controlFrame.grid_forget()
            self.offerFrame.grid(row = 2, column = 1)

    def createControlQuestion(self):
        if self.controlNum:
            self.controlQuestion.grid_forget()
        texts = self.controlTexts[self.controlNum]
        self.controlQuestion = MultipleChoice(self.controlFrame, text = texts[0], answers = texts[1], feedback = texts[2])
        self.controlQuestion.grid(row = 0, column = 0)
        self.controlNum += 1        

    def onValidate(self, P):
        try:
            if "," in P or "." in P:
                raise ValueError()            
            if "-" in P:
                raise Exception("Nabídka musí být vyšší než 0 Kč.")
            offer = int(P)
            if offer < 0:
                raise Exception("Nabídka musí být vyšší než 0 Kč.")
            elif offer > MAX_BDM_PRIZE:
                raise Exception("Nabídka nesmí být vyšší než {} Kč.".format(MAX_BDM_PRIZE))
            else:
                self.next["state"] = "!disabled"
                self.problem["text"] = ""
        except ValueError:
            self.next["state"] = "disabled"
            self.problem["text"] = "Do textového pole je potřeba uvést celé číslo."
        except Exception as e:
            self.next["state"] = "disabled"
            self.problem["text"] = e
        return True
  
    def write(self):
        self.file.write("\n" + self.name + "\n")
        self.file.write(self.id + "\t" + str(self.root.status["block"]) + "\t" + self.offerVar.get() + "\n\n")

    def nextFun(self):        
        if (not self.controlQuestions) or (self.controlNum == len(self.controlTexts) and self.offerVar.get()):
            self.write()
            super().nextFun()   
        else:
            self.file.write(self.id + "\t" + str(self.controlNum) + "\t" + self.controlQuestion.answer.get() + "\n")
            self.createQuestion()



class Auction(PaymentFrame):
    def __init__(self, root):
        if "info" in root.status["condition"] and root.status["block"] > 4 and root.status["conditions"][root.status["block"]-2] != "treatment":
            if int(root.texts["outcome"].split("_")[1]) == -99:
                text = intro_auction    
            else:
                text = intro_auction + auction_info.format(*root.texts["outcome"].split("_")[1:4])
        else:
            text = intro_auction

        self.controlQuestions = root.status["block"] == 4
        self.controlTexts = [[AuctionControl1, AuctionAnswers1, AuctionFeedback1], [AuctionControl2, AuctionAnswers2, AuctionFeedback2]]

        super().__init__(root, text = text, name = "Auction", height = 15)

        if self.controlQuestions:
            self.file.write("Auction Control Questions" + "\n")

        self.state = "bid"

        self.predictionVar = StringVar()
        self.vcmd2 = (self.register(self.onValidatePrediction), '%P')
        self.predictionFrame = Canvas(self.offerFrame, background = "white", highlightbackground = "white",
                                 highlightcolor = "white")
        self.predictionFrame.grid(row = 3, column = 0, columnspan = 3, pady = 20, sticky = EW)
        self.predictionTextLab = ttk.Label(self.predictionFrame, text = auction_prediction, font = "helvetica 15", background = "white", foreground = "white")
        self.predictionTextLab.grid(row = 1, column = 0, padx = 6, sticky = E)
        self.predictionEntry = ttk.Entry(self.predictionFrame, textvariable = self.predictionVar, width = 10, justify = "right",
                                font = "helvetica 15", validate = "key", validatecommand = self.vcmd2)
        self.predictionEntry.grid(row = 1, column = 1, padx = 10)
        self.predictionEntry.grid_remove()


    def onValidatePrediction(self, P):
        try:
            if "," in P or "." in P:
                raise ValueError()            
            if "-" in P:
                raise Exception("Není možné správně odhadnout záporné množství hodů.")
            offer = int(P)
            if offer < 0:
                raise Exception("Není možné správně odhadnout záporné množství hodů.")
            elif offer > 12:
                raise Exception("Není možné odhadnout správně více než 12 hodů.")
            else:
                self.next["state"] = "!disabled"
                self.problem["text"] = ""
        except ValueError:
            self.next["state"] = "disabled"
            self.problem["text"] = "Do textového pole je potřeba uvést celé číslo."
        except Exception as e:
            self.next["state"] = "disabled"
            self.problem["text"] = e
        return True

  
    def write(self):
        self.root.texts["auctionResponse"] = self.offerVar.get()

        self.file.write(self.name + "\n")
        self.file.write(self.id + "\t" + str(self.root.status["block"]) + "\t" + self.offerVar.get() + "\t" + self.predictionVar.get() + "\n\n")

        data = urllib.parse.urlencode({'id': self.id, 'round': self.root.status["block"], 'offer': self.offerVar.get()})
        data = data.encode('ascii')
        if URL != "TEST":
            for i in range(60):                
                with urllib.request.urlopen(URL, data = data) as f:
                    if f.getcode() != 200 or f.read().decode("utf-8").strip() != "ok":
                        self.root.config(cursor = "wait")
                        self.root.update()
                        sleep(1)
                    else:
                        self.root.config(cursor = "")
                        break
            else:
                messagebox.showinfo(message = "Zavolejte prosím experimentátora.", icon = "error", parent = self.root, 
                                  detail = "Pravděpodobně je problém se serverem.", title = "Problém")
        else:
            self.root.status["TESTauction"] = self.offerVar.get()


    def nextFun(self):
        if self.state == "bid" and ((not self.controlQuestions) or (self.controlNum == len(self.controlTexts) and self.offerVar.get())):
            self.state = "prediction"
            self.entry["state"] = "disabled"
            self.next["state"] = "disabled"
            self.predictionTextLab["foreground"] = "black"
            self.predictionEntry.grid(row = 1, column = 1, padx = 10)
        else:
            super().nextFun()



class BDM(PaymentFrame):
    def __init__(self, root):
        if (not "block" in root.status) or root.status["block"] == 3:
            self.controlQuestions = True
            text = intro_BDM  
        else: 
            self.controlQuestions = False
            text = intro_BDM2        

        self.controlTexts = [[BDMcontrol1, BDManswers1, BDMfeedback1], [BDMcontrol2, BDManswers2, BDMfeedback2]]

        super().__init__(root, text = text, name = "BDM", height = 30)

        if self.controlQuestions:
            self.file.write("BDM Control Questions" + "\n")

    def write(self):        
        fee = self.root.status["bdm1"] if self.root.status["block"] == 3 else self.root.status["bdm2"]
        if int(self.offerVar.get()) >= fee:
            condition = "after"
            self.root.texts["bdmVersion"] = "PO"
            self.root.texts["bdmPaymentText"] = bdm_after
            self.root.status["conditions"].append("treatment")
            self.root.fees[self.root.status["block"]] = fee
        else:
            condition = "before"
            self.root.texts["bdmVersion"] = "PŘED"
            self.root.texts["bdmPaymentText"] = bdm_before
            self.root.status["conditions"].append("control")
        self.root.texts["bdmFee"] = fee
        self.root.texts["bdmResponse"] = int(self.offerVar.get())                

        super().write()


class Wait(InstructionsFrame):
    def __init__(self, root, what = "auction"):
        super().__init__(root, text = wait_text, height = 3, font = 15, proceed = False, width = 45)
        self.what = what
        self.progressBar = ttk.Progressbar(self, orient = HORIZONTAL, length = 400, mode = 'indeterminate')
        self.progressBar.grid(row = 2, column = 1, sticky = N)

    def checkOffers(self):
        count = 0
        while True:
            self.update()
            if count % 50 == 0:
                if self.what == "auction":
                    data = urllib.parse.urlencode({'id': self.id, 'round': self.root.status["block"], 'offer': "result"})
                elif self.what == "outcome":
                    data = urllib.parse.urlencode({'id': self.id, 'round': self.root.status["block"], 'offer': "outcome"})
                data = data.encode('ascii')
                if URL == "TEST":
                    if self.what == "auction":
                        myoffer = int(self.root.status["TESTauction"])
                        offers = [myoffer, random.randint(1,MAX_BDM_PRIZE), random.randint(1,MAX_BDM_PRIZE), random.randint(1,MAX_BDM_PRIZE)]
                        maxoffer = max(offers)
                        offers.sort()
                        secondoffer = offers[2]
                        condition = "treatment" if myoffer == maxoffer else "control"
                        response = "|".join([condition, str(maxoffer), str(secondoffer), str(myoffer)])
                    elif self.what == "outcome":
                        if self.root.status["conditions"][self.root.status["block"]-2] == "treatment":
                            response = self.root.texts["testOutcome"] + "_True"
                        else:
                            charity = -25 if "low" in self.root.status["condition"] else -100
                            response = "outcome_{}_{}_{}_True".format(10, 275, charity)
                else:
                    try:
                        with urllib.request.urlopen(URL, data = data) as f:
                            response = f.read().decode("utf-8")       
                    except Exception:
                        pass
                if response:
                    if self.what == "auction":
                        condition, maxoffer, secondoffer, myoffer = response.split("|")           
                        self.root.status["conditions"].append(condition)
                        sameoffers = myoffer == maxoffer and myoffer == secondoffer
                        self.updateResults(maxoffer, secondoffer, condition, sameoffers)
                        self.write(response)
                    elif self.what == "outcome":
                        _, wins, reward, charity, completed = response.split("_")
                        if completed != "True":
                            continue
                        else:
                            self.root.texts["outcome"] = response
                    self.progressBar.stop()
                    self.nextFun()  
                    return
            count += 1
            sleep(0.1)

    def run(self):
        self.progressBar.start()
        self.checkOffers()

    def updateResults(self, maxoffer, secondoffer, nextCondition, sameoffers):        
        if not hasattr(self.root, "fees"):
            self.root.fees = defaultdict(int)
        if nextCondition == "treatment":
            self.root.fees[self.root.status["block"]] = int(secondoffer)
            if sameoffers:
                self.root.texts["auctionText"] = auction_after_same.format(secondoffer, secondoffer)
            else:
                self.root.texts["auctionText"] = auction_after.format(secondoffer, secondoffer)
        else:
            if sameoffers:
                self.root.texts["auctionText"] = auction_before_same.format(maxoffer)   
            else:
                self.root.texts["auctionText"] = auction_before.format(maxoffer)           

    def write(self, response):
        self.file.write("Auction Result" + "\n")
        self.file.write(self.id + "\t" + str(self.root.status["block"]) + "\t" + response.replace("|", "\t") + "\n\n")          
            

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
                    response = "_".join(["start", str(random.randint(1,MAX_BDM_PRIZE)), str(random.randint(1,MAX_BDM_PRIZE)), random.choice(["lowinfo", "highinfo", "lowcontrol", "highcontrol"])])
                else:
                    response = ""
                    try:
                        with urllib.request.urlopen(URL, data = data) as f:
                            response = f.read().decode("utf-8") 
                    except Exception:
                        self.changeText("Server nedostupný")
                if "start" in response:
                    info, bdm1, bdm2, condition = response.split("_")                    
                    self.root.status["bdm1"] = int(bdm1)
                    self.root.status["bdm2"] = int(bdm2)
                    self.root.status["condition"] = condition
                    self.update_intro(condition)
                    self.progressBar.stop()
                    self.write(response)
                    self.nextFun()                      
                    break
                elif response == "login_successful" or response == "already_logged":
                    self.changeText("Přihlášen")
                elif response == "ongoing":
                    self.changeText("Do studie se již nelze připojit")
                elif response == "no_open":
                    self.changeText("Studie není otevřena")
                elif response == "closed":
                    self.changeText("Studie je uzavřena pro přihlašování")
                elif response == "not_grouped":
                    self.changeText("Nebyla Vám přiřazena žádná skupina") # TO DO
                #elif frame in response:
                    #pass # to do?
            count += 1                  
            sleep(0.1)        

    def run(self):
        self.progressBar.start()
        self.login()

    def update_intro(self, condition):        
        loss = CONDITION_HIGH if "high" in condition else CONDITION_LOW
        self.root.texts["intro_block_1"] = intro_block_1.format(loss[0], loss[1], loss[2], sum(loss), loss[0], loss[1], loss[2])

    def write(self, response):
        self.file.write("Login" + "\n")
        self.file.write(self.id + "\t" + response.replace("_", "\t") + "\n\n")        





Instructions2 = (InstructionsFrame, {"text": intro_block_2, "height": 5, "update": ["win1", "charity1"]})
BDMResult = (InstructionsFrame, {"text": bdm_result, "height": 3, "update": ["bdmFee", "bdmResponse", "bdmVersion", "bdmPaymentText"]})
AuctionResult = (InstructionsFrame, {"text": auction_result, "height": 3, "update": ["auctionResponse", "auctionText"]})
EndCheating = (InstructionsFrame, {"text": endtext, "height": 5, "update": ["win7", "charity7"]})
AuctionWait = (Wait, {"what": "outcome"})




if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Login,
         CheatingInstructions,
         Cheating,
         Instructions2,
         Cheating,
         BDM,
         BDMResult,
         Cheating,
         Auction,
         Wait,
         AuctionResult,
         Cheating,
         AuctionWait,
         Auction,
         Wait,
         AuctionResult,
         Cheating,
         AuctionWait,
         Auction,
         Wait,
         AuctionResult,
         Cheating,
         BDM,
         BDMResult,
         Cheating,
         EndCheating,
         DebriefCheating
         ])
