# -*- coding: utf-8 -*-
import re
import numpy as np
import jieba
from gensim.models import word2vec
from db2text import clean_txt

text1 = u'柯洁对战AlphaGo。'
text2 = u'AlphaGo帮助围棋文化被更多人了解和熟知，并产生浓厚的兴趣。'
clean_text1 = clean_txt(text1)
clean_text2 = clean_txt(text2)

def get_word_sim(word1, word2):
    # word2vec计算单词间的相似度
    model = word2vec.Word2Vec.load('微博.model')
    return model.similarity(word1, word2)

def get_sen_sim_word2vec(text1, text2):
    # 基于词匹配的文本相似度计算
    sim_sentence = np.zeros((len(clean_text1), len(clean_text2)), dtype = float)
    for i in range(len(clean_text1)):
        for j in range(len(clean_text2)):
            sim = get_word_sim(clean_text1[i], clean_text2[j])
            sim_sentence[i, j] = sim
    return sim_sentence

def get_best_pair(sim_sentence):
    # 找到最大相似的句子对儿
    best_word_set = []
    where_max_sim = sim_sentence.argmax(axis=0)
    for j in range(len(where_max_sim)):
        best_word_set.append((clean_text1[where_max_sim[j]], clean_text2[j]))
    print(best_word_set)
    return best_word_set

def get_sim(best_word_set):           
    sim_word = 2 * len(best_word_set) / (len(clean_text1) + len(clean_text2))
    r1 = np.arange(len(best_word_set))
    r2 = []
    for i in range(len(best_word_set)):
        for j in range(len(clean_text1)):
            if clean_text1[j] == best_word_set[i][0]:
                r2.append(j)
    print(r2)
    sim_order = 1.0 - np.sqrt(np.sum(np.square(r1 - r2)))/np.sqrt(np.sum(np.square(r1 + r2)))
    sim = 0.5 * sim_word + 0.5 * sim_order
    return sim

def main(clean_text1, clean_text2):
    sim_sentence = get_sen_sim_word2vec(clean_text1, clean_text2)
    best_word_set = get_best_pair(sim_sentence)
    sim = get_sim(best_word_set)
    print(sim)
    return sim

if __name__ == '__main__':
    main(clean_text1, clean_text2)
    