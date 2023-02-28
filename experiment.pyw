#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from quest import Hexaco, QuestInstructions
from questionnaire import DarkTriad1, DarkTriad2
from intros import Intro, Ending
from demo import Demographics
from cheating import Instructions1, BlockOne, Instructions2, BlockTwo, Instructions3, BlockThree
from cheating import Instructions4, BlockFour, Estimate, Instructions5, BlockFive, EndCheating
from debriefcheating import DebriefCheating
from debriefing import Debriefing
from lottery import Lottery, LotteryInstructions


frames = [Intro,
          Instructions1,
          BlockOne,
          Instructions2,
          BlockTwo,
          Instructions3,
          BlockThree,
          Instructions4,
          BlockFour,
          Estimate,
          Instructions5,
          BlockFive,
          EndCheating,
          LotteryInstructions,
          Lottery,
          QuestInstructions,
          Hexaco,
          DarkTriad1,
          DarkTriad2,
          Demographics,
          DebriefCheating,
          Debriefing,
          Ending
         ]


GUI(frames)
