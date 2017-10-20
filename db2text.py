# -*- coding: utf-8 -*-
# 创建微博语料库
# Author: Zhou Fuxing
import pymongo
import jieba
import re

def get_tweets():
    """
    获取数据库中的数据
    """
    client = pymongo.MongoClient('101.132.76.124', 27017)
    sina_db = client.sina_db
    print('Connected to Mongodb!')
    collection = sina_db.tweets
    items = collection.find()
    items = [item["content"] for item in items]
    return items

def list2txt(contextlist):
    """
    写进txt文件
    """
    with open("tweets.txt", "w+") as tweets:
        for context in contextlist:
            tweets.write(context + '\n')

def clean_txt(context):
    """
    去除停用词
    """
    context = re.sub("http://[a-zA-Z./\d]*","",context)
    # remove emojo
    context = re.sub("\[.{0,12}\]","",context)
    # extract and remove tag
    context = re.sub("#.{0,30}#","",context)
	# extract and remove @somebody
    context = re.sub("@([^@]{0,30})\s","",context)
    context = re.sub("@([^@]{0,30})）","",context)
	# lower the english characaters
    context  = context.lower()
    return context


def main():
    tweets = get_tweets()
    list2txt(tweets)
    with open ("tweets.txt") as tweets:
        lines = tweets.readlines()
        for line in lines:
            line = clean_txt(line)
            line.replace('\t', '').replace('\n', '').replace(' ','')
            seg_list = jieba.cut(line, cut_all = False)
            with open('tweets_result.txt', 'a') as f2:
                f2.write(" ".join(seg_list))

if __name__ == '__main__':
    main()
       
    