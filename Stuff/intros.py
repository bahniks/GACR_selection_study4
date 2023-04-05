#! python3

import os

from common import InstructionsFrame
from gui import GUI

from constants import BONUS


################################################################################
# TEXTS
intro = """
Vítejte na výzkumné studii pořádané Fakultou podnikohospodářskou Vysoké školy ekonomické v Praze. Tato studie se skládá z několika různých úkolů a otázek. Níže je uveden přehled toho, co vás čeká:

1) Hod kostkou: vaším úkolem bude uhodnout, zda na kostce padne liché, nebo sudé číslo. Budete hádat v sedmi blocích, každém po dvanácti kolech. V tomto úkolu můžete vydělat peníze.
2) Loterie: můžete se rozhodnout zúčastnit se loterie s několika koly a získat další peníze v závislosti na vašich rozhodnutích a výsledcích loterie.
3) Dotazníky: budete odpovídat na otázky ohledně vašich vlastností a postojů. Dotazník zahrnuje položky, které kontrolují, zda otázkám věnujete pozornost. Pokud odpovíte na tyto kontroly pozornosti správně, získáte další peníze. 
4) Konec studie a platba: poté, co skončíte, půjdete do vedlejší místnosti, kde podepíšete pokladní dokument, na základě kterého obdržíte vydělané peníze v hotovosti. <b>Jelikož v dokumentu bude uvedena pouze celková suma, experimentátor nebude vědět, kolik jste vydělali v jednotlivých částech studie.</b>

Děkujeme, že jste vypnuli své mobilní telefony, a že nebudete s nikým komunikovat v průběhu studie. Pokud s někým budete komunikovat, nebo pokud budete nějakým jiným způsobem narušovat průběh studie, budete požádáni, abyste opustili laboratoř, bez nároku na vyplacení peněz.

V případě, že máte otázky nebo narazíte na technický problém během úkolů, zvedněte ruku a tiše vyčkejte příchodu výzkumného asistenta.

Nepokračujte prosím dokud vám výzkumný asistent nedá pokyn.
"""


czechending = """
V úloze s házením kostek byl náhodně vybrán blok {}. V úkolu s kostkou jste tedy vydělali {} Kč. V loterii jste vydělali {} Kč. {} jste správně na všechny kontroly pozornosti a tedy {} dalších {} Kč. Za účast na studii dostáváte 50 Kč. Vaše odměna za tuto studii je tedy dohromady {} Kč, zaokrouhleno na desítky korun nahoru získáváte {} Kč. Napište prosím tuto (zaokrouhlenou) částku společně s číslem vašeho místa - {} na papír na stole před vámi. 

Výsledky experimentu budou volně dostupné na stránkách Centrum laboratorního a experimentálního výzkumu FPH VŠE, krátce po vyhodnocení dat a publikaci výsledků. Žádáme vás, abyste nesdělovali detaily této studie možným účastníkům, aby jejich volby a odpovědi nebyly ovlivněny a znehodnoceny.
  
Můžete vzít všechny svoje věci, papír s číslem vašeho místa a uvedenou odměnou, a, aniž byste rušili ostatní účastníky, se odeberte za výzkumným asistentem, od kterého obdržíte svoji odměnu. 

Toto je konec experimentu. Děkujeme za vaši účast!
 
Centrum laboratorního a experimentálního výzkumu FPH VŠE
""" 


################################################################################


updates = ["block", "dice", "lottery_win", "attention1", "attention2", "bonus", "reward", "rounded_reward", "station"]



Intro = (InstructionsFrame, {"text": intro, "proceed": True, "height": 28})
Ending = (InstructionsFrame, {"text": czechending, "keys": ["g", "G"], "proceed": False, "height": 30,
                              "update": updates})



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Intro,
         Ending])
