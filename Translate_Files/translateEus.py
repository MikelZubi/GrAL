import json
import copy as cp
import os


dicLab = {"PER":"PERSON","ORG":"ORGANIZATION","GPE":"GEO","LOC":"LOCATION","FAC":"FACILITY","VEH":"VEHICLE","WEA":"WEAPON","TIME":"TIME","MON":"MONEY","CRIME":"CRIME","POS":"JOB"}
dicTrig = {}
pathR = "Eus/1500.eusie.annotated.json"
pathW = "MEE_BIO/euskara/dev.json"
pathWArg = "MEE_BIO/euskara/dev_arg.json"
os.makedirs(os.path.dirname(pathW), exist_ok=True)
jsonR = open(pathR, "r")
jsonW = open(pathW, "w")
argJsonW = open(pathWArg, "w")
newdata = {}
newdataArg = {}
lineCount = 0
for line in jsonR:
    if lineCount == 150:
        jsonW.close()
        argJsonW.close()
        pathW2 = "MEE_BIO/euskara/test.json"
        pathW2Arg = "MEE_BIO/euskara/test_arg.json"
        os.makedirs(os.path.dirname(pathW2), exist_ok=True)
        jsonW = open(pathW2, "w")
        argJsonW = open(pathW2Arg, "w")
    data = json.loads(line)
    #newdata["doc_id"] = data["doc_id"]
    #newdata["sent_id"] = data["sent_id"]
    #newdata["sentece"] = data["sentence"]
    newdata["tokens"] = data["tokens"]
    newdata["labels"] = ["O" for i in range(len(data["tokens"]))]
    newdata["triggers"] = ["O" for i in range(len(data["tokens"]))]
    newdata["arguments"] = []

    entityIds = {}
    


    #Labels detection
    for label in data["entity_mentions"]:
        entityIds[label["id"]] = {"start": label["start"],"end": label["end"]}
        if label["entity_type"] == "OBJ":
            continue
        labType = dicLab[label["entity_type"]]
        pre = "B-"
        for i in range(label["start"],label["end"]):
            newdata["labels"][i] = pre + labType
            pre = "I-"
        
    #Triggers detection
    for trigger in data["event_mentinos"]:
        splitted = trigger["event_type"].split(":")
        triggType = splitted[0] + "_" + splitted[1]
        start = trigger["trigger"]["start"]
        end = trigger["trigger"]["end"]
        pre = "B-"
        for i in range(start,end):
            newdata["triggers"][i] = pre + triggType
            pre = "I-"
        
        
        if trigger["arguments"] == []:
            continue

        #Ola jarrita bakarrik argumentuak dittuztenak eongo die, bestela aurreko if-an gañetik jarri kodigo zati hau
        #newdataArg["doc_id"] = data["doc_id"]
        #newdataArg["sent_id"] = data["sent_id"]
        #newdataArg["sentece"] = data["sentence"]
        newdataArg["line"] = lineCount
        newdataArg["lineAll"] = lineCount
        tokens = cp.deepcopy(data["tokens"])
        tokens.insert(start,"$$$")
        tokens.insert(end+1,"$$$")
        newdataArg["tokens"] = tokens
        newdataArg["arguments"] = ["O" for i in range(len(newdataArg["tokens"]))]
        for argument in trigger["arguments"]:
            entStart = entityIds[argument["entity_id"]]["start"]
            entEnd = entityIds[argument["entity_id"]]["end"]
            if entStart < start:
                pre = "B-"
                role = argument["role"]
                for i in range(entStart,entEnd):
                    newdataArg["arguments"][i] = pre + role
                    pre = "I-"
                newdataArg["arguments"][entStart]
            else:
                pre = "B-"
                role = argument["role"]
                for i in range(entStart+2,entEnd+2):
                    newdataArg["arguments"][i] = pre + role
                    pre = "I-"
                newdataArg["arguments"][entStart]
        write_string = json.dumps(newdataArg,ensure_ascii=False)
        argJsonW.write(write_string + '\n')





    
    write_string = json.dumps(newdata,ensure_ascii=False)
    jsonW.write(write_string + '\n')
    lineCount += 1

jsonR.close()
jsonW.close()
argJsonW.close()

        

