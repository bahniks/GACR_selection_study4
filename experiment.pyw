#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from quest import Hexaco, QuestInstructions
from intros import Intro, Ending
from demo import Demographics
from cheating import Instructions1, Cheating, Instructions2, BDM, BDMResult, Auction, Wait
from cheating import AuctionResult, EndCheating, Login, AuctionWait
#from debriefcheating import DebriefCheating
from lottery import Lottery, LotteryWin
from charity import Charity
from questionnaire import Prosociality
from anchoring import AnchoringInstructions, Anchoring


frames = [Login,
          Intro,          
          Charity,
          Instructions1,
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
          Lottery,
          LotteryWin,
          AnchoringInstructions, 
          Anchoring,
          QuestInstructions,
          Hexaco,
          Prosociality,
          Demographics,
          #DebriefCheating, # ?
          #Debriefing, # ?
          Ending
         ]

if __name__ == "__main__":
    GUI(frames, load = os.path.exists("temp.json"))