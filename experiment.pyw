#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from quest import Hexaco, QuestInstructions
from intros import Intro, Ending
from demo import Demographics
from cheating import Instructions1, Cheating, Instructions2, BDM, BDMResult, Auction, Wait
from cheating import AuctionResult, EndCheating, Login
from debriefcheating import DebriefCheating
from debriefing import Debriefing
from lottery import Lottery, LotteryInstructions
from charity import Charity


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
          Auction,
          Wait,
          AuctionResult,
          Cheating,
          Auction,
          Wait,
          AuctionResult,
          Cheating,
          BDM,
          BDMResult,
          Cheating,
          EndCheating,
          LotteryInstructions,
          Lottery,
          QuestInstructions,
          Hexaco,
          Demographics,
          DebriefCheating,
          Debriefing,
          Ending
         ]


GUI(frames)
