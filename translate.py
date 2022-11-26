import os
import json
import shutil

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
            translate(fileR,fileW)


def translate(filenameR, filenameW):
    os.makedirs(os.path.dirname(filenameW), exist_ok=True)
    jsonR = open(filenameR, "r")
    jsonW = open(filenameW, "w")
    newdata = {}
    for line in jsonR:
        data = json.loads(line)
        newdata["tokens"] = data["tokens"]
        newdata["labels"] = ["O" for i in range(len(data["tokens"]))]
        start, end = getStartEnd(data["tokens"])
        for label in data["entities"]:
            startPos = data["entities"][label]["start"]
            endPos = data["entities"][label]["end"]
            if ';' in endPos: #?¿
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
    jsonR.close()
    jsonW.close()

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

if __name__ == "__main__":
    main()

