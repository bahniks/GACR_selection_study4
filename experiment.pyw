#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from quest import QuestInstructions, Hexaco
from intros import Initial, Intro, Ending#, HEXACOintro
from demo import Demographics
from cheating import Instructions1, Cheating, Instructions2, Wait, Instructions3Check, Instructions3, Instructions4Check, Instructions4, Instructions5
from cheating import EndCheating, ConditionInformation, Login, Prediction, OutcomeWait#, VotingResult, Perception, Debrief, FinalWait
from lottery import Lottery, LotteryWin
from dicelottery import LotteryInstructions, DiceLottery
from comments import Comments
from questionnaire import TDMS

frames = [Initial,
          Intro,
          Login,
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
          EndCheating,
          Lottery,
          LotteryWin,
          LotteryInstructions,
          DiceLottery,
          QuestInstructions,
          Hexaco,
          TDMS,
          Demographics,
          Comments,
          Ending
         ]

#frames = [Login, HEXACOinfo]

if __name__ == "__main__":
    GUI(frames, load = os.path.exists("temp.json"))