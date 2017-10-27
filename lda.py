# -*- coding: utf-8 -*-
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
lda = models.LdaModel(corpus, num_topic = 10,
                        id2word = dictionary,
                        update_exery = 5,
                        chunksize = 10000,
                        passes = 100)

lda.show_topics()
topics_matrix = lda.show_topics(formatted = False, num_words = 20)
topics_matrix = np.array(topics_matrix)

topic_words = topics_matrix[:,:,1]
for i in topic_words:
   print([str(word) for word in i])

