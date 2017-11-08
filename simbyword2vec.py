# -*- coding: utf-8 -*-
import numpy as np
from gensim.models import word2vec
from cleantext_cutwords import clean_text
from cleantext_cutwords import cutwords_and_save


#可以调整的有get_list_pair函数中的threshold
#以及get_finally_sim函数的a_coefficient b_coefficient

def get_list(filename):
    list=[]
    file=open(filename)
    for word in file:
        list.append(word.decode('utf-8').rstrip())
    file.close()
    return list

def create_matrix(list1,list2):
    a=np.zeros(shape=(len(list1),len(list2)))
    return a

def get_word_similarity(word1,word2,model):

    return model.similarity(word1,word2)

def get_all_words_similarity(a,list1,list2,model):
    count=0
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            try:
               a[i][j]=get_word_similarity(list1[i],list2[j],model)
            except KeyError:
                continue
            count=count+1
    return count
def get_list_pair(list1,list2,a):
    list_pair={}
    threshold = 0.3
    flag = 0
    max = -1
    max_x = -1
    max_y = -1
    while flag == 0:
        for i in range(len(list1)):
            for j in range(len(list2)):
                if a[i][j] > max and a[i][j] >= threshold:
                    max = a[i][j]
                    max_x = i
                    max_y = j
                    flag = 1

        if flag:
            list_pair[list1[max_x]] = list2[max_y]
            a[max_x][max_y] = 0
            flag = 0
            max = -1
        else:
            break
    return list_pair

def sort_list(list,list_from_pairs):
    #根据list 排list_from_pairs
    list_sort=[]
    for i in range(len(list)):
        for j in range(len(list_from_pairs)):
            if list[i] == list_from_pairs[j]:
                list_sort.append(list[i])
    return  list_sort

def get_block_list(list_first_sort,list_second_sort):
    blocklist = []
    m = 0
    n = 0
    k = 0
    find_flag = 0
    while n < len(list_first_sort):
        while k < len(list_second_sort) and list_pair[list_first_sort[n]] != list_second_sort[k]:
            k = k + 1
        if k < len(list_second_sort):
            find_flag = 1

        else:
            find_flag = 0
        if find_flag:
            n = n + 1
            k = k + 1
            find_flag = 0
            continue
        else:
            tmp = []
            for i in range(m, n):
                tmp.append(list_first_sort[i])
                if len(tmp) != 0:
                    blocklist.append(tmp)
            k = 0
            m = n
    return blocklist

def get_finally_sim(blocklist,list_second_sort,list_pair):
    r1 = np.arange(len(blocklist))
    r2 = []
    for i in range(len(blocklist)):
        tmp = blocklist[i][0]
        for j in range(len(list_second_sort)):
            if list_pair[tmp] == list_second_sort[j]:
                r2.append(j)
                break
    sim_word = 2 * len(list_first_sort) * 1.0 / (len(list1) + len(list2))
    sim_order = 1 - np.sqrt(np.sum(np.square(r1 - r2))) / np.sqrt(np.sum(np.square(r1 + r2)))
    a_coefficient = 0.8
    b_coefficient = 0.2
    print sim_order
    print sim_word
    sim = a_coefficient * sim_word + b_coefficient * sim_order
    return sim


#先读入微博文本并进行数据清洗 之后写入txttr
sentence1=u'#英雄联盟S7#【淘汰赛第二日直播】今天是广州站第二个比赛日，@SKT_T1俱乐部 将迎来MSF的挑战，MSF能否带来惊喜，让我们拭目以待！锁定@英雄联盟 微博直播，通过弹幕和现场大屏幕为他们加油打call，有机会赢得精美礼品，评论互动抽取@微博电竞 提供的10份精美奖品！'
sentence2=u'【小组赛第八日直播】今天是#2017全球总决赛#小组赛第八个比赛日，今天的比赛将决出A组出线队伍，目前@EDG电子竞技俱乐部 仅存理论出线可能，但他们绝不放弃！欢迎通过弹幕和现场大屏幕为他们加油！所有比赛结束后，将由@谢天宇iiiiiicon 抽签决定淘汰赛对阵情况！ '
sentence1=clean_text(sentence1)
sentence2=clean_text(sentence2)
cutwords_and_save(sentence1,'microblog1.txt')
cutwords_and_save(sentence2,'microblog2.txt')

#从txt中获取词列表
list1=get_list('microblog1.txt')
list2=get_list('microblog2.txt')

#创建一个词关系矩阵
a=create_matrix(list1,list2)

#填充相似度矩阵
model=word2vec.Word2Vec.load('weibo.model')
count=get_all_words_similarity(a,list1,list2,model)

#获取相似度矩阵中相似度较高的词对 字典形式
list_pair=get_list_pair(list1,list2,a)

#将被提取出来的词对重新构建一个list_first 和list_second
list_first=[]
list_second=[]
for i in range(len(list_pair)):
    list_first.append(list_pair.keys()[i])
    list_second.append(list_pair[list_pair.keys()[i]])

#对词列表进行排序
list_first_sort=sort_list(list1,list_first)
list_second_sort=sort_list(list2,list_second)

#获取公共块
blocklist=get_block_list(list_first_sort,list_second_sort)

#计算出两条微博文本的相似度
final_similarity=get_finally_sim(blocklist,list_second_sort,list_pair)
print final_similarity
