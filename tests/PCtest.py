class Indexation():
    def __init__(self,word):
        self.word=parse.quote(word.encode('gb2312'))
        self.res='kA0fEnocADxXMiojICIAXmc1ITARBgY8OhtFM0Nscxd0ZApfDAA3cAUhCAVyK1QxYwAMcgsgLDMXED9xJy8uIxVoUTBHXAZULEwCEy4HbCFQKBsuDTc5QW4iFxEXbndBIyMMVwBYfU9kMSAJKjd2TkQgJTJ2bgFWEkUyMEBtc0t2LlsWMmh1K29tBT82fzs%2FVXEed1I6A0kCEkcrJAtSQAdvOHIoTBoiSiwSXyxFQWJlUHs6elQbGAIgJQhhOQA1NioAAUAoBDIIPl4TKAQ%3D'
        self.res2='34it0b9NUwkBNPMd1A0skMQgr2WmiD7GhmxCyziqxblV6j20oL831.351632.3X7'
        try:
            with open('data/cookies.json','rb') as c:
                self.cookies=json.loads(c.read().decode())
        except:
            self.cookies=getcookies(DEBUG)
        cook_str=[]
        for cookie in cookies:
            cook_str.append(cookie.get('name')+'='+cookie.get('value'))
        cook_str='; '.join(cook_str)
        self.headers={
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'index.baidu.com',
            'Referer': 'https://index.baidu.com/?tpl=trend&type=0&area=0&time=13&word='+word,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie':cook_str,
            }
    def getAllIndex(self,headers,res,res2,startdate,enddate):
        url='https://index.baidu.com/Interface/Search/getAllIndex/'
        params={
            'res':res,
            'res2':res2,
            'startdate':startdate,
            'enddate':enddate,
            }
        response=requests.get(url,headers=self.headers,params=params).json()
        for data in response.get('data').get('all'):
            self.agv_w_enc=5



def getres3s(headers):
    url='http://index.baidu.com/Interface/Newwordgraph/getIndex?region=0&startdate=20180626&enddate=20180702&wordlist%5B0%5D=%E5%93%88%E5%93%88'
    response=requests.get(url,headers=headers)
    return response.json()
word='哈哈'
word=parse.quote(word.encode('gb2312'))
res='kA0fEnocADxXMiojICIAXmc1ITARBgY8OhtFM0Nscxd0ZApfDAA3cAUhCAVyK1QxYwAMcgsgLDMXED9xJy8uIxVoUTBHXAZULEwCEy4HbCFQKBsuDTc5QW4iFxEXbndBIyMMVwBYfU9kMSAJKjd2TkQgJTJ2bgFWEkUyMEBtc0t2LlsWMmh1K29tBT82fzs%2FVXEed1I6A0kCEkcrJAtSQAdvOHIoTBoiSiwSXyxFQWJlUHs6elQbGAIgJQhhOQA1NioAAUAoBDIIPl4TKAQ%3D'
res2='34it0b9NUwkBNPMd1A0skMQgr2WmiD7GhmxCyziqxblV6j20oL831.351632.3X7'
'''res3[]=84V44&res3[]=fI6g&className=profWagv'''
startdate='2018-06-02'
enddate='2018-07-01'
try:
    with open('data/cookies.json','rb') as c:
        cookies=json.loads(c.read().decode())
except:
    cookies=getcookies(DEBUG)
cs=[]
for cookie in cookies:
    cs.append(cookie.get('name')+'='+cookie.get('value'))
cs='; '.join(cs)
headers={
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'index.baidu.com',
    'Referer': 'http://index.baidu.com/baidu-index-mobile/index.html',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie':cs,
    }
