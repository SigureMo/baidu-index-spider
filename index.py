import os
import json
import sys
import time

from urllib import parse

from utils.crawler import Crawler

spider = Crawler()


def store_cookies(restore=False):
    """存储并返回 Cookie 字典"""

    def cookie_to_json():
        """将分号分隔的 Cookie 转为字典"""

        cookies_dict = {}
        raw_cookies = input('> ')
        if not raw_cookies:
            return {}
        if raw_cookies[:7].lower() == 'cookie:':
            raw_cookies = raw_cookies[7:]

        for cookie in raw_cookies.split(';'):
            key, value = cookie.lstrip().split("=", 1)
            cookies_dict[key] = value

        return cookies_dict

    file_path = os.path.join(sys.path[0], "cookies.json")
    if not os.path.isfile(file_path):
        cookies = {}
    else:
        with open(file_path, 'r') as cookies_file:
            cookies = json.load(cookies_file)

    if restore or not cookies:
        print("输入 Cookie：")
        cookies = cookie_to_json()
        with open(file_path, 'w') as f:
            json.dump(cookies, f, indent=2)

    return cookies


def get_index(words, startdate, enddate):
    """ 获取在某个时间范围内的指数信息 """
    wordlist = ""
    for n in range(len(words)):
        wordlist += '&wordlist%5B{}%5D={}'.format(n, words[n])
    url = 'http://index.baidu.com/Interface/Newwordgraph/getIndex?region=0&startdate={}&enddate={}{}'\
        .format(startdate, enddate, wordlist)
    res = spider.get(url)
    return res.json()


def decrypto(origin, key):
    """ 解密指数信息 """
    s = ''
    for c in origin:
        if c:
            s += key[key.index(c)+len(key)//2]
    data = []
    for i in s.split(','):
        data.append(int(i))
    return data


def getkey(uniqid):
    """ 获取解密密钥 """
    url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=' + uniqid
    return spider.get(url).json()["data"]


def average(index, n=0):
    """ 用于计算最近 n 日均值(n <= span) """
    span = len(index["all"])
    if not n or n > span:
        n = span
    return {
        "span": n,
        "all": sum(self.index["all"][-n:])//n,
        "pc": sum(self.index["pc"][-n:])//n,
        "wise": sum(self.index["wise"][-n:])//n,
    }


if __name__ == '__main__':
    cookies = store_cookies(restore=False)
    spider.set_cookies(cookies)
    span = 90
    words = ["百度", "指数", "爬虫"]
    for n in range(len(words)):
        words[n] = parse.quote(words[n].encode())

    if isinstance(span, int):
        startdate = time.strftime(
            '%Y%m%d', time.localtime(time.time()-60*60*24*span))
        enddate = time.strftime(
            '%Y%m%d', time.localtime(time.time()-60*60*24*1))
    elif isinstance(span, str):
        startdate = span.split('|')[0]
        enddate = span.split('|')[1]

    index_data = get_index(words, startdate, enddate)
    uniqid, data_list = index_data["uniqid"], index_data["data"]

    indexes = []
    key = getkey(uniqid)
    for origin_data in data_list:

        index = {}
        index_period = origin_data["index"][0]["period"]
        index = {
            "word": origin_data["key"],
            "start_date": index_period.split("|")[0],
            "end_date": index_period.split("|")[1],
            "all": decrypto(origin_data["index"][0]["_all"], key),
            "pc": decrypto(origin_data["index"][0]["_pc"], key),
            "wise": decrypto(origin_data["index"][0]["_wise"], key)
        }
        print(index)
