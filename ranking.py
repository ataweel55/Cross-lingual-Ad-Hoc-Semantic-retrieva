import csv
import numpy as np
import pandas as pd
from scipy import spatial
from math import *
import re
from sklearn.metrics.pairwise import cosine_similarity

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

english = {}
espanol = {}
print("Write number of doc: ")
englishdoc = input()
print("How many relevant you want: ")
relevant = input()
a = 0
with open("English.csv", "r") as f:
	for line in f:
		line = re.sub(',', ' ', str(line))
		line = re.sub('\n', ' ', str(line))
		line = re.split(" ", str(line))
		if not line[1].isalpha():
			if fabs(float(line[1])) >= 0.0000001:
				if (len(line) > 299):
					english[line[0]] = [float(n) for n in line[1:301]]
					a+=1
#print (a) #number of right english documents

b = 0
with open("Spanish.csv", "r") as file:
	for line in file:
		line = re.sub(',', ' ', str(line))
		line = re.sub('\n', ' ', str(line))
		line = re.split(" ", str(line))
		if not line[1].isalpha():
			if fabs(float(line[1])) >= 0.0000001:
				if (len(line) > 299):
					espanol[line[0]] = [float(n) for n in line[1:301]]
					b+=1
#print (b) #number of right espanol documents
flag = 0
ap = 0
print(relevant +' most relevant:')
morerelevant = []
flag = 0
corrdocs = {}
if englishdoc in english.keys() and englishdoc in espanol.keys():
	for z in espanol.keys():
		cos = cosine_similarity([english[englishdoc]], [espanol[z]])
		morerelevant.append(cos)
		corrdocs[flag] = z
		flag+=1
else:
	print("No document with this number, sorry!")
k = int(relevant)
lastcnt = 0

while (lastcnt < k):
	print(corrdocs[morerelevant.index(max(morerelevant))])
	morerelevant.pop(morerelevant.index(max(morerelevant)))
	lastcnt += 1

print("DONE")