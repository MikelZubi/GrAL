
import pandas as pd
import matplotlib.pyplot as plt


db = pd.read_csv('Test/Reduced/table.csv')
db1 = db[db['metric'] == 'F1']

#Delete spanish arguments
cond1 = db1['train_lang'] == 'spanish'
cond2 = db1['task'] == 'Arguments'
cond = cond1 & cond2
df = db1[~cond]

tasks = ["Entity","Triggers","Arguments"]
head = ["morphC","morphT","morph-synC","morph-synT","orderC","orderT","scriptC","scriptT","geoC","geoT"]
atrs = []
count = 0

for i in range(0,len(head),2):
    name = head[i][0:len(head[i])-1]
    for value in df[head[i]]:
        if value not in atrs:
            atrs.append(value)
    for atr in atrs:
        count = 0
        hdf = df[df[head[i]] == atr]
        fig, axs = plt.subplots(1,3,figsize=(14,10))


        for task in tasks:

            dfa = hdf[hdf['task']==task]
            b_plot = dfa.boxplot(by = head[i+1], column = ['score'],grid = True, ax = axs[count])
            axs[count].title.set_text(task)
            axs[count].set_xlabel("")
            axs[count].tick_params(labelrotation=45)
            b_plot.plot()
            count +=1

        fig.suptitle(name + " = " + atr)
        axs[0].set_ylabel("F1")
        fig.savefig('Images/'+name+"_"+atr+".png")
        plt.close()


    atrs.clear()



