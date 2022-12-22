from transformers import XLMRobertaForTokenClassification,  AutoTokenizer
import torch
import os
import json
import copy as cp
from pdb import set_trace


def main():
    device = torch.device(type='cuda',index=0)
    language = "english"
    for task in os.listdir('Models/' + language):
        print(task)
        path = 'Models/' + language + '/' + task + '/'
        configPath = open(path + 'config.json','r')
        config = json.load(configPath)
        model = XLMRobertaForTokenClassification.from_pretrained(path)
        model = model.to(device)
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base')
        tokenized_input, labels = tokenize_and_align_labels([["Alice", "is", "the", "boss", "of", "XYZ", "company"], ["Alice", "is", "the", "boss", "of", "XYZ", "company"]],tokenizer,device)
        #parameters = torch.load(path)
        #model.to(device)
        #model.load_from_state_dict(parameters)
        #pipe = pipeline("ner", model=model, tokenizer=tokenizer,device=device)
        out = model(**tokenized_input)['logits']
        maxout = torch.argmax(out,dim=2)
        maxout = maxout.to('cpu')
        bio = []
        maxoutnp = maxout.numpy()
        for i in range(len(maxoutnp)):
            bioT = []
            for j in range(len(maxoutnp[i])):
                if labels[i][j] != -100:
                    bioT.append(config['id2label'][str(maxoutnp[i][j])])
            bio.append(cp.deepcopy(bioT))
        print(bio)        

# Tokenize all texts and align the labels with them.
def tokenize_and_align_labels(examples,tokenizer,device):
    tokenized_inputs = tokenizer(examples, truncation=True, is_split_into_words=True,return_tensors='pt').to(device)

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