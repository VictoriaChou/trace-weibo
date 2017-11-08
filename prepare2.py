# -*- coding: utf-8 -*-

def process(file_testmeanings,file_newtestmeanings,file_microblog):
    buffer = ""
    for lines in file_testmeanings:
        if (lines.find(':') >= 0 or lines.strip() == "") and buffer.find(':') >= 0:
            buffer = lines
            continue
        else:
            if (buffer.find('...') < 0 and buffer.strip() != ''):
                file_newtestmeanings.write(buffer)
            if buffer.find(':') >= 0:
                file_microblog.write(buffer[1:])
            buffer = lines
    if (buffer.find('...') < 0 and buffer.strip() != ''):
        file_newtestmeanings.write(buffer)
    file_testmeanings.close()
    file_microblog.close()



file1=open('TestMeanings_list1.txt','r')
file2=open('TestMeanings_list2.txt','r')
file3=open('NewTestMeanings.txt','w')
file4=open('microblog1.txt','w')
file5=open('microblog2.txt','w')  #直接覆盖上去

process(file1,file3,file4)
process(file2,file3,file5)
file3.close()

#接下来把NewTestMeanings.txt给hownet 换个数据文件保存成data.txt 再把data.txt换成utf-8编码就行了！
#同时也要把microblog1.txt microblog2.txt转成utf-8








