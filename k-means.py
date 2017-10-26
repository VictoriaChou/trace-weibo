# -*- coding: utf-8 -*-
# tf-idf建模，k-means聚类
# Author: Zhou Fuxing

import numpy as np
import pandas as pd
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from db2text import get_tweets
from clean_txt import clean_txt

f1 = open('stopwords.txt','r')
stopwords = [l.strip() for l in f1.readlines()]
f1.close()
tfidf_vectorizer = TfidfVectorizer(max_df = 0.8, stop_words = stopwords,
                                min_df = 10, use_idf = True, ngram_range = (1, 3))

tweets = get_tweets()
clean_tweets = []
for tweet in tweets:
    clean_txt(tweet)
    clean_tweets.append(tweet)
tfidf_matrix = tfidf_vectorizer.fit_transform(clean_tweets)
print(tfidf_matrix.shape)

# 获取tf-idf矩阵中的特征表
terms = tfidf_vectorizer.get_feature_names()
num_clusters = 10

km = KMeans(n_clusters = num_clusters)
km.fit(tfidf_matrix)
joblib.dump(km, 'doc_cluster.pkl')
clusters = km.labels_.tolist()

print("Top terms per cluster:")
print()
# 按离质心的距离排列聚类中心，由近到远
order_centroids = km.cluster_centers_.argsort()[:, ::-1] 
 
for i in range(num_clusters):
    print("Cluster %d words:" % i)
 
    for ind in order_centroids[i, :6]: # 每个聚类选 6 个词
        print(ind)
    print() # 空行