import os
import json
import shutil
import copy as cp
import random as rd
import sys

def main(cross):
    hasieratu()
    reduce(cross)
    directoryR = 'MEE_REDUCED3'
    directoryW = 'MEE_BIO_REDUCED3'
    for language in os.listdir(directoryR):
        pathR = directoryR + '/' + language
        pathW = directoryW + '/' + language
        print(language)
        for filetype in os.listdir(directoryR + '/' + language):
            fileR = pathR + '/' + filetype + '/train.jsonl'
            fileW = pathW + '/' + filetype + '/train.json'
            translate(fileR,fileW,filetype)


def translate(filenameR, filenameW,filetype):
    allPath = 'MEE_BIO_REDUCED3/all/'+ filetype + '/train.json'
    os.makedirs(os.path.dirname(filenameW), exist_ok=True)
    os.makedirs(os.path.dirname(allPath), exist_ok=True)
    jsonR = open(filenameR, "r")
    jsonW = open(filenameW, "w")
    #For count the lines in all 
    try:
        jsonAllRead = open(allPath, "r")
        for count, _ in enumerate(jsonAllRead):
            pass
        lineCountAll = count + 1
        jsonAllRead.close()
    except:
        lineCountAll = 0
    jsonAll = open(allPath, "a")
    if filetype == 'entities':
        entities(jsonR,jsonW,jsonAll)
    elif filetype == 'triggers':
        triggers(jsonR,jsonW,jsonAll)
    else:
        arguments(jsonR,jsonW,jsonAll,lineCountAll)
    

def entities(jsonR,jsonW,jsonAll):
    newdata = {}
    for line in jsonR:
        data = json.loads(line)
        newdata["tokens"] = data["tokens"]
        newdata["labels"] = ["O" for i in range(len(data["tokens"]))]
        newdata["triggers"] = ["O" for i in range(len(data["tokens"]))] #Entrenatzeakoan bestela errorea
        newdata["arguments"] = [] #Entrenatzekoan bestela errorea
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
        write_string = json.dumps(newdata,ensure_ascii=False)
        jsonW.write(write_string + '\n')
        jsonAll.write(write_string + '\n')
    jsonR.close()
    jsonW.close()
    jsonAll.close()

def triggers(jsonR,jsonW,jsonAll):
    newdata = {}
    for line in jsonR:
        data = json.loads(line)
        newdata["tokens"] = data["tokens"]
        newdata["labels"] = ["O" for i in range(len(data["tokens"]))] #Entrenatzeakoan bestela errore
        newdata["triggers"] = ["O" for i in range(len(data["tokens"]))]
        newdata["arguments"] = [] #Entrenatzekoan bestela errorea
        start, end = getStartEnd(data["tokens"])
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
            newdata["triggers"][hasiera] = "B-" + data["triggers"][label]["type"]
            for i in range(hasiera + 1, amaiera + 1):
                newdata["triggers"][i] = "I-" + data["triggers"][label]["type"]
        write_string = json.dumps(newdata,ensure_ascii=False)
        jsonW.write(write_string + '\n')
        jsonAll.write(write_string + '\n')
    jsonR.close()
    jsonW.close()
    jsonAll.close()

def arguments(jsonR,jsonW,jsonAll,lineCountAll):
    newdataArg = {}
    lineCount  = 0
    for line in jsonR:
        data = json.loads(line)
        start, end = getStartEnd(data["tokens"])
        #Arguments Extraction
        newdataArg = {}
        prevTrigg = None
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
            triggers = [i for i in range(hasieraT,amaieraT+1)]
            if triggers != prevTrigg:
                if prevTrigg != None:
                    argWrite_string = json.dumps(newdataArg, ensure_ascii=False)
                    jsonW.write(argWrite_string + '\n')
                    jsonAll.write(argWrite_string + '\n')
                newdataArg = {}
                newdataArg["line"] = lineCount
                newdataArg["lineAll"] = lineCountAll
                newdataArg["tokens"] = []
                for i in range(len(data["tokens"])):
                    if i == triggers[0]:
                        newdataArg["tokens"].append("$$$")
                        for j in triggers:
                            newdataArg["tokens"].append(data["tokens"][j])
                        newdataArg["tokens"].append("$$$")
                    else:
                        newdataArg["tokens"].append(data["tokens"][i])
                newdataArg["arguments"] = ["O" for i in range(len(newdataArg["tokens"]))]
                prevTrigg = cp.deepcopy(triggers)
            arguments = [i if hasieraA < triggers[0] else (i + 2) for i in range(hasieraA, amaieraA + 1)]
            newdataArg["arguments"][arguments[0]] = "B-"+label["role"]
            for i in arguments[1:]:
                newdataArg["arguments"][i] ="I-"+label["role"]
        if prevTrigg != None:
            argWrite_string = json.dumps(newdataArg, ensure_ascii=False)
            jsonW.write(argWrite_string + '\n')
            jsonAll.write(argWrite_string + '\n')
        lineCount+=1
        lineCountAll+=1
    jsonR.close()
    jsonW.close()
    jsonAll.close()

def hasieratu():
    dirpath = os.path.join('MEE_BIO_REDUCED3')
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
    dirpath = os.path.join('MEE_REDUCED3')
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


#Labelak jun sartzen denak 12508 euki arte (esaldi baten pasatzen bada berdin du). Bestek borratu (ez sartu)
#Triggerrak jun sartzen denak (Asta ez dittuenak berez) 1125 euki arte (esaldi baten pasatzen bada berdin du). Bestek borratu (ez sartu)
#Argumentuak jun sartzen denak 1416 euki arte. Bestek borratu (Ez sartu). Goatu gaztelera eztela allatzen kantitate orreta
def reduce(cross):
    rd.seed(16)
    directoryR = 'MEE'
    directoryW = 'MEE_REDUCED3'
    dirpath = os.path.join(directoryW)
    motak = ["entities","triggers","arguments"]
    maxim = [12508,1125,1416]
    lines = []
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
    for j in range(3):
        print(motak[j])
        for language in os.listdir(directoryR):
            if language == cross:
                continue
            print(language)
            pathR = directoryR + '/' + language
            pathW = directoryW + '/' + language + '/' + motak[j]
            lines.clear()
            for file in os.listdir(directoryR + '/' + language):
                fileR = pathR + '/' + file
                jsonR = open(fileR, "r")
                lines += [json.loads(line) for line in jsonR]
                jsonR.close()
            rd.shuffle(lines)
            fileW = pathW +'/train.jsonl'
            os.makedirs(os.path.dirname(fileW), exist_ok=True)
            jsonW = open(fileW,'w')
            count = 0
            for line in lines:
                newLines = cp.deepcopy(line)
                count += len(line[motak[j]])
                write_string = json.dumps(newLines,ensure_ascii=False)
                jsonW.write(write_string + '\n')
                if count > maxim[j]:
                    break
            jsonW.close()

if __name__ == "__main__":
    main(cross=sys.argv[1])