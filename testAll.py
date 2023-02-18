from transformers import XLMRobertaForTokenClassification,  AutoTokenizer
import torch
import os
import json
import copy as cp
from pdb import set_trace
from seqeval.metrics import f1_score
from seqeval.metrics import accuracy_score


def main():
    device = torch.device(type='cuda',index=0)
    for language in os.listdir('Models'):
        print("****************************************************")
        print(language)
        test = 'MEE_BIO/' + language + '/test.json'
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
        path = 'Models/all/' + task + '/'
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
        accuracy = accuracy_score(entity,bio)
        print('Accuracy: ' + str(accuracy))
        print('f1: ' + str(f1))


        #TRIGGERS
    
        task = 'triggers'
        print("----------------------------------------------------")
        print(task)
        path = 'Models/all/' + task + '/'
        configPath = open(path + 'config.json','r')
        config = json.load(configPath)
        model = XLMRobertaForTokenClassification.from_pretrained(path)
        model = model.to(device)
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base',use_fast=True)
        tokensArg = []
        linesPre = []
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
            labels = []
            for j in range(len(bio[z])):
                if bio[z][j] != 'O':
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
        f1 = f1_score(triggers,bio,zero_division='0')
        accuracy = accuracy_score(triggers,bio)
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
        path = 'Models/all/' + task + '/'
        configPath = open(path + 'config.json','r')
        config = json.load(configPath)
        model = XLMRobertaForTokenClassification.from_pretrained(path)
        model = model.to(device)
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base',use_fast=True)
        bio = []
        bioPipe=[]
        founded = 0
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
        goldPipe=[]
        for z in range(len(tokensArg)):
            for i in range(len(linesGold)):
                if linesGold[i] == linesPre[z] and tokensArg[z] == tokensArgGold[i]:
                    founded+=1
                    goldPipe.append(arguments[i])
                    tokenized_input, labels = tokenize_and_align_labels([tokensArg[z]],tokenizer,device)
                    out = model(**tokenized_input)['logits']
                    maxout = torch.argmax(out,dim=2)
                    maxout = maxout.to('cpu')
                    maxoutnp = maxout.numpy()
                    for i in range(len(maxoutnp)):
                        bioT = []
                        for j in range(len(maxoutnp[i])):
                            if labels[i][j] != -100:
                                bioT.append(config['id2label'][str(maxoutnp[i][j])])
                        bioPipe.append(bioT)
                    break
        f1 = f1_score(arguments,bio,zero_division='0')
        accuracy = accuracy_score(arguments,bio)
        f1Pipe = f1_score(goldPipe,bioPipe,zero_division='0')*(founded/len(linesGold))
        print('Accuracy: ' + str(accuracy))
        print('f1: ' + str(f1))
        print('f1Pipe: ' + str(f1Pipe))



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