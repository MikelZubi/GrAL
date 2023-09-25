import numpy as np
import csv
import os
for cross in os.listdir("../Test/Reduced"):

    CSVData1 = open("../Test/Reduced/"+ cross +"/seed16/test.csv")
    print(cross)
    reader = csv.reader(CSVData1,delimiter=",")
    for row in reader:
        header1 = row
        break

    Array2d_result1 = np.genfromtxt(CSVData1, delimiter=",")
    data16 = Array2d_result1[0:,1:]
    CSVData2 = open("../Test/Reduced/"+ cross +"/seed44/test.csv")

    reader2 = csv.reader(CSVData2, delimiter=",")
    for row in reader2:
        header2 = row
        break

    Array2d_result2 = np.genfromtxt(CSVData2, delimiter=",")
    data44 = Array2d_result2[0:,1:]
    CSVData3 = open("../Test/Reduced/"+ cross +"/seed85/test.csv")

    reader3 = csv.reader(CSVData3, delimiter=",")
    for row in reader3:
        header3 = row
        break

    Array2d_result3 = np.genfromtxt(CSVData3, delimiter=",")
    data85 = Array2d_result3[0:,1:]

    assert header1 == header2
    assert header2 == header3

    dataAvg = [[] for i in range(len(Array2d_result3)+1)]
    dataStd = [[] for i in range(len(Array2d_result3)+1)]
    dataAvg[0] = header1
    dataAvg[1] = ["F1 Entity"]
    dataAvg[2] = ["Precision Entity"]
    dataAvg[3] = ["Recall Entity"]
    dataAvg[4] = ["F1 Triggers"]
    dataAvg[5] = ["Precision Triggers"]
    dataAvg[6] = ["Recall Triggers"]
    dataAvg[7] = ["F1 Arguments"]
    dataAvg[8] = ["Precision Arguments"]
    dataAvg[9] = ["Recall Arguments"]
    dataStd[0] = header1
    dataStd[1] = ["F1 Entity"]
    dataStd[2] = ["Recall Entity"]
    dataStd[3] = ["Precision Entity"]
    dataStd[4] = ["F1 Triggers"]
    dataStd[5] = ["Recall Triggers"]
    dataStd[6] = ["Precision Triggers"]
    dataStd[7] = ["F1 Arguments"]
    dataStd[8] = ["Recall Arguments"]
    dataStd[9] = ["Precision Arguments"]

    for i in range(1,len(dataAvg)):
        for j in range(len(data16[i-1])):
            array = np.array([data16[i-1,j],data44[i-1,j],data85[i-1,j]])
            dataAvg[i].append(round(np.mean(array,dtype=float),4)*100)
            dataStd[i].append(round(np.std(array,dtype=float),4)*100)
    fileAvg = "../Test/Reduced/"+cross+"/test_Avg.csv"
    os.makedirs(os.path.dirname(fileAvg), exist_ok=True)
    csvFileAvg = open(fileAvg,"w")
    csvAvg = csv.writer(csvFileAvg, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(dataAvg)):
        csvAvg.writerow(dataAvg[i])
    csvFileAvg.close()

    fileStd = "../Test/Reduced/"+cross+"/test_Std.csv"
    os.makedirs(os.path.dirname(fileStd), exist_ok=True)
    csvFileStd = open(fileStd,"w")
    csvStd = csv.writer(csvFileStd, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(dataStd)):
        csvStd.writerow(dataStd[i])
    csvFileStd.close()