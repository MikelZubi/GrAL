from transformers import XLMRobertaForTokenClassification,  AutoTokenizer
import torch
import os
import json
import copy as cp
from pdb import set_trace
from sklearn.metrics import f1_score


def main():
    device = torch.device(type='cuda',index=0)
    for language in os.listdir('Models'):
        print("****************************************************")
        print(language)
        test = 'MEE_BIO/' + language + '/test.json'
        testR =  open(test, "r")
        tokens = []
        entity = []
        triggers = []
        for line in testR:
            data = json.loads(line)
            tokens.append(data['tokens'])
            entity.append(data['labels'])
            triggers.append(data['triggers'])
        testR.close()

        #ENTITY

        task = 'entity'
        print("----------------------------------------------------")
        print(task)
        path = 'Models/' + language + '/' + task + '/'
        configPath = open(path + 'config.json','r')
        config = json.load(configPath)
        model = XLMRobertaForTokenClassification.from_pretrained(path)
        model = model.to(device)
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base',use_fast=True)
        accuracy = 0
        f1 = 0
        for z in range(len(tokens)):
            tokenized_input, labels = tokenize_and_align_labels([tokens[z]],tokenizer,device)
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
                    if bio[i][j] == entity[z][j]:
                        accuracy+= 1 / len(bio[i])
                    if entity[z][j] != 'O' and entity[z][j] not in labels:
                        labels.append(entity[z][j])
                    if bio[i][j] != 'O' and bio[i][j] not in labels:
                        labels.append(bio[i][j])
                f1 += f1_score(entity[z],bio[i],average='micro',labels=labels,zero_division=0)
        accuracy = accuracy / len(tokens)
        f1 = f1 / len(tokens)
        print('Accuracy: ' + str(accuracy))
        print('f1: ' + str(f1))


        #TRIGGERS
    
        task = 'triggers'
        print("----------------------------------------------------")
        print(task)
        path = 'Models/' + language + '/' + task + '/'
        configPath = open(path + 'config.json','r')
        config = json.load(configPath)
        model = XLMRobertaForTokenClassification.from_pretrained(path)
        model = model.to(device)
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base',use_fast=True)
        accuracy = 0
        f1 = 0
        tokensArg = []
        linesPre = []
        for z in range(len(tokens)):
            tokenized_input, labels = tokenize_and_align_labels([tokens[z]],tokenizer,device)
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
                    if bio[i][j] == triggers[z][j]:
                        accuracy+= 1 / len(bio[i])
                    if triggers[z][j] != 'O' and triggers[z][j] not in labels:
                        labels.append(triggers[z][j])
                    if bio[i][j] != 'O':
                        if bio[i][j] not in labels:
                            labels.append(bio[i][j])
                        tokenArg = []
                        linesPre.append(z)
                        for w in range(len(tokens[z])):
                            if w == j:
                                tokenArg.append("$$$")
                                tokenArg.append(tokens[z][w])
                                tokenArg.append("$$$")
                            else:
                                tokenArg.append(tokens[z][w])
                        tokensArg.append(cp.deepcopy(tokenArg))
                f1 += f1_score(triggers[z],bio[i],average='micro',labels=labels,zero_division=0)
        accuracy = accuracy / len(tokens)
        f1 = f1 / len(tokens)
        print('Accuracy: ' + str(accuracy))
        print('f1: ' + str(f1))


        #ARGUMENTS

        task = 'arguments'
        print("----------------------------------------------------")
        print(task)
        test = 'MEE_BIO/' + language + '/test_arg.json'
        testR =  open(test, "r")
        tokensArgGold = []
        arguments = []
        linesGold = []
        for line in testR:
            data = json.loads(line)
            tokensArgGold.append(data['tokens'])
            arguments.append(data['arguments'])
            if language != 'all':
                linesGold.append(data['line'])
            else:
                linesGold.append(data['lineAll'])
        testR.close()
        path = 'Models/' + language + '/' + task + '/'
        configPath = open(path + 'config.json','r')
        config = json.load(configPath)
        model = XLMRobertaForTokenClassification.from_pretrained(path)
        model = model.to(device)
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base',use_fast=True)
        accuracy = 0
        f1 = 0
        for z in range(len(tokensArg)):
            found = False
            for i in range(len(linesGold)):
                #Hemen all-ek fallatzen du, konpondu
                if linesGold[i] == linesPre[z]:
                    if tokensArg[z] == tokensArgGold[i]:
                        found = True
                        pos = i
                        break

            if found:
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
                for i in range(len(bio)):
                    for j in range(len(bio[i])):
                        if bio[i][j] == arguments[pos][j]:
                            accuracy+= 1 / len(bio[i])
                        if arguments[pos][j] != 'O' and arguments[pos][j] not in labels:
                            labels.append(arguments[pos][j])
                        if bio[i][j] != 'O' and bio[i][j] not in labels:
                            labels.append(bio[i][j])
                    f1 += f1_score(arguments[pos],bio[i],average='micro',labels=labels,zero_division=0)
        accuracy = accuracy / len(tokensArgGold)
        f1 = f1 / len(tokensArgGold)
        print('Accuracy: ' + str(accuracy))
        print('f1: ' + str(f1))



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