import os

studies = ["Login",
           "Cheating Instructions Control Questions",
           "Cheating 1",
           "Cheating 2",
           "Cheating Round 3 Control Questions",
           "Cheating 3",
           "Voting",
           "Perception",
           "Voting Results",
           "Cheating 4",
           "Debrief",
           "Pairing",
           "Dictator Control Questions",
           "DictatorA", # DictatorB
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
           # dodelano sem

           "Debriefing2": ("id", "bdm_reward", "bdm_charity_loss", "bdm_charity_loss_others", "bdm_others_bids", "bdm_others_prediction", "bdm_fun", "bdm_ease", "bdm_reward_influence", "bdm_charity_loss_influence", "bdm_winner", "bdm_overcome_others", "auction_reward", "auction_charity_loss", "auction_charity_loss_others", "auction_others_bids", "auction_others_prediction", "auction_fun", "auction_ease", "auction_reward_influence", "auction_charity_loss_influence", "auction_winner", "auction_overcome_others"),
           "Debriefing3": ("id", "bdm_unfair", "bdm_risky", "bdm_not_understood", "bdm_complicated", "auction_unfair", "auction_risky", "auction_not_understood", "auction_complicated"),
           "Debriefing4": ("id", "others_charity_interest", "you_charity_interest", "aware_cheating", "aware_preventing_cheating", "aware_preventing_loss"),           
           "Lottery": ("id", "choice1", "choice2", "choice3", "choice4", "choice5", "chosen", "win"),
           "Dice Lottery": ("id", "rolls", "reward"),
           "Hexaco": ("id", "number", "answer", "item"),           
           "Attention checks": ("id", "part", "correct"),
           "Prosociality": ("id", "item", "answer"),
           "Demographics": ("id", "sex", "age", "language", "student", "field"),
           "Ending": ("id", "reward", "chosen_block"),

           "Perception cheating": ("id", "before_attention", "before_thinking", "before_cheating", "before_fun",
                                   "before_justification", "before_random", "after_attention", "after_thinking",
                                   "after_cheating",  "after_fun", "after_justification", "after_random"),
           "Debriefing": ("id", "comments", "aim_dice", "aim_correct", "demand", "immoral", "truth") 
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
          "Ending"
         ]

for study in studies:
    with open("{} results.txt".format(study), mode = "w") as f:
        f.write("\t".join(columns[study]))

with open("Time results.txt", mode = "w") as times:
    times.write("\t".join(["id", "order", "frame", "time"]))

dirs = os.listdir()
#filecount = 0 #
for directory in dirs:
    if ".py" in directory or "results" in directory:
        continue
    files = os.listdir(directory)
    for file in files:
        if ".py" in file or "results" in file or "file.txt" in file or "STATION" in file or ".txt" not in file:
            continue

        with open(os.path.join(directory, file)) as datafile:
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
                            if columns[study][0] == "id" and content: #
                                identificator = content.split()[0] #
                                content = content.replace(identificator, identificator + "_" + directory) #
                                #content = content.replace(identificator, identificator + "_" + str(filecount)) #
                            if not content:
                                break
                            else:
                                results.write("\n" + content)
                        
                

    
        
