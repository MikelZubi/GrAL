import numpy as np
import csv
import os

CSVData1 = open("Test/Reduced2/seed16/test_Euskera.csv")
Array2d_result1 = np.genfromtxt(CSVData1, delimiter=",")
data16 = Array2d_result1[1:,1:]
CSVData2 = open("Test/Reduced2/seed44/test_Euskera.csv")
Array2d_result2 = np.genfromtxt(CSVData2, delimiter=",")
data44 = Array2d_result2[1:,1:]
CSVData3 = open("Test/Reduced2/seed85/test_Euskera.csv")
Array2d_result3 = np.genfromtxt(CSVData3, delimiter=",")
data85 = Array2d_result3[1:,1:]
dataAvg = [[] for i in range(len(Array2d_result3))]
dataStd = [[] for i in range(len(Array2d_result3))]
dataAvg[0] = ["","all","english","polish","spanish","portuguese","japanese","hindi","korean","turkish"]
dataAvg[1] = ["Accuracy Entity"]
dataAvg[2] = ["F1 Entity"]
dataAvg[3] = ["Recall Entity"]
dataAvg[4] = ["Precision Entity"]
dataAvg[5] = ["Accuracy Triggers"]
dataAvg[6] = ["F1 Triggers"]
dataAvg[7] = ["Recall Triggers"]
dataAvg[8] = ["Precision Triggers"]
dataAvg[9] = ["Accuracy Arguments"]
dataAvg[10] = ["F1 Arguments"]
dataAvg[11] = ["Recall Arguments"]
dataAvg[12] = ["Precision Arguments"]
dataStd[0] = ["","all","english","polish","spanish","portuguese","japanese","hindi","korean","turkish"]
dataStd[1] = ["Accuracy Entity"]
dataStd[2] = ["F1 Entity"]
dataStd[3] = ["Recall Entity"]
dataStd[4] = ["Precision Entity"]
dataStd[5] = ["Accuracy Triggers"]
dataStd[6] = ["F1 Triggers"]
dataStd[7] = ["Recall Triggers"]
dataStd[8] = ["Precision Triggers"]
dataStd[9] = ["Accuracy Arguments"]
dataStd[10] = ["F1 Arguments"]
dataStd[11] = ["Recall Arguments"]
dataStd[12] = ["Precision Arguments"]

for i in range(1,len(Array2d_result3)):
    for j in range(len(data16[i-1])):
        array = np.array([data16[i-1,j],data44[i-1,j],data85[i-1,j]])
        dataAvg[i].append(round(np.mean(array,dtype=float),2))
        dataStd[i].append(round(np.std(array,dtype=float),2))
fileAvg = "Test/Reduced2/test_Avg.csv"
os.makedirs(os.path.dirname(fileAvg), exist_ok=True)
csvFileAvg = open(fileAvg,"w")
csvAvg = csv.writer(csvFileAvg, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
for i in range(len(dataAvg)):
    csvAvg.writerow(dataAvg[i])
csvFileAvg.close()

fileStd = "Test/Reduced2/test_Std.csv"
os.makedirs(os.path.dirname(fileStd), exist_ok=True)
csvFileStd = open(fileStd,"w")
csvStd = csv.writer(csvFileStd, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
for i in range(len(dataStd)):
    csvStd.writerow(dataStd[i])
csvFileStd.close()