import os

studies = ["Login",
           "Cheating Instructions Control Questions",
           "Cheating 1",
           "Cheating 2",
           "Prediction3",
           "Cheating Round 3 Control Questions",
           "Selection",
           "Cheating 3",
           "Cheating Round 4 Control Questions", 
           "Prediction4",
           "Voting Result",
           "Cheating 4",
           "Prediction5",
           "Cheating 5",
           "Debriefing1",
           "Pairing",
           "Dictator Control Questions",
           "DictatorA",
           "Dictator Feelings1",
           "Dictator Expectation",
           "Dictator Results 1",
           "Dictator2",
           "Dictator Feelings2",
           "Dictator Results 2",
           "Contribution",
           "Hexaco",
           "TDMS",
           "TEQ",
           "TOSCA",
           "Political Will",
           "Lottery",
           "Dice Lottery",
           "Demographics",
           "Comments",
           "Contribution Result",
           "Ending"
           ]


columns = {"Login": ("id", "condition", "information", "winning_block"),
           "Cheating Instructions Control Questions": ("id", "item", "answer"),
           "Cheating 1": ("id", "block", "trial", "version", "condition", "roll", "prediction", "report", "reward", "time", "time1", "time2"), 
           "Cheating 2": ("id", "block", "trial", "version", "condition", "roll", "prediction", "report", "reward", "time", "time1", "time2"), 
           "Prediction3": ("id", "block", "before", "after"),
           "Cheating Round 3 Control Questions": ("id", "item", "answer"),
           "Selection": ("id", "block", "selection"),           
           "Cheating 3": ("id", "block", "trial", "version", "condition", "roll", "prediction", "report", "reward", "time", "time1", "time2"),
           "Cheating Round 4 Control Questions": ("id", "item", "answer"),
           "Prediction4": ("id", "block", "before_others", "after_others", "before_self", "after_self"),
           "Voting Result": ("id", "block", "condition"),
           "Cheating 4": ("id", "block", "trial", "version", "condition", "roll", "prediction", "report", "reward", "time", "time1", "time2"), 
           "Prediction5": ("id", "block", "before_others", "after_others", "before_self", "after_self"),
           "Cheating 5": ("id", "block", "trial", "version", "condition", "roll", "prediction", "report", "reward", "time", "time1", "time2"),
           "Debriefing1": ("id", "third_process", "later_process"),
           "Pairing": ("id", "pair", "role"),
           "Dictator Control Questions": ("id", "item", "answer"),
           "DictatorA": ("id", "round", "withdrawal"),
           "DictatorB": ("id", "withdrawal0", "response0", "message0", "money0", "withdrawal2", "response2", "message2", "money2", "withdrawal4", "response4", "message4", "money4", "withdrawal6", "response6", "message6", "money6", "withdrawal8", "response8", "message8", "money8", "withdrawal10", "response10", "message10", "money10"),
           "Dictator Feelings1": ("id", "feeling", "rating"),
           "Dictator Expectation": ("id", "expectation"),
           "Dictator Results 1": ("id", "pair", "withdrawal", "response", "message", "money"),
           "Dictator2": ("id", "round", "withdrawal"),
           "Dictator Feelings2": ("id", "feeling", "rating"),
           "Dictator Results 2": ("id", "pair", "withdrawal"),
           "Contribution": ("id", "choice1", "choice2", "choice3", "choice4", "choice5", "choice6", "choice7", "chosen"),
           "Hexaco": ("id", "trial", "answer", "item"),
           "TDMS": ("id", "item", "answer"),
           "TEQ": ("id", "item", "answer"),
           "TOSCA": ("id", "number", "answer", "item"),  
           "Political Will": ("id", "item", "answer"),
           "Lottery": ("id", "choice1", "choice2", "choice3", "choice4", "choice5", "chosen", "win"),
           "Dice Lottery": ("id", "rolls", "reward"),           
           "Demographics": ("id", "sex", "age", "language", "student", "field"),
           "Comments": ("id", "comments"),
           "Contribution Result": ("id", "contributed"),
           "Ending": ("id", "reward")
           }

frames = ["Initial",
          "Intro",
          "Login",
          "Instructions1",
          "Cheating",
          "Instructions2",
          "Cheating",
          "Prediction",
          "Instructions3Check",
          "Instructions3",
          "Cheating",
          "OutcomeWait",
          "Instructions4Check",
          "Prediction",
          "Instructions4",
          "Wait",
          "ConditionInformation",
          "Cheating",
          "OutcomeWait",
          "Instructions5",
          "Prediction",
          "Choice5",
          "Wait",
          "ConditionInformation",
          "Cheating",
          "OutcomeWait",
          "EndCheating",
          "DebriefingInstructions",
          "DebriefCheating",
          "Contribution",
          "WaitDictator",
          "InstructionsDictator",
          "DictatorDecision",
          "DictatorFeelings",
          "WaitResult1",
          "DictatorResult",
          "DictatorFeelings2",
          "WaitResult2",
          "DictatorEnd",
          "QuestInstructions",
          "Hexaco",
          "TDMS",
          "TEQ",
          "TOSCA",
          "PoliticalWill",
          "Lottery",
          "LotteryWin",
          "LotteryInstructions",
          "DiceLottery",
          "Demographics",
          "Comments",
          "WaitContribution",
          "Ending",
          "end"
         ]

for study in studies:
    with open("{} results.txt".format(study), mode = "w", encoding="utf-8") as f:
        f.write("\t".join(columns[study]))

with open("Time results.txt", mode = "w", encoding="utf-8") as times:
    times.write("\t".join(["id", "order", "frame", "time"]))

files = os.listdir()
for file in files:
    if ".py" in file or "results" in file or "file.txt" in file or "STATION" in file or ".txt" not in file:
        continue

    with open(file, encoding="utf-8") as datafile:
        #filecount += 1 #
        count = 1
        for line in datafile:

            study = line.strip()
            if line.startswith("time: "):
                with open("Time results.txt", mode = "a", encoding="utf-8") as times:
                    times.write("\n" + "\t".join([file, str(count), frames[count-1], line.split()[1]]))
                    count += 1
                    continue
            if study in studies:
                with open("{} results.txt".format(study), mode = "a", encoding="utf-8") as results:
                    for line in datafile:
                        content = line.strip()
                        if not content or content.startswith("time: "):
                            break
                        else:
                            results.write("\n" + content)