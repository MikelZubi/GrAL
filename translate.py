import os
import json
import shutil
import copy as cp

def main():
    directoryR = 'MEE'
    directoryW = 'MEE_BIO'
    hasieratu()
    for language in os.listdir(directoryR):
        pathR = directoryR + '/' + language
        pathW = directoryW + '/' + language
        print(language)
        for file in os.listdir(directoryR + '/' + language):
            fileR = pathR + '/' + file
            fileW = pathW + '/' + file[0:-1]
            translate(fileR,fileW,file[0:-1])


def translate(filenameR, filenameW,filetype):
    allPath = 'MEE_BIO/all/'+filetype
    argFileW = filenameW.split(".")[0] + "_arg" + ".json"
    os.makedirs(os.path.dirname(filenameW), exist_ok=True)
    os.makedirs(os.path.dirname(argFileW), exist_ok=True)
    os.makedirs(os.path.dirname(allPath), exist_ok=True)
    jsonR = open(filenameR, "r")
    jsonW = open(filenameW, "w")
    argJsonW = open(argFileW)
    jsonAll = open(allPath, "a")
    newdata = {}
    newdataArg = {}
    trigCount = 0
    for line in jsonR:
        data = json.loads(line)
        newdata["tokens"] = data["tokens"]
        newdata["labels"] = ["O" for i in range(len(data["tokens"]))]
        newdata["triggers"] = ["O" for i in range(len(data["tokens"]))]
        newdata["arguments"] = []
        start, end = getStartEnd(data["tokens"])
        #Entities extraction
        for label in data["entities"]:
            startPos = data["entities"][label]["start"]
            endPos = data["entities"][label]["end"]
            if ';' in endPos:
                endPos = endPos.split(";")[1]
            for i in range(0,len(start)):
                if start[i] > int(startPos):
                    hasiera = i - 1
                    break
            for i in range(hasiera,len(end)):
                if end[i] >= int(endPos):
                    amaiera = i
                    break
            newdata["labels"][hasiera] = "B-" + data["entities"][label]["type"]
            for i in range(hasiera + 1,amaiera + 1):
                newdata["labels"][i] = "I-" + data["entities"][label]["type"]
        #Triggers Extraction
        for label in data["triggers"]:
            startPos = data["triggers"][label]["start"]
            endPos = data["triggers"][label]["end"]
            if ';' in endPos:
                endPos = endPos.split(";")[1]
            for i in range(0, len(start)):
                if start[i] > int(startPos):
                    hasiera = i - 1
                    break
            for i in range(hasiera, len(end)):
                if end[i] >= int(endPos):
                    amaiera = i
                    break
            newdataArg["tokens"] =
            newdata["triggers"][hasiera] = "B-" + data["triggers"][label]["type"]
            for i in range(hasiera + 1, amaiera + 1):
                newdata["triggers"][i] = "I-" + data["triggers"][label]["type"]
        #Arguments Extraction
        for label in data["arguments"]:
            startPosT = data["triggers"][label["trigger"]]["start"]
            endPosT = data["triggers"][label["trigger"]]["end"]
            startPosA = data["entities"][label["argument"]]["start"]
            endPosA = data["entities"][label["argument"]]["end"]
            if ';' in endPosT:
                endPosT = endPosT.split(";")[1]
            for i in range(0, len(start)):
                if start[i] > int(startPosT):
                    hasieraT = i - 1
                    break
            for i in range(hasieraT, len(end)):
                if end[i] >= int(endPosT):
                    amaieraT = i
                    break
            if ';' in endPosA:
                endPosA = endPosA.split(";")[1]
            for i in range(0, len(start)):
                if start[i] > int(startPosA):
                    hasieraA = i - 1
                    break
            for i in range(hasieraA, len(end)):
                if end[i] >= int(endPosA):
                    amaieraA = i
                    break
            newdict = label
            newdict["trigger"] = [str(i) for i in range(hasieraT,amaieraT+1)]
            newdict["argument"] = [str(i) for i in range(hasieraA, amaieraA + 1)]
            newdata["arguments"].append(cp.deepcopy(newdict))
        write_string = json.dumps(newdata,ensure_ascii=False)
        jsonW.write(write_string + '\n')
        jsonAll.write(write_string + '\n')
    jsonR.close()
    jsonW.close()
    jsonAll.close()

def hasieratu():
    dirpath = os.path.join('MEE_BIO')
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)

def getStartEnd(tokens):
    count = 0
    start = []
    end = []
    for token in tokens:
        start.append(count)
        end.append(count + len(token))
        count += len(token) + 1
    return start, end

def getArgTokens(tokens,trigger):
    argTokens = []
    triggerFound = False
    for token in tokens:
        if token == trigger:
            argTokens.append("$$$")
            argTokens.append(token)
            argTokens.append("$$$")
            triggerFound = True
        else:
            argTokens.append(token)
        if token == ".":
            if triggerFound:
                break
            else:
                argTokens.clear()

    #Begiratu, ola programatuta soilik puntu eta geroko argumentoak ahalko ziren atera.
    return argTokens


if __name__ == "__main__":
    main()

