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
    collection = sina_db.recent_tweets
    items = collection.find()
    items = [item["content"] for item in items]
    return items

def list2txt(contextlist):
    """
    写进txt文件
    """
    with open("tweets_recent.txt", "w+") as tweets:
        for context in contextlist:
            tweets.write(context + '\n')

def clean_txt(context):
    """
    去除停用词
    """
    f1 = open('stopwords.txt','r')
    stopwords = [l.strip() for l in f1.readlines()]
    f1.close()
    f2 = open('common.txt', 'r')
    commonwords = [l.strip() for l in f2.readlines()]
    f2.close()
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
    context = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）《》；：“”-]+", "",context)
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
    context_seg = jieba.cut(context, cut_all = False)

    # 去除停用词
    tweets = [t for t in context_seg if t not in stopwords]
    # 去除微博高频无用词
    tweets_clean = [word for word in tweets if word not in commonwords]
    return tweets_clean


def main():
    # tweets = get_tweets()
    # list2txt(tweets)
    with open ("tweets_recent.txt") as tweets:
        lines = tweets.readlines()
        for line in lines:
            line_clean = clean_txt(line)
            with open('tweets_recent_result.txt', 'a') as f2:
                f2.write(" ".join(line_clean))

if __name__ == '__main__':
    main()
       
    