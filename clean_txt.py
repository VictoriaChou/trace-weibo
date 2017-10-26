# -*- coding: utf-8 -*-
# 微博数据清洗
# Author: Zhou Fuxing
import pymongo
import re

def clean_txt(context):
    """
    去除停用词
    """
    f1 = open('stopwords.txt','r')
    stopwords = [l.strip() for l in f1.readlines()]
    f1.close()
    context = re.sub("http://[a-zA-Z./\d]*","",context)
    # remove emojo
    context = re.sub("\[.{0,12}\]","",context)
    # extract and remove tag
    context = re.sub("#.{0,30}#","",context)
	# extract and remove @somebody
    context = re.sub("@([^@]{0,30})\s","",context)
    context = re.sub("@([^@]{0,30})）","",context)
	# lower the english characaters
    context = context.lower()
    # remove punctuation
    context = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "",context)
    context = re.sub("[【】╮╯▽╰╭★→「」]+","",context)
    # remove wirte space
    context = re.sub("\s","",context)
    # remove digits
    context = re.sub("\d","",context)
    # remove ....
    context = re.sub("\.*","",context)
    context = re.sub("\t", "",context)
    context = re.sub("\n","",context)
    context = re.sub(" ","",context)
    return context