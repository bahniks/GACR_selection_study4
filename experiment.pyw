#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from quest import QuestInstructions #, Hexaco
from intros import Initial, Intro, Ending
from demo import Demographics
from cheating import CheatingInstructions, Cheating, Instructions2, Wait, Voting
from cheating import EndCheating, Login, Instructions3, OutcomeWait, VotingResult
from debriefing import DebriefingInstructions, DebriefCheating1, DebriefCheating2, DebriefCheating3, DebriefCheating4
from lottery import Lottery, LotteryWin
from dicelottery import LotteryInstructions, DiceLottery
from dictator import WaitDictator, InstructionsDictator, DictatorDecision, DictatorFeelings, WaitResult1, DictatorResult
from dictator import DictatorFeelings2, WaitResult2, DictatorEnd
from questionnaire import TEQ
from tosca import TOSCA

frames = [Initial,
          Login,
          Intro,
          CheatingInstructions,
          Cheating,
          Instructions2,
          Cheating,
          Instructions3,
          Cheating,
          OutcomeWait,
          Voting,
          Wait,
          VotingResult,
          Cheating,         
          EndCheating    
          DebriefingInstructions,      
          DebriefCheating1,
          DebriefCheating2,
          DebriefCheating3,
          DebriefCheating4,
          WaitDictator,
          InstructionsDictator,
          DictatorDecision,
          DictatorFeelings,
          WaitResult1,
          DictatorResult,
          DictatorFeelings2,
          WaitResult2,
          DictatorEnd,
          Lottery,
          LotteryWin,
          LotteryInstructions,
          DiceLottery,
          QuestInstructions,
          TEQ,
          TOSCA,
          Demographics,
          Ending
         ]

if __name__ == "__main__":
    GUI(frames, load = os.path.exists("temp.json"))