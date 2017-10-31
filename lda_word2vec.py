# -*- coding: utf-8 -*-
# 基于word2vec拓展主题的lda文本建模
# Author: Zhou Fuxing

import numpy as np
from gensim import corpora, models, similarities
from db2text import get_tweets
from db2text import clean_txt

tweets = get_tweets()
clean_tweets = []
for tweet in tweets:
    clean_tweet = clean_txt(tweet)
    clean_tweets.append(clean_tweet)

# 用文本构建Gensim字典
dictionary = corpora.Dictionary(clean_tweets)
dic_keys = list(dictionary.key())
print(dic_keys[0])
# 将字典转化为词袋模型(bag of words)作为参考
corpus = [dictionary.doc2bow(tweet) for tweet in clean_tweets]
lda = models.LdaModel(corpus, num_topics = 200,
                        id2word = dictionary,
                        update_exery = 5,
                        chunksize = 10000,
                        passes = 100)

lda.show_topics()
topics_matrix = lda.show_topics(formatted = False, num_words = 20, num_topics = 200)
# 找到主题中每个词在语料库中对应的词向量
topics =[topics[1] for topics in topics_matrix]
topics_word2vec = []
model = models.word2vec.Word2Vec.load('微博.model')
for topic in topics:
    topics_word2vec.append((model.wv[word[0]],word[1]) for word in topic)
print(topics_word2vec)

