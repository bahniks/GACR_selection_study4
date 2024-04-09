import os

studies = ["Login",
           "Cheating Instructions Control Questions",
           "Cheating 1",
           "Cheating 2",
           "Cheating Round 3 Control Questions",
           "Cheating 3",
           "Voting",
           "Perception",
           "Voting Result",
           "Cheating 4",
           "Debrief",
           "Pairing",
           "Dictator Control Questions",
           "DictatorA", 
           "DictatorB",
           "Dictator Feelings1",
           "Dictator Expectation",
           "Dictator Results 1",
           "Dictator2",
           "Dictator Feelings2",
           "Dictator Results 2",
           "Lottery",
           "Dice Lottery",
           "RSMS",
           "TEQ",
           "TOSCA",
           "Political Will",           
           "Demographics",
           "Ending"
           ]


columns = {"Login": ("id", "source", "condition", "number_in_group", "winning_block", "hexaco_id"),
           "Cheating Instructions Control Questions": ("id", "item", "answer"),
           "Cheating 1": ("id", "block", "trial", "version", "source", "condition", "roll", "prediction", "report", "reward", "time", "time1", "time2"), 
           "Cheating 2": ("id", "block", "trial", "version", "source", "condition", "roll", "prediction", "report", "reward", "time", "time1", "time2"), 
           "Cheating Round 3 Control Questions": ("id", "item", "answer"),           
           "Cheating 3": ("id", "block", "trial", "version", "source", "condition", "roll", "prediction", "report", "reward", "time", "time1", "time2"),
           "Voting": ("id", "block", "vote"),  
           "Perception": ("id", "prediction_voted_report", "prediction_my_votes", "p1_honest", "p1_selfish", "p1_calculating", "p2_honest", "p2_selfish", "p2_calculating", "p3_honest", "p3_selfish", "p3_calculating", "me_honest", "me_selfish", "me_calculating"),
           "Voting Result": ("id", "block", "condition", "elected", "number_of_votes"),
           "Cheating 4": ("id", "block", "trial", "version", "source", "condition", "roll", "prediction", "report", "reward", "time", "time1", "time2"), 
           "Debrief": ("id", "wanted_elected", "believed_elected", "preference_strength", "decision_process", "strategy"),
           "Pairing": ("id", "pair", "role", "condition"),
           "Dictator Control Questions": ("id", "item", "answer"),
           "DictatorA": ("id", "round", "withdrawal"),
           "DictatorB": ("id", "withdrawal0", "response0", "message0", "money0", "withdrawal2", "response2", "message2", "money2", "withdrawal4", "response4", "message4", "money4", "withdrawal6", "response6", "message6", "money6", "withdrawal8", "response8", "message8", "money8", "withdrawal10", "response10", "message10", "money10"),
           "Dictator Feelings1": ("id", "feeling", "rating"),
           "Dictator Expectation": ("id", "expectation"),
           "Dictator Results 1": ("id", "pair", "withdrawal", "response", "message", "money"),
           "Dictator2": ("id", "round", "withdrawal"),
           "Dictator Feelings2": ("id", "feeling", "rating"),
           "Dictator Results 2": ("id", "pair", "withdrawal"),
           "Lottery": ("id", "choice1", "choice2", "choice3", "choice4", "choice5", "chosen", "win"),
           "Dice Lottery": ("id", "rolls", "reward"),
           "RSMS": ("id", "item", "answer"),
           "TEQ": ("id", "item", "answer"),
           "TOSCA": ("id", "number", "answer", "item"),  
           "Political Will": ("id", "item", "answer"),           
           "Demographics": ("id", "sex", "age", "language", "student", "field"),
           "Ending": ("id", "reward", "chosen_block")
           }

frames = ["Initial",
          "Login",
          "Intro",
          "HEXACOintro",
          "CheatingInstructions",
          "Cheating",
          "Instructions2",
          "Cheating",
          "Instructions3",
          "Cheating",
          "OutcomeWait",
          "Voting",
          "Perception",
          "Wait",
          "VotingResult",
          "Cheating",   
          "Debrief",    
          "FinalWait",
          "EndCheating",
          "WaitDictator",
          "InstructionsDictator",
          "DictatorDecision",
          "DictatorFeelings",
          "WaitResult1",
          "DictatorResult",
          "DictatorFeelings2",
          "WaitResult2",
          "DictatorEnd",
          "Lottery",
          "LotteryWin",
          "LotteryInstructions",
          "DiceLottery",
          "QuestInstructions",
          "RSMS",
          "TEQ",
          "TOSCA",
          "PoliticalWill",
          "HEXACOinfo",
          "Demographics",
          "Ending",
          "end"
         ]

for study in studies:
    with open("{} results.txt".format(study), mode = "w") as f:
        f.write("\t".join(columns[study]))

with open("Time results.txt", mode = "w") as times:
    times.write("\t".join(["id", "order", "frame", "time"]))

files = os.listdir()
for file in files:
    if ".py" in file or "results" in file or "file.txt" in file or "STATION" in file or ".txt" not in file:
        continue

    with open(file) as datafile:
        #filecount += 1 #
        count = 1
        for line in datafile:

            study = line.strip()
            if line.startswith("time: "):
                with open("Time results.txt", mode = "a") as times:
                    times.write("\n" + "\t".join([file, str(count), frames[count-1], line.split()[1]]))
                    count += 1
                    continue
            if study in studies:
                with open("{} results.txt".format(study), mode = "a") as results:
                    for line in datafile:
                        content = line.strip()
                        if not content or content.startswith("time: "):
                            break
                        else:
                            results.write("\n" + content)