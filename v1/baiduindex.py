import os
import random
import time

from Indexation import *
from baidulogin import getcookies

if __name__=='__main__':
    DEBUG=True
    if not os.path.exists('input.csv'):
        demo=[
            ['关键词','模式','最近n天','开始时间','结束时间'],
            ['示例','0','30','20160626','20180702','←请不要在此行输入数据'],
            ['仙剑','0','7','',''],
            ['幻璃镜','0','7','',''],
            ['百度','0','30','',''],
            ['指数','0','30','',''],
            ['爬虫','0','30','',''],
            ]
        with open('input.csv','w') as f:
            s=''
            for l in demo:
                s+=','.join(l)+'\n'
            f.write(s)
        input('请在input.csv中按照示例输入数据，完成后回到程序窗体回车')
    with open('input.csv','r') as f:
        keywords=[]
        for line in f:
            keywords.append(line.replace('\n','').split(','))
    keywords=keywords[2:]
    kws=[]
    num=0
    while num<len(keywords):
        words=[keywords[num]]
        num+=1
        if num<len(keywords) and keywords[num-1][1:5]==keywords[num][1:5]:
            words.append(keywords[num])
            num+=1
            if num<len(keywords) and keywords[num-1][1:5]==keywords[num][1:5]:
                words.append(keywords[num])
                num+=1
        kws.append(words)
    ls=[['关键词','开始时间','结束时间','时间跨度（日）','整体均值','PC均值','移动均值']]
    indexes=[]
    for kw in kws:
        print('当前收集词语：'+','.join(list(map(lambda x:x[0],kw))))
        while True:
            try:
                if not kw[0][1] or kw[0][1]=='0':
                    indexes+=BaiduIndex(list(map(lambda x:x[0],kw)),int(kw[0][2])).indexes
                elif kw[0][1]=='1':
                    indexes+=BaiduIndex(list(map(lambda x:x[0],kw)),'|'.join(kw[0][3:5])).indexes
                else:
                    print('模式参数有误！名称：{} 位置：第{}行'.format(kw[0][0],kws.index(kw)+3))
                time.sleep(3)
                break
            except TypeError:
                print('数据请求发生错误，正在尝试重新获取cookies...')
                print(e)
                getcookies()
                
            
    for index in indexes:
        ls.append(index.average())
    if not os.path.exists('output'):
        os.mkdir('output')
    with open('output/'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'.csv','w') as f:
        s=''
        for l in ls:
            s+=','.join(list(map(str,l)))+'\n'
        f.write(s)
    print('本次爬取已完成，请到output文件夹内寻找（当前以文件生成时间命名）')
    input('Press <Enter>')

