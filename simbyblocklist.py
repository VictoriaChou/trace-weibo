# -*- coding: utf-8 -*-
import numpy as np

def load_blog(list1,list2):
    # 读入两条分词好的微博文本
    file = open('processed_microblog1.txt', 'r')
    for lines in file:
        if lines.strip() != '':
            list1.append(lines.strip().rstrip())
    file.close()
    file = open('processed_microblog2.txt', 'r')
    for lines in file:
        if lines.strip() != '':
            list2.append(lines.strip().rstrip())
    file.close()

def get_similarity(a,size_of_list1,size_of_list2):
    for i in range(size_of_list1):
        for j in range(size_of_list2):
            file = open('data.txt', 'r')
            for lines in file:
                if lines.find(list1[i] + ',' + list2[j]) >= 0 or lines.find(list2[j] + ',' + list1[i]) >= 0:
                    a[i][j] = float(lines[lines.find(":") + 1:])
                    break
            file.close()

def get_list_pair(list1,list2,a):
    list_pair={}
    threshold = 0.5
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

list1=[]
list2=[]
load_blog(list1,list2)
size_of_list1=len(list1)
size_of_list2=len(list2)

a=np.zeros(shape=(size_of_list1,size_of_list2))
get_similarity(a,size_of_list1,size_of_list2)
list_pair=get_list_pair(list1,list2,a)
list_first=[]
list_second=[]
for i in range(len(list_pair)):
    list_first.append(list_pair.keys()[i])
    list_second.append(list_pair[list_pair.keys()[i]])
list_first_sort=[]
list_second_sort=[]
for i in range(len(list1)):
    for j in range(len(list_first)):
        if list1[i]==list_first[j]:
            list_first_sort.append(list1[i])
for i in range(len(list2)):
    for j in range(len(list_second)):
        if list2[i]==list_second[j]:
            list_second_sort.append(list2[i])
blocklist=get_block_list(list_first_sort,list_second_sort)

r1=np.arange(len(blocklist))
r2=[]
for i in range(len(blocklist)):
    tmp=blocklist[i][0]
    for j in range(len(list_second_sort)):
        if list_pair[tmp]==list_second_sort[j]:
            r2.append(j)
            break
sim_word=2*len(list_first_sort)*1.0/(len(list1)+len(list2))
sim_order=1-np.sqrt(np.sum(np.square(r1-r2)))/np.sqrt(np.sum(np.square(r1+r2)))
a_coefficient=0.5
b_coefficient=0.5
sim=a_coefficient*sim_word+b_coefficient*sim_order
print sim












