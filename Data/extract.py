import os

studies = ["Cheating estimates",
           "Cheating 1",
           "Cheating 2",
           "Cheating 3",
           "Cheating 4",
           "Cheating predictions",
           "Cheating 5",
           "Lottery",
           "Anchoring 1",
           "Anchoring 2",
           "Character environment",
           "Character character",
           "Hexaco",
           "Attention checks",
           "Dark Triad",
           "Demographics",
           "Winnings",
           "Perception cheating",
           "Debriefing"
           ]


columns = {"Cheating estimates": ("id", "estimate"),
           "Cheating 1": ("id", "block", "trial", "condition", "roll", "prediction", "report", "time",
                          "time1", "time2"), 
           "Cheating 2": ("id", "block", "trial", "condition", "roll", "prediction", "report", "time",
                          "time1", "time2"), 
           "Cheating 3": ("id", "block", "trial", "condition", "roll", "prediction", "report", "time",
                          "time1", "time2"),
           "Cheating 4": ("id", "block", "trial", "condition", "roll", "prediction", "report", "time",
                          "time1", "time2"),
           "Cheating predictions": ("id", "before_percent", "after_percent", "before_average", "after_average"),
           "Cheating 5": ("id", "block", "trial", "condition", "roll", "prediction", "report", "time",
                          "time1", "time2"),
           "Lottery": ("id", "rolls", "reward"),
           "Anchoring 1": ("id", "trial", "item", "anchor", "answer", "example"),
           "Anchoring 2": ("id", "trial", "item", "comparison", "absolute"),
           "Character environment": ("id", "block", "behavior", "person", "condition", "item1", "item2",
                                     "item3", "item4", "immoral", "time"),
           "Character character": ("id", "block", "behavior", "person", "condition", "item1", "item2",
                                   "item3", "item4", "immoral", "time"),
           "Hexaco": ("id", "number", "answer", "item"),
           "Attention checks": ("id", "part", "failed"),
           "Dark Triad": ("id", "item", "answer"),
           "Demographics": ("id", "sex", "age", "language", "student", "field"),
           "Winnings": ("id", "reward"),
           "Perception cheating": ("id", "before_attention", "before_thinking", "before_cheating", "before_fun",
                                   "before_justification", "before_random", "after_attention", "after_thinking",
                                   "after_cheating",  "after_fun", "after_justification", "after_random"),
           "Debriefing": ("id", "comments", "aim_dice", "aim_correct", "demand", "immoral", "truth") 
           }

frames = ["Intro",
          "Instructions1",
          "BlockOne",
          "Instructions2",
          "BlockTwo",
          "Instructions3",
          "BlockThree",
          "Instructions4",
          "BlockFour",
          "Estimate",
          "Instructions5",
          "BlockFive",
          "EndCheating",
          "AnchoringInstructions1",
          "Comparison1",
          "AnchoringInstructions2",
          "Comparison2",
          "CharacterIntro",
          "Character1",
          "CharacterIntro2",
          "Character2",
          "LotteryInstructions",
          "Lottery",
          "QuestInstructions",
          "Hexaco",
          "DarkTriad1",
          "DarkTriad2",
          "Demographics",
          "DebriefCheating",
          "Debriefing",
          "Ending",
          "end"
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
                        
                

    
        
