import pandas
import copy as cp
import os
import csv
import sys

cross = str(sys.argv[1])

morph = {"euskara":"agglutinative","english":"fusional","spanish":"fusional","portuguese":"fusional","polish":"fusional","turkish":"agglutinative","hindi":"fusional","japanese":"agglutinative","korean":"agglutinative"}
morphS = {"euskara":"Ergative-Absolutive","english":"Nominative-Accusative","spanish":"Nominative-Accusative","portuguese":"Nominative-Accusative","polish":"Nominative-Accusative","turkish":"Nominative-Accusative","hindi":"Split Ergative","japanese":"Nominative-Accusative","korean":"Nominative-Accusative"}
order = {"euskara":"SOV","english":"SVO","spanish":"SVO","portuguese":"SVO","polish":"SVO","turkish":"SOV","hindi":"SOV","japanese":"SOV","korean":"SOV"}
script = {"euskara":"Latin","english":"Latin","spanish":"Latin","portuguese":"Latin","polish":"Latin","turkish":"Latin","hindi":"Devanagari","japanese":"Kanji\Kana","korean":"Hangul"}
geo = {"euskara":"West_Europe","english":"West_Europe","spanish":"West_Europe","portuguese":"West_Europe","polish":"East_Europe","turkish":"East_Europe\West_Asia","hindi":"India","japanese":"East_Asia","korean":"East_Asia"}

metrics = ["F1","Precision","Recall"]
tasks = ["Entity","Triggers","Arguments"]
lang = ["english","spanish","portuguese","polish","turkish","hindi","japanese","korean"]

head = ["seed","task","train_lang","morph","morph-syn","order","script","geo","metric","score"]
rows = []

seed16 = pandas.read_csv("../Test/Reduced/"+cross+"/seed16/test.csv",header=0,index_col=0)
for language in lang:
    if language == cross:
        continue
    for task in tasks:
        for metric in metrics:
            key = metric + " " + task
            score = seed16[language][key]
            row = ["16",task,language,morph[language],morphS[language],order[language],script[language],geo[language],metric,score]
            rows.append(cp.deepcopy(row))

seed44 = pandas.read_csv("../Test/Reduced/"+cross+"/seed44/test.csv",header=0,index_col=0)
for language in lang:
    if language == cross:
        continue
    for task in tasks:
        for metric in metrics:
            key = metric + " " + task
            score = seed44[language][key]
            row = ["44",task,language,morph[language],morphS[language],order[language],script[language],geo[language],metric,score]
            rows.append(cp.deepcopy(row))

seed85 = pandas.read_csv("../Test/Reduced/"+cross+"/seed85/test.csv",header=0,index_col=0)
for language in lang:
    if language == cross:
        continue
    for task in tasks:
        for metric in metrics:
            key = metric + " " + task
            score = seed85[language][key]
            row = ["85",task,language,morph[language],morphS[language],order[language],script[language],geo[language],metric,score]
            rows.append(cp.deepcopy(row))
    
file = "../Test/Reduced/"+cross+"/table.csv"
os.makedirs(os.path.dirname(file), exist_ok=True)
csvFile = open(file,"w")
csvTable = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csvTable.writerow(head)
for row in rows:
    csvTable.writerow(row)
csvFile.close()

