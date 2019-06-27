import csv
import numpy as np
from numpy import genfromtxt
import re

print "starting....."
english = {}
spanish = {}

#Building English Dictionary

with open("short english.txt", "r") as f: #short dictionary is a shorter version of the original English embeding having only the top 200K words
	for line in f.xreadlines():
		line = line.decode("utf-8")
		columns = line.strip().split()
		english[columns[0]] = [float(n) for n in columns[1:]]
print 'done english '

#Building Spanish Dictionary
with open("short spanish.txt", "r") as f:  #short spanish is a shorter versision of the original Spanish embeddings having 200K term
	for line in f.xreadlines():
		line = line.decode("utf-8")
		columns = line.strip().split()
		spanish[columns[0]] = [float(n) for n in columns[1:]]
		
print 'done spanish'

################################################################################################################################################

e_f =open ('enlighs final.txt', 'w') #found english words with their corresponding embeddings
s_f = open ('spanish final.txt', 'w') #found spanish words with their corresponding embeddings
new_pair = open ('new pair.csv', 'w') #found pairs kept as a referance

#open csv file with pairs and assign them to temp_list
with open ('English to Spanish (duplicate removed) - 6000 word no stopwords.csv','r') as f_pair:
	reader = csv.reader(f_pair)
	temp_list = list(reader)

counter = 0

#Lookup for pairs' embdeddings
for x in  range(len(temp_list)):
	english_word = temp_list[x][0]
	spanish_word = temp_list[x][1]
	#print english_word
	#print spanish_word

	if english_word in english and spanish_word in spanish:
		em1 = english[english_word]
		em1 = str(em1)
		em2 = spanish[spanish_word]
		em2 = str(em2) 
		e_f.write(em1)
		e_f.write("\n")
		s_f.write(em2)
		s_f.write('\n')
		new_pair.write(english_word)
		new_pair.write(",")
		new_pair.write(spanish_word)
		new_pair.write('\n')

		counter = counter + 1
print counter
print "DONE"
e_f.close()
s_f.close()
new_pair.close()
#############################################################
#reformating the files in preparation for building the matrix
#############################################################
f = open ('english final striped.csv', 'w')
m = open ('spanish final stripped.csv', 'w')
with open ('enlighs final.txt', 'r') as source:
	for line in source:
		line =line.strip()
		line = re.sub('\[', '', line)
		line = re.sub('[\]]', '', line)
		line = re.sub(' ', '', line)
		#print line
		
		f.write(line)
		f.write("\n")		
f.close()

with open('spanish final.txt', 'r') as s_source:
	for line in s_source:
		line =line.strip()
		line = re.sub('\[', '', line)
		line = re.sub('[\]]', '', line)
		line = re.sub(' ', '', line)
		m.write(line)
		m.write("\n")
m.close()

print 'done'
#loaded_data = np.loadtxt('enlighs final.txt', dtype='float')
count_english = 0 
count_spanish = 0
with open ('spanish final stripped.csv' , 'r') as english_final:
	for line in english_final:
		count_english = count_english +1

with open ('english final striped.csv', 'r') as spanish_final:
	for line in spanish_final:
		count_spanish = count_spanish +1

print count_english
print count_spanish

####################
#building the matrix
####################

s = genfromtxt('english final striped.csv', delimiter=',') #import the found english embeddings 
t = genfromtxt('spanish final stripped.csv', delimiter = ',') #import the found spanish embeddings

s_plus = np.linalg.pinv(s)
m =np.dot(s_plus,t)

temp =np.dot(s_plus,s)

#writing the matrixes to CSV files
np.savetxt('s.csv', s, delimiter=',', fmt= '%.5f')
np.savetxt('t.csv', t, delimiter=',' ,fmt='%.5f')
np.savetxt('s_plus.csv', s_plus, delimiter=',' ,fmt='%.5f')
np.savetxt('m.csv', m, delimiter=',' ,fmt='%.5f')

print 'DONE /ALL'