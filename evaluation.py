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
print (a) #number of right english documents

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
print (b) #number of right espanol documents
flag = 0
out = open('ranked.csv', 'w')

ap = 0

#to calculate cosine manually really faster than prepared function! Thanks :)
for x in english.keys():
	vec1 = english[x]
	maxcos = -1.
	corr_doc = 0
	dev = 1
	norm1 = np.linalg.norm(vec1)
	if x in espanol:
		for y in espanol.keys():
			vec2 = espanol[y]
			norm2 = np.linalg.norm(vec2)
			exact = espanol[x]
			compare = np.dot(vec1, exact)/np.dot(norm1, np.linalg.norm(exact))
			newcos = np.dot(vec1, vec2)/np.dot(norm1, norm2)
			if (compare<newcos):
				dev+=1
			if (newcos > maxcos):
				maxcos = newcos
				corr_doc = y
		prec = 1 / dev
		out.write(str(x))
		out.write(" ")
		out.write(str(corr_doc))
		out.write(" ")
		out.write("1/")
		out.write(str(dev))
		out.write(" ")
		out.write(str(prec))
		out.write("\n")
		prec = 1/dev
		ap+=prec
		flag+=1
		print(str(x)+" "+str(corr_doc) + " " + "1/"+ str(dev)+" "+str(prec))
		if flag%100 == 0:
			print("already: " + str(flag))
out.close()
print(ap)
print(flag)
average = ap/flag
print(average)

print("DONE")