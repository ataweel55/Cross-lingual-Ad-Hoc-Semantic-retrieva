import csv
import numpy as np
import pandas as pd
from scipy import spatial
from math import *
import re
from numpy import genfromtxt
from sklearn.metrics.pairwise import cosine_similarity

vocab = {}
list_of_query = []
print 'query?'
query = raw_input()
#divide query for each word, make a list of words
list_of_query = re.split('\s+', str(query))
# the dictionary of whole vocabulary
# key = word; value = number of word given to us
with open('vocab.txt', 'r') as fvocab:
    for a in range(20000):
        m = fvocab.readline()
        m = re.split('\s+', m)
        vocab[m[1]] = m[0]
#print(vocab)  # the dictionary of whole vocabulary
# the part of dictionary with only our query
final_vocab = {}  # the dictionary with only our part of the query
for q in range(len(list_of_query)):
    if list_of_query[q] in vocab:
        final_vocab[list_of_query[q]] = vocab[list_of_query[q]]

average = {} # dictionary with the word's number and the list of all tfidf for this word
rez = {}  # dictioanry with the word's number and the average tfidf
with open('train_en.txt', 'r') as t:
    for m in t.readline():
        line = t.readline()
        line = re.split('\s+', line)
        if line[1] in average:
            average[line[1]].append(float(line[2]))
        else:
            average[line[1]] = [float(line[2])]
for s in average:
    rez[s] = sum(average[s]) / float(len(average[s]))
englishdict = {}
#make dictionary from english word's embeddings vectors
with open("short english.txt", "r") as f:
    for line in f.xreadlines():
        line = line.decode("utf-8")
        columns = line.strip().split()
        englishdict[columns[0]] = [float(n) for n in columns[1:]]

print 'done english '
m = genfromtxt('m.csv', delimiter=',')
word_embedin = {}
query_embedding = [0 for x in range(300)]

flag = 0
for word in final_vocab:
    if final_vocab[word] in rez and word in englishdict:
        tmp = []
        tmp = np.dot(englishdict[word], m)  # "spanish" emb
        tmp = np.dot(tmp, rez[final_vocab[word]])  # dot product tf and spanish emb
        flag += rez[final_vocab[word]]
        query_embedding = np.add(tmp, query_embedding)  # nominator of final fraction

query_embedding = np.dot(query_embedding, flag ** (-1))  # the final query embedding
print query_embedding
# rez[final_vocab[word]] - average tfidf for each word in the query

espanol ={}
#make dictionary from spanish embeddings to compare
with open("Spanish.csv", "r") as file:
    for line in file:
        line = re.sub(',', ' ', str(line))
        line = re.sub('\n', ' ', str(line))
        line = re.split(" ", str(line))
        if not line[1].isalpha():
            if fabs(float(line[1])) >= 0.0000001:
                if (len(line) > 299):
                    espanol[line[0]] = [float(n) for n in line[1:301]]
print 'done spanish dataset'
norm1 = np.linalg.norm(query_embedding)
print("How many relevant you want: ")
relevant = raw_input()

flag = 0
corrdocs = {}
morerelevant = []
for z in espanol.keys():
    vec2 = espanol[z]
    #norm2 = np.linalg.norm(vec2)
    cos = cosine_similarity([query_embedding], [vec2])
    #cos = np.dot(query_embedding, vec2) / np.dot(norm1, norm2)
    #this works slowly :)
    #cos = cosine_similarity([query_embedding], [vec2])
    morerelevant.append(cos)
    corrdocs[flag] = z
    flag += 1

k = int(relevant)
lastcnt = 0
# and finally print just some input number of most relevant documents
while lastcnt < k:
    print corrdocs[morerelevant.index(max(morerelevant))]
    morerelevant.pop(morerelevant.index(max(morerelevant)))
    lastcnt += 1