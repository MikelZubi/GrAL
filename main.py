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
    text = ""
    nlp = spacy.blank("xx")
    doc = nlp(text)
    tokens = []
    for token in doc:
        tokens.append(token.text)
    
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
        bio.append(bioT)
    labels = []

    #TODO Zeoze in lortutako datuekin, nonbaitte txukun idatzi...
        


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
        bio.append(bioT)
    labels = []
    for i in range(len(bio)):
        for j in range(len(bio[i])):
            if bio[i][j] != 'O':
                tokenArg = []
                for w in range(len(tokens)):
                    if w == j:
                        tokenArg.append("$$$")
                        tokenArg.append(tokens[z][w])
                        tokenArg.append("$$$")
                        triggers.append(tokens[z][w])
                    else:
                        tokenArg.append(tokens[z][w])
                tokensArg.append(cp.deepcopy(tokenArg))
    
    #TODO Zeoze in lortutako datuekin, nonbaitte txukun idatzi...


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
            bio.append(bioT)
        labels = []
        
        #TODO Zeoze in lortutako datuekin, nonbaitte txukun idatzi...

  

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