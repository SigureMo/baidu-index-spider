import requests
import json
import os
import time

from urllib import parse

from baidulogin import login,getcookies
from siguretools.network_file import Networkfile
from siguretools.config import Config

class BaiduIndex():
    def __init__(self,words,span):
        for n in range(len(words)):
            words[n]=parse.quote(words[n].encode())
        self.words=words
        if isinstance(span,int):
            self.startdate=time.strftime('%Y%m%d',time.localtime(time.time()-60*60*24*span))
            self.enddate=time.strftime('%Y%m%d',time.localtime(time.time()-60*60*24*1))
        elif isinstance(span,str):
            self.startdate=span.split('|')[0]
            self.enddate=span.split('|')[1]
        try:
            with open('data/cookies.json','rb') as c:
                self.cookies=json.loads(c.read().decode())
        except:
            self.cookies=getcookies()
        cook_str=[]
        for cookie in self.cookies:
            cook_str.append(cookie.get('name')+'='+cookie.get('value'))
        cook_str='; '.join(cook_str)
        self.headers={
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'index.baidu.com',
            'Referer': 'http://index.baidu.com/baidu-index-mobile/index.html',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Mobile Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie':cook_str,
            }
        response=self.getIndex()
        self.uniqid=response.get('uniqid')
        datas=response.get('data')
        self.indexes=[]
        for data in datas:
            self.indexes.append(Easyindex(data,self.uniqid,self.headers))
        
    def getIndex(self):
        wordlist=''
        for n in range(len(self.words)):
            wordlist+='&wordlist%5B{}%5D={}'.format(n,self.words[n])
        url='http://index.baidu.com/Interface/Newwordgraph/getIndex?region=0&startdate={}&enddate={}{}'\
             .format(self.startdate,self.enddate,wordlist)
        response=requests.get(url,headers=self.headers)
        return response.json()


class Easyindex():
    def __init__(self,data,uniqid,headers):
        self.uniqid=uniqid
        self.headers=headers
        self.word=data.get('key')
        self.dict=self.getdict()

        def decoder(s,d):
            l=''
            for c in s:
                if c:
                    l+=d[d.index(c)+len(d)//2]
            a=[]
            for i in l.split(','):
                a.append(int(i))
            return a
        self.index_period=data.get('index')[0].get('period')
        self.index_all=decoder(data.get('index')[0].get('_all'),self.dict)
        self.index_pc=decoder(data.get('index')[0].get('_pc'),self.dict)
        self.index_wise=decoder(data.get('index')[0].get('_wise'),self.dict)
        
    def getdict(self):
        url='http://index.baidu.com/Interface/api/ptbk?uniqid='+self.uniqid
        response=requests.get(url,headers=self.headers)
        return response.json().get('data')

    def average(self,n=0):#可计算最近n日均值(n<span)
        l=len(self.index_all)
        if not n:
            n=l
        if n > l:
            return self.word,self.index_period.split('|')[0],self.index_period.split('|')[1],l,\
                   sum(self.index_all[-l:])//l,sum(self.index_pc[-l:])//l,sum(self.index_wise[-l:])//l
        else:
            return self.word,self.index_period.split('|')[0],self.index_period.split('|')[1],n,\
                   sum(self.index_all[-n:])//n,sum(self.index_pc[-n:])//n,sum(self.index_wise[-n:])//n

if __name__=='__main__':
    DEBUG=False
    span=90
    baiduindexes=BaiduIndex(['哈哈','啦啦','幻璃镜'],span)
    ll=[]
    for index in baiduindexes.indexes:
        ll.append(index.average(30))
    #with open('test.csv','w') as f:
    #    s=''
    #    for l in ll:
    #        s+=','.join(list(map(str,l)))+'\n'
    #    f.write(s)
    input('Press <Enter>')

