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
            denakO(fileR,fileW)


def denakO(filenameR, filenameW):
    os.makedirs(os.path.dirname(filenameW), exist_ok=True)
    jsonR = open(filenameR, "r")
    jsonW = open(filenameW, "w")
    newdata = {}
    for line in jsonR:
        data = json.loads(line)
        newdata["tokens"] = data["tokens"]
        newdata["labels"] = ["O" for i in range(len(data["tokens"]))]
        write_string = json.dumps(newdata,ensure_ascii=False)
        jsonW.write(write_string + '\n')
    jsonR.close()
    jsonW.close()

def hasieratu():
    dirpath = os.path.join('MEE_BIO')
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)

def translate(filename):
    return 0

if __name__ == "__main__":
    main()

