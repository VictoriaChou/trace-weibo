# -*- coding: utf-8 -*-
from cleantext_cutwords import clean_text
from cleantext_cutwords import cutwords_and_save

sentence1=u'#英雄联盟S7#【淘汰赛第二日直播】今天是广州站第二个比赛日，@SKT_T1俱乐部 将迎来MSF的挑战，MSF能否带来惊喜，让我们拭目以待！锁定@英雄联盟 微博直播，通过弹幕和现场大屏幕为他们加油打call，有机会赢得精美礼品，评论互动抽取@微博电竞 提供的10份精美奖品！'
sentence2=u'【小组赛第八日直播】今天是#2017全球总决赛#小组赛第八个比赛日，今天的比赛将决出A组出线队伍，目前@EDG电子竞技俱乐部 仅存理论出线可能，但他们绝不放弃！欢迎通过弹幕和现场大屏幕为他们加油！所有比赛结束后，将由@谢天宇iiiiiicon 抽签决定淘汰赛对阵情况！ '
sentence1=clean_text(sentence1)
sentence2=clean_text(sentence2)
cutwords_and_save(sentence1,'microblog1.txt')
cutwords_and_save(sentence2,'microblog2.txt')

#接下来去打开microblog1.txt 和micorblog2.txt去转成ACSN编码并且手动传到hownet
#获取hownet得到的每个词项的义原 并分别保存为TestMeanings_list1.txt TestMeanings_list2.txt