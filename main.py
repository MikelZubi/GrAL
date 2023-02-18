from transformers import XLMRobertaForTokenClassification,  AutoTokenizer
import torch
import os
import json
import copy as cp
from pdb import set_trace
import spacy


def main():
    device = torch.device(type='cuda',index=0)
    language = "english"
    text = "Alice and Bob got married yesterday in Brazil "
    nlp = spacy.blank("xx")
    doc = nlp(text)
    tokens = []
    for token in doc:
        tokens.append(token.text)

    result = {}
    result["text"] = text
    result["language"] = language
    result["labels"]={}
    result["triggers"]={}
    
    #ENTITY
    task = 'entity'
    print(task)
    path = 'Models/' + language + '/' + task + '/'
    configPath = open(path + 'config.json','r')
    config = json.load(configPath)
    model = XLMRobertaForTokenClassification.from_pretrained(path)
    model = model.to(device)
    model.eval()
    tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base',use_fast=True)
    tokenized_input, labels = tokenize_and_align_labels([tokens],tokenizer,device)
    out = model(**tokenized_input)['logits']
    maxout = torch.argmax(out,dim=2)
    maxout = maxout.to('cpu')
    maxoutnp = maxout.numpy()
    bio = []
    for i in range(len(maxoutnp)):
        bioT = []
        for j in range(len(maxoutnp[i])):
            if labels[i][j] != -100:
                bioT.append(config['id2label'][str(maxoutnp[i][j])])
        bio+=bioT
    labels = []

    for i in range(len(bio)):
        tag = bio[i]
        if tag != "O":
            splited = tag.split('-')
            if splited[0] == 'B':
                result["labels"][str(i)] = {}
                result["labels"][str(i)]["Type"] = splited[1]
                result["labels"][str(i)]["StartPosition"] = i
                result["labels"][str(i)]["EndPosition"] = i
                result["labels"][str(i)]["Name"] = tokens[i]
                current = i
            else:
                result["labels"][str(current)]["EndPosition"]+=1
                result["labels"][str(current)]["Name"]+= " " + tokens[i]
                


    #TRIGGERS

    task = 'triggers'
    print(task)
    path = 'Models/' + language + '/' + task + '/'
    configPath = open(path + 'config.json','r')
    config = json.load(configPath)
    model = XLMRobertaForTokenClassification.from_pretrained(path)
    model = model.to(device)
    model.eval()
    tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base',use_fast=True)
    tokensArg = []
    triggers = []
    tokenized_input, labels = tokenize_and_align_labels([tokens],tokenizer,device)
    out = model(**tokenized_input)['logits']
    maxout = torch.argmax(out,dim=2)
    maxout = maxout.to('cpu')
    maxoutnp = maxout.numpy()
    bio = []
    for i in range(len(maxoutnp)):
        bioT = []
        for j in range(len(maxoutnp[i])):
            if labels[i][j] != -100:
                bioT.append(config['id2label'][str(maxoutnp[i][j])])
        bio+=bioT
    labels = []
    for i in range(len(bio)):
        for j in range(len(bio[i])):
            if bio[i][j] != 'O':
                tokenArg = []
                for w in range(len(tokens)):
                    if w == j:
                        tokenArg.append("$$$")
                        tokenArg.append(tokens[z][w]) #Z hau ezdakit nondik atea den ERROREA TODO
                        tokenArg.append("$$$")
                    else:
                        tokenArg.append(tokens[z][w])
                tokensArg.append(cp.deepcopy(tokenArg))
    
    triggerPos = []
    for i in range(len(bio)):
        tag = bio[i]
        if tag != "O":
            splited = tag.split('-')
            if splited[0] == 'B':
                result["triggers"][str(i)] = {}
                result["triggers"][str(i)]["Type"] = splited[1]
                result["triggers"][str(i)]["StartPosition"] = i
                result["triggers"][str(i)]["EndPosition"] = i
                result["triggers"][str(i)]["Name"] = tokens[i]
                result["triggers"][str(i)]["Arguments"] = {}
                current = i
                triggerPos.append(str(i))
            else:
                result["labels"][str(current)]["EndPosition"]+=1
                result["labels"][str(current)]["Name"]+= " " + tokens[i]


    #ARGUMENTS

    task = 'arguments'
    print(task)
    path = 'Models/' + language + '/' + task + '/'
    configPath = open(path + 'config.json','r')
    config = json.load(configPath)
    model = XLMRobertaForTokenClassification.from_pretrained(path)
    model = model.to(device)
    model.eval()
    tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base',use_fast=True)
    for z in range(len(tokensArg)):
        tokenized_input, labels = tokenize_and_align_labels([tokensArg[z]],tokenizer,device)
        out = model(**tokenized_input)['logits']
        maxout = torch.argmax(out,dim=2)
        maxout = maxout.to('cpu')
        maxoutnp = maxout.numpy()
        bio = []
        for i in range(len(maxoutnp)):
            bioT = []
            for j in range(len(maxoutnp[i])):
                if labels[i][j] != -100:
                    bioT.append(config['id2label'][str(maxoutnp[i][j])])
            bio+=bioT
        labels = []
        for i in range(len(bio)):
            tag = bio[i]
            if tag != "O":
                splited = tag.split('-')
                if splited[0] == 'B':
                    result["triggers"][triggerPos[z]]["Arguments"][str(i)]["Type"] = splited[1]
                    result["triggers"][triggerPos[z]]["Arguments"][str(i)]["StartPosition"] = i
                    result["triggers"][triggerPos[z]]["Arguments"][str(i)]["EndPosition"] = i
                    result["triggers"][triggerPos[z]]["Arguments"][str(i)]["Name"] = tokens[i]
                    current = i
                    triggerPos.append(i)
                else:
                    result["labels"][triggerPos[z]]["Arguments"][str(current)]["EndPosition"]+=1
                    result["labels"][triggerPos[z]]["Arguments"][str(current)]["Name"]+= " " + tokens[i]
 

    with open('result.json', 'w') as fp:
        json.dump(result, fp)
  

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
    main()