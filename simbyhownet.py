# -*- coding: utf-8 -*-
import numpy as np

def load_blog(file):
    list=[]
    for lines in file:
        if lines.strip() != '':
            list.append(lines.strip().rstrip())
    return list

def get_similarity(a,list1,list2):
    for i in range(len(list1)):
        for j in range(len(list2)):
            file = open('data.txt', 'r')
            for lines in file:
                if lines.find(list1[i] + ',' + list2[j]) >= 0 or lines.find(list2[j] + ',' + list1[i]) >= 0:
                    a[i][j] = float(lines[lines.find(":") + 1:])
                    break
            file.close()

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

def sort_list(list,list_origin):
    list_sort=[]
    for i in range(len(list_origin)):
        for j in range(len(list)):
            if list_origin[i] == list[j]:
                list_sort.append(list_origin[i])
    return list_sort

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
    sim = a_coefficient * sim_word + b_coefficient * sim_order
    return sim

#将文本词项加载到List1 list2
file1=open('microblog1.txt','r')
file2=open('microblog2.txt','r')
list1=load_blog(file1)
list2=load_blog(file2)

#创建相似度矩阵
a=np.zeros(shape=(len(list1),len(list2)))

#填充相似度矩阵
get_similarity(a,list1,list2)

#从相似度矩阵中获取词对
list_pair=get_list_pair(list1,list2,a)

#词对元素分别加入list_first list_second
list_first=[]
list_second=[]
for i in range(len(list_pair)):
    list_first.append(list_pair.keys()[i])
    list_second.append(list_pair[list_pair.keys()[i]])

#对list_first list_second根据list1 list2进行排序
list_first_sort=sort_list(list_first,list1)
list_second_sort=sort_list(list_second,list2)

#获取公共块
blocklist=get_block_list(list_first_sort,list_second_sort)

#计算出两条微博文本的相似度
final_similarity=get_finally_sim(blocklist,list_second_sort,list_pair)
print final_similarity












