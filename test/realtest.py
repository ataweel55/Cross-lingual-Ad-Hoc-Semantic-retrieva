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
print("How many relevant you want: ")
relevant = raw_input()
list_of_query = re.split('\s+', str(query))

final_vocab = {}  # the dictionary with only our part of the query
for q in range(len(list_of_query)):
    if list_of_query[q] in vocab:
        final_vocab[list_of_query[q]] = vocab[list_of_query[q]]
average = {}
rez = {}  # dictioanry with the word's number and the average tfidf

with open('tf_en.txt', 'r') as t:
    for m in range(4950):
        line = t.readline()
        line = re.split('\s+', line)
        if line[1] in list_of_query:
            if line[1] in average:
                average[line[1]].append(float(line[2]))
            else:
                average[line[1]] = [float(line[2])]
for s in average:
    rez[s] = sum(average[s]) / float(len(average[s]))
#print rez
englishdict ={}
with open("short english.txt", "r") as f:
    for line in f.xreadlines():
        line = line.decode("utf-8")
        columns = line.strip().split()
        englishdict[columns[0]] = [float(n) for n in columns[1:]]

#print 'done english '
flag =0
query_embedding = [0 for x in range(300)]
for word in list_of_query:
    if word in rez and word in englishdict:
        tmp = []
        tmp = np.dot(englishdict[word], m)  # "spanish" emb
        tmp = np.dot(tmp, rez[word])  # dot product tf and spanish emb
        flag += rez[word] #sum of all tfidf
        query_embedding = np.add(tmp, query_embedding)  # nominator of final fraction

query_embedding = np.dot(query_embedding, flag ** (-1))  # the final query embedding
#print query_embedding
espanol = {}
with open("spanish.txt", "r") as file:
    for line in file:
        line = re.sub('   ', ' ', str(line))
        line = re.sub('  ', ' ', str(line))
        line = re.sub(',', ' ', str(line))
        line = re.sub('\n', ' ', str(line))
        line = re.split(" ", str(line))
        if not line[1].isalpha():
            if fabs(float(line[1])) >= 0.0000001:
                if (len(line) > 299):
                    espanol[line[0]] = [float(n) for n in line[1:301]]

#print espanol
norm1 = np.linalg.norm(query_embedding)


flag = 0
corrdocs = {}
morerelevant = {}
for z in espanol.keys():
    vec2 = espanol[z]
    norm2 = np.linalg.norm(vec2)
    #cos = cosine_similarity([query_embedding], [vec2])
    cos = np.dot(query_embedding, vec2) / np.dot(norm1, norm2)
    #morerelevant.append(cos)
    morerelevant[flag] = cos
    corrdocs[flag] = z
    flag += 1

k = int(relevant)
lastcnt = 0

while lastcnt < k:
    remove = max(morerelevant, key = lambda i: morerelevant[i])
    print corrdocs[remove]
    morerelevant.pop(remove)
    corrdocs.pop(remove)
    lastcnt += 1
