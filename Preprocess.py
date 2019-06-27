import numpy as np
from scipy import linalg
import pandas as pd
from math import*
import csv
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

def make_zeros(number):
    return [0] * number

def doc_embeddings(dataframe, doc, allwords, names, number_of_doc = 5):
    list = []
    list_up = []
    multvec = []
    for ind in range(number_of_doc):
        coef = 0.
        coef_up = make_zeros(300)
        for k in range(len(allwords)):
            if allwords[k] in one:
                coef = coef + dataframe[k][ind]
                coef_up += np.multiply(one[allwords[k]], dataframe[k][ind])

        if not coef < 0.00001:
            list_up.append(np.multiply(coef_up, coef ** (-1)))
            doc.write(str(names[ind]))
            doc.write(str(np.multiply(coef_up, coef ** (-1))))
            doc.write("\n")
        else:
            list_up.append(make_zeros(300))
            doc.write(str(names[ind]))
            doc.write(str(make_zeros(300)))
            doc.write("\n")

    return list_up


one = open("1en.txt").read()
two = open("hp_eng.txt").read()
three = open("2en.txt").read()
four = open("3eng.txt").read()
five = open("hp2eng.txt").read()
tffile = open ('tf_en.txt', 'w')
documents = (one,two,three,four,five)
tf = TfidfVectorizer(analyzer='word', min_df = 0, stop_words = 'english')
tfidf_matrix =  tf.fit_transform(documents)
feature_names = tf.get_feature_names()
df = pd.DataFrame(tfidf_matrix.toarray())
for ind in range(5):
    for n in range(len(feature_names)):
        tffile.write((str(ind) + " " + feature_names[n]+ " "+ str(df[n][ind])))
        tffile.write('\n')
tffile.close()
print('done eng')

onesp = open("1es.txt").read()
twosp = open("hp_sp.txt").read()
threesp = open("2es.txt").read()
foursp = open("3sp.txt").read()
fivesp = open("hp2sp.txt").read()
tffilesp = open ('tf_esp.txt', 'w')
documents_sp = (onesp,twosp,threesp,foursp,fivesp)
stop_words = [x for x in open('stopwords-es.txt','r').read().split('\n')]
tf1 = TfidfVectorizer(analyzer='word', min_df = 0, stop_words = stop_words)
tfidf_matrix1 =  tf1.fit_transform(documents_sp)
feature_names1 = tf1.get_feature_names()
df1 = pd.DataFrame(tfidf_matrix1.toarray())
for ind in range(5):
    for n in range(len(feature_names1)):
        tffilesp.write((str(ind) + " " + feature_names1[n]+ " "+ str(df1[n][ind])))
        tffilesp.write('\n')
tffilesp.close()
print('done esp')

one = {}
with open("SBW-vectors-300-min5.txt", "r", encoding='utf-8', errors='replace') as file:
    for a in range(200000):
        try:
            line = file.readline()
            line = re.sub('\[', '', str(line))
            line = re.sub('\'', '', str(line))
            line = re.sub('\]', '', str(line))
            line = re.sub(r'[;,\s]', ' ', str(line))
            line = re.split(" ", str(line))
            if line[0].isalpha() and line[0] in feature_names1:
                for i in range(1,len(line)-1):
                    line[i] = float(line[i])
                one[line[0]] = [float(n) for n in line[1:len(line)-1]]
        except (IndexError, UnicodeEncodeError):
            print("Incorrect format line!")

embfilesp = open ('emb_esp.csv', 'w')
list = doc_embeddings(df1, embfilesp, feature_names1, [0,1,2,3,4])
for l in list:
    embfilesp.write(str(l))
    embfilesp.write('\n')
np.savetxt('list.csv', list, delimiter = ',', fmt = '%.5f')
embfilesp.close()