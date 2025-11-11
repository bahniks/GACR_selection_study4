#! python3

import sys
import os
import argparse

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from quest import QuestInstructions, Hexaco
from intros import Initial, Intro, Ending
from demo import Demographics
from cheating import Instructions1, Cheating, Instructions2, Wait, Instructions3Check, Instructions3, Instructions4Check, Instructions4, Instructions5
from cheating import EndCheating, ConditionInformation, Login, Prediction, OutcomeWait, Choice5
from lottery import Lottery, LotteryWin
from dicelottery import LotteryInstructions, DiceLottery
from comments import Comments
from questionnaire import TDMS, TEQ, PoliticalWill
from tosca import TOSCA
from contribution import Contribution, WaitContribution
from dictator import WaitDictator, InstructionsDictator, DictatorDecision, DictatorFeelings, WaitResult1, DictatorResult, DictatorFeelings2, WaitResult2, DictatorEnd
from debriefing import DebriefCheating, DebriefingInstructions
#from svo import SVO

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
          Prediction,
          Instructions4,
          Wait,
          ConditionInformation,
          Cheating,         
          OutcomeWait,
          Instructions5,
          Prediction,
          Choice5,
          Wait,
          ConditionInformation,
          Cheating,     
          OutcomeWait,  
          EndCheating,
          DebriefingInstructions,
          DebriefCheating,
          Contribution,
          WaitDictator,
          InstructionsDictator,
          DictatorDecision,
          DictatorFeelings,
          WaitResult1,
          DictatorResult,
          DictatorFeelings2,
          WaitResult2,
          DictatorEnd,
          QuestInstructions,
          Hexaco,
          TDMS,
          TEQ,
          TOSCA,
          PoliticalWill,
          Lottery,
          LotteryWin,
          LotteryInstructions,
          DiceLottery,
          Demographics,
          Comments,
          WaitContribution,
          Ending
         ]

#frames = [Login, HEXACOinfo]


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run experiment')
    parser.add_argument('--load', type=str, default='True', help='Load previous session data')    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    if args.load == "False":
        load = False
    else:
        load = os.path.exists("temp.json")    
    
    GUI(frames, load=load)