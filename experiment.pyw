#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

#from quest import QuestInstructions #, Hexaco
from intros import Initial, Intro, Ending#, HEXACOintro
from demo import Demographics
from cheating import Instructions1, Cheating, Instructions2, Wait, Instructions3, Instructions4, Instructions5, ConditionInformation
from cheating import EndCheating, Login, Prediction, OutcomeWait#, VotingResult, Perception, Debrief, FinalWait
from lottery import Lottery, LotteryWin
from dicelottery import LotteryInstructions, DiceLottery
#from questionnaire import TEQ, RSMS, HEXACOinfo, PoliticalWill
#from tosca import TOSCA

frames = [Initial,
          Intro,
          Login,
          Instructions1,
          Cheating,
          Instructions2,
          Cheating,
          Prediction,
          Instructions3,         
          Cheating,
          OutcomeWait, 
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
          #QuestInstructions,
          #RSMS,
          #TEQ,
          #TOSCA,
          #PoliticalWill,
          #HEXACOinfo,
          Demographics,
          Ending
         ]

#frames = [Login, HEXACOinfo]

if __name__ == "__main__":
    GUI(frames, load = os.path.exists("temp.json"))