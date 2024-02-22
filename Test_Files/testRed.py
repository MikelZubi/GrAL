from transformers import XLMRobertaForTokenClassification,  AutoTokenizer
import torch
import os
import json
import csv
import sys
from seqeval.metrics import f1_score, recall_score, precision_score



def main(cross,seed="42"):
    f1Entity = ["F1 Entity"]
    recallEntity = ["Recall Entity"]
    precisionEntity = ["Precision Entity"]
    f1Triggers=["F1 Triggers"]
    recallTriggers = ["Recall Triggers"]
    precisionTriggers = ["Precision Triggers"]
    f1ArgumentsGold=["F1 Arguments"]
    recallArguments = ["Recall Arguments"]
    precisionArguments = ["Precision Arguments"]
    languages = [""]
    device = torch.device(type='cuda',index=0)
    for language in os.listdir('Models_REDUCED'):
        languages.append(language)
        print("****************************************************")
        print(language)
        test = "MEE_BIO/" + cross + "/test.json"
        testR =  open(test, "r")
        tokens = []
        entity = []
        entityF = []
        triggers = []
        triggersF = []
        for line in testR:
            data = json.loads(line)
            tokens.append(data['tokens'])
            entity.append(data['labels'])
            for label in data['labels']:
                entityF.append(label)
            triggers.append(data['triggers'])
            for trigger in data['triggers']:
                triggersF.append(trigger)
        testR.close()

        #ENTITY

        task = 'entity'
        print("----------------------------------------------------")
        print(task)
        path = 'Models_REDUCED/' + language + '/' + task + '/'
        configPath = open(path + 'config.json','r')
        config = json.load(configPath)
        model = XLMRobertaForTokenClassification.from_pretrained(path)
        model = model.to(device)
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base',use_fast=True)
        bio = []
        for z in range(len(tokens)):
            tokenized_input, labels = tokenize_and_align_labels([tokens[z]],tokenizer,device)
            out = model(**tokenized_input)['logits']
            maxout = torch.argmax(out,dim=2)
            maxout = maxout.to('cpu')
            maxoutnp = maxout.numpy()
            for i in range(len(maxoutnp)):
                bioT = []
                for j in range(len(maxoutnp[i])):
                    if labels[i][j] != -100:
                        bioT.append(config['id2label'][str(maxoutnp[i][j])])
                bio.append(bioT)
        
        f1 = f1_score(entity,bio,zero_division='0')
        precision = precision_score(entity,bio)
        recall = recall_score(entity,bio)
        precisionEntity.append(str(precision,2))
        recallEntity.append(str(recall,2))
        f1Entity.append(str(f1,2))


        #TRIGGERS
    
        task = 'triggers'
        print("----------------------------------------------------")
        print(task)
        path = 'Models_REDUCED/' + language + '/' + task + '/'
        bio = []
        configPath = open(path + 'config.json','r')
        config = json.load(configPath)
        model = XLMRobertaForTokenClassification.from_pretrained(path)
        model = model.to(device)
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base',use_fast=True)
        for z in range(len(tokens)):
            tokenized_input, labels = tokenize_and_align_labels([tokens[z]],tokenizer,device)
            out = model(**tokenized_input)['logits']
            maxout = torch.argmax(out,dim=2)
            maxout = maxout.to('cpu')
            maxoutnp = maxout.numpy()
            for i in range(len(maxoutnp)):
                bioT = []
                for j in range(len(maxoutnp[i])):
                    if labels[i][j] != -100:
                        bioT.append(config['id2label'][str(maxoutnp[i][j])])
                bio.append(bioT)

        f1 = f1_score(triggers,bio,zero_division='0')
        precision = precision_score(triggers,bio)
        recall = recall_score(triggers,bio)
        precisionTriggers.append(str(precision,2))
        recallTriggers.append(str(recall,2))
        f1Triggers.append(str(f1,2))

    
        #ARGUMENTS

        task = 'arguments'
        print("----------------------------------------------------")
        print(task)
        test = "MEE_BIO/" + cross + "/test_arg.json"
        testR =  open(test, "r")
        tokensArgGold = []
        arguments = []
        argumentsF = []
        linesGold = []
        for line in testR:
            data = json.loads(line)
            tokensArgGold.append(data['tokens'])
            arguments.append(data['arguments'])
            for argument in data['arguments']:
                argumentsF.append(argument)
            if language != 'all':
                linesGold.append(data['line'])
            else:
                linesGold.append(data['lineAll'])
        testR.close()
        path = 'Models_REDUCED/' + language + '/' + task + '/'
        bio = []
        configPath = open(path + 'config.json','r')
        config = json.load(configPath)
        model = XLMRobertaForTokenClassification.from_pretrained(path)
        model = model.to(device)
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base',use_fast=True) 
        for z in range(len(linesGold)):
            tokenized_input, labels = tokenize_and_align_labels([tokensArgGold[z]],tokenizer,device)
            out = model(**tokenized_input)['logits']
            maxout = torch.argmax(out,dim=2)
            maxout = maxout.to('cpu')
            maxoutnp = maxout.numpy()
            for i in range(len(maxoutnp)):
                bioT = []
                for j in range(len(maxoutnp[i])):
                    if labels[i][j] != -100:
                        bioT.append(config['id2label'][str(maxoutnp[i][j])])
                bio.append(bioT)
        
            
    
    
        f1 = f1_score(arguments,bio,zero_division='0')
        precision = precision_score(arguments,bio)
        recall = recall_score(arguments,bio)
        f1ArgumentsGold.append(str(f1,2))
        precisionArguments.append(str(precision,2))
        recallArguments.append(str(recall,2))

    file = "Test/Reduced/" + cross + "/seed"+ str(seed) + "/test.csv"
    os.makedirs(os.path.dirname(file), exist_ok=True)
    csvFile = open(file,"w")
    csvTest = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvTest.writerow(languages)
    csvTest.writerow(f1Entity)
    csvTest.writerow(precisionEntity)
    csvTest.writerow(recallEntity)
    csvTest.writerow(f1Triggers)
    csvTest.writerow(precisionTriggers)
    csvTest.writerow(recallTriggers)
    csvTest.writerow(f1ArgumentsGold)
    csvTest.writerow(precisionArguments)
    csvTest.writerow(recallArguments)
    csvFile.close()


# Tokenize all texts and align the labels with them.
def tokenize_and_align_labels(examples,tokenizer,device):
    tokenized_inputs = tokenizer(examples, padding=False,truncation=True, is_split_into_words=True,max_length = None,return_tensors='pt').to(device)

    labels = []
    for i, label in enumerate(examples):
        word_ids = tokenized_inputs.word_ids(batch_index=i)  # Map tokens to their respective word.
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:  # Set the special tokens to -100.
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:  # Only label the first token of a given word.
                label_ids.append(label[word_idx])
            else:
                label_ids.append(-100)
            previous_word_idx = word_idx
        labels.append(label_ids)

    return tokenized_inputs, labels


if __name__ == "__main__":
    main(cross=str(sys.argv[1]),seed=sys.argv[2])