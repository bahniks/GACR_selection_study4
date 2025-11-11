#! python3
from tkinter import *
from tkinter import ttk

import os
import urllib.request
import urllib.parse

from math import ceil
from time import sleep

from common import InstructionsFrame
from gui import GUI

from constants import BONUS, PARTICIPATION_FEE, URL, PREDICTION_BONUS
from cheating import Login


################################################################################
# TEXTS
login = """Vítejte na výzkumné studii pořádané Fakultou podnikohospodářskou Vysoké školy ekonomické v Praze! 

Za účast na studii obdržíte {} Kč. Kromě toho můžete vydělat další peníze v průběhu studie. 

Studie bude trvat cca 50-70 minut.

Děkujeme, že jste vypnuli své mobilní telefony, a že nebudete s nikým komunikovat v průběhu studie. Pokud s někým budete komunikovat, nebo pokud budete nějakým jiným způsobem narušovat průběh studie, budete požádáni, abyste opustili laboratoř, bez nároku na vyplacení peněz.

Pokud jste již tak neučinili, přečtěte si informovaný souhlas a pokud s ním budete souhlasit, podepište ho. 

Počkejte na pokyn experimentátora.""".format(PARTICIPATION_FEE)


intro = """Studie se skládá z několika různých úkolů a otázek. Níže je uveden přehled toho, co Vás čeká:
1) Hod kostkou: Vaším úkolem bude uhodnout, zda na kostce padne liché, nebo sudé číslo. Budete hádat v pěti blocích, v každém po dvanácti kolech. V tomto úkolu můžete vydělat peníze.
2) Dělení peněz: Budete se rozhodovat, jak dělit peníze v páru s jiným účastníkem studie. V tomto úkolu můžete vydělat peníze. 
3) Dotazníky: budete odpovídat na otázky ohledně Vašich vlastností a postojů. 
4) Loterie: můžete se rozhodnout zúčastnit se loterie a získat další peníze v závislosti na výsledcích loterie.
5) Konec studie a platba: poté, co skončíte, půjdete do vedlejší místnosti, kde podepíšete pokladní dokument, na základě kterého obdržíte vydělané peníze v hotovosti. <b>Jelikož v dokumentu bude uvedena pouze celková suma, experimentátor, který Vám bude vyplácet odměnu, nebude vědět, kolik jste vydělali v jednotlivých částech studie.</b>

Jelikož v průběhu studie interagujete s jinými účastníky, je možné, že v některých částech studie budete muset chvíli počkat, než se tito účastníci dostanou do stejného bodu studie. V takovém případě Vás požádáme o trpělivost a klidné vyčkání.

V případě, že máte otázky nebo narazíte na technický problém během úkolů, zvedněte ruku a tiše vyčkejte příchodu výzkumného asistenta.

Všechny informace, které v průběhu studie uvidíte, jsou pravdivé a nebudete za žádných okolností klamáni či jinak podváděni.

Po přečtení stiskněte tlačítko “Pokračovat”."""


ending = """Toto byl poslední úkol studie.
{}
Za účast na studii dostáváte {} Kč.
Vaše odměna za tuto studii je tedy dohromady {} Kč, zaokrouhleno na desítky korun nahoru <b>získáváte {} Kč. Napište prosím tuto (zaokrouhlenou) částku do pokladního dokladu na stole před Vámi.</b>

Výsledky experimentu budou volně dostupné na stránkách Centra laboratorního a experimentálního výzkumu FPH VŠE, krátce po vyhodnocení dat a publikaci výsledků. Žádáme Vás, abyste nesdělovali detaily této studie možným účastníkům, aby jejich volby a odpovědi nebyly ovlivněny a znehodnoceny.
  
Můžete si vzít všechny svoje věci, vyplněný pokladní doklad, a aniž byste rušili ostatní účastníky, odeberte se do vedlejší místnosti za výzkumným asistentem, od kterého obdržíte svoji odměnu. 

Toto je konec experimentu. Děkujeme za Vaši účast!
 
Decision Lab při FPH VŠE""" 

################################################################################




class Ending(InstructionsFrame):
    def __init__(self, root):
        root.texts["results"] = "\n" + "\n".join(root.status["results"]) + "\n"
        root.texts["reward"] = str(root.status["reward"])
        root.texts["rounded_reward"] = ceil(root.status["reward"] / 10) * 10
        root.texts["participation_fee"] = PARTICIPATION_FEE
        updates = ["results", "participation_fee", "reward", "rounded_reward"]
        super().__init__(root, text = ending, keys = ["g", "G"], proceed = False, height = "auto", update = updates, width = 100)
        self.file.write("Ending\n")
        self.file.write(self.id + "\t" + str(root.texts["rounded_reward"]) + "\n\n")

    def run(self):
        self.sendInfo()

    def sendInfo(self):
        while True:
            self.update()    
            data = urllib.parse.urlencode({'id': self.root.id, 'round': -99, 'offer': self.root.texts["rounded_reward"]})
            data = data.encode('ascii')
            if URL == "TEST":
                response = "ok"
            else:
                try:
                    with urllib.request.urlopen(URL, data = data) as f:
                        response = f.read().decode("utf-8") 
                except Exception:
                    pass
            if "ok" in response:                     
                break              
            sleep(5)

    def gothrough(self):
        self.run()
        super().gothrough()



Intro = (InstructionsFrame, {"text": intro, "proceed": True, "height": "auto"})
Initial = (InstructionsFrame, {"text": login, "proceed": False, "height": "auto", "keys": ["g", "G"]})


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Login,
         Initial, 
         Intro,
         Ending])
