import json

pathD = "Eus/dev.json"
pathT = "Eus/test.json"
jsonD = open(pathD, "r")
jsonT = open(pathT, "r")
countTrigg = 0
countLabel = 0
tokensKop = 0
for line in jsonD:
    data = json.loads(line)
    labs = data["labels"]
    for lab in labs:
        if lab[0] == "B":
            countLabel+= 1
    triggs = data["triggers"]
    for trigg in triggs:
        if trigg[0] == "B":
            countTrigg+= 1
    tokensKop += len(data["tokens"])
    
for line in jsonT:
    data = json.loads(line)
    labs = data["labels"]
    for lab in labs:
        if lab[0] == "B":
            countLabel+= 1
    triggs = data["triggers"]
    for trigg in triggs:
        if trigg[0] == "B":
            countTrigg+= 1
    tokensKop += len(data["tokens"])

pathDA = "Eus/dev_arg.json"
jsonDA = open(pathDA, "r")
countArg = 0
for line in jsonDA:
    data = json.loads(line)
    args = data["arguments"]
    for arg in args:
        if arg[0] == "B":
            countArg+=1

pathTA = "Eus/test_arg.json"
jsonTA = open(pathTA, "r")
for line in jsonTA:
    data = json.loads(line)
    args = data["arguments"]
    for arg in args:
        if arg[0] == "B":
            countArg+=1

print("Entitateak: " + str(countLabel))
print("Gertaerak: " + str(countTrigg))
print("Argumentuak: " + str(countArg))
print("Batazbesteko token kop: " + str(tokensKop/295))