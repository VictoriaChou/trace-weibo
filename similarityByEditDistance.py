#encoding: utf-8
from __future__ import division 
import jieba
import Levenshtein
import numpy as np

def stopwordslist(filepath):  
    stopwords = [line.strip().decode("utf-8") for line in open(filepath, 'r').readlines()]  
    return stopwords  
 
def seg_sentence(sentence):  
    sentence_seged = jieba.cut(sentence.strip())  
    stopwords = stopwordslist('data/stopwords.txt')  
    outstr = ''  
    for word in sentence_seged:  
        if word not in stopwords:  
            if word != '\t':  
                outstr += word  
                outstr += " "  
    return outstr  

def cut_sentence(sentence):
    periods = stopwordslist('data/periods.txt')
    outstr = ''  
    sentence = sentence.strip()
    for char in sentence.decode("utf-8"): 
        if char not in periods:  
            outstr += char 
        else:
            outstr += '^'
    return outstr

def getsim(a,b):
    try:
        return 1- Levenshtein.distance(a,b)/(max(len(a),len(b)))
    except ZeroDivisionError as e:
        return 1

np.set_printoptions(precision=3)
file = open("sim_sample.txt")
line = file.readline()
while line:
    a = cut_sentence(line)
    b = cut_sentence(file.readline())
    a = a.split('^')
    b = b.split('^')
    #ap = [str(item) for item in a]
    for i in range(len(a)):
        print a[i].encode("utf-8"),
    print " "
    for i in range(len(b)):
        print b[i].encode("utf-8"),
    print " "
    sizea, sizeb = len(a),len(b)
    simmatric = np.mat(np.zeros((sizeb,sizea)))
    print sizea, sizeb
    for i in range(sizeb):
        if sizeb == 0:
            continue
        for j in range(sizea):
            #print a[i]
            simmatric[i,j] = getsim(b[i],a[j])
    print simmatric
    print np.max(simmatric,0)
	#print len(a),len(b),Levenshtein.distance(a,b)
    line = file.readline()
