#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from quest import QuestInstructions #, Hexaco
from intros import Initial, Intro, Ending, HEXACOintro
from demo import Demographics
from cheating import CheatingInstructions, Cheating, Instructions2, Wait, Voting
from cheating import EndCheating, Login, Instructions3, OutcomeWait, VotingResult, Perception, Debrief, FinalWait
from lottery import Lottery, LotteryWin
from dicelottery import LotteryInstructions, DiceLottery
from dictator import WaitDictator, InstructionsDictator, DictatorDecision, DictatorFeelings, WaitResult1, DictatorResult
from dictator import DictatorFeelings2, WaitResult2, DictatorEnd
from questionnaire import TEQ, RSMS, HEXACOinfo, PoliticalWill
from tosca import TOSCA

frames = [Initial,
          Login,
          Intro,
          HEXACOintro,
          CheatingInstructions,
          Cheating,
          Instructions2,
          Cheating,
          Instructions3,
          Cheating,
          OutcomeWait,
          Voting,
          Perception,
          Wait,
          VotingResult,
          Cheating,   
          Debrief,    
          FinalWait,
          EndCheating,
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
          RSMS,
          TEQ,
          TOSCA,
          PoliticalWill,
          HEXACOinfo,
          Demographics,
          Ending
         ]

#frames = [Login, HEXACOinfo]

if __name__ == "__main__":
    GUI(frames, load = os.path.exists("temp.json"))