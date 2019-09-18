import json
import os
import time
from urllib import parse

from utils.common import store_cookies
from utils.crawler import Crawler

spider = Crawler()


def get_index(words, start_date, end_date):
    """ 获取在某个时间范围内的指数信息 """
    wordlist = ""
    for n in range(len(words)):
        wordlist += '&wordlist%5B{}%5D={}'.format(n, words[n])
    url = 'http://index.baidu.com/Interface/Newwordgraph/getIndex?region=0&startdate={}&enddate={}{}'\
        .format(start_date, end_date, wordlist)
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


if __name__ == '__main__':
    # 随便在一个已登录的百度页面， F12 就能找到
    cookies = store_cookies(restore=False)
    spider.set_cookies(cookies)
    # 支持两种格式的时间跨度
    span = 90
    # span = "20190907|20190918"
    # 关键词列表
    all_words = ["百度", "指数", "爬虫", "移动", "接口"]
    indices = []

    # 转换关键词
    for n in range(len(all_words)):
        all_words[n] = parse.quote(all_words[n].encode())

    # 转换时间跨度
    if isinstance(span, int):
        start_date = time.strftime(
            '%Y%m%d', time.localtime(time.time()-60*60*24*span))
        end_date = time.strftime(
            '%Y%m%d', time.localtime(time.time()-60*60*24*1))
    elif isinstance(span, str):
        start_date = span.split('|')[0]
        end_date = span.split('|')[1]

    # 批量查询，每三个查询一次
    for i in range(0, len(all_words), 3):
        words = all_words[i: i+3]

        # 查询数据
        index_data = get_index(words, start_date, end_date)
        uniqid, data_list = index_data["uniqid"], index_data["data"]

        # 解密数据
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
            indices.append(index)

    for index in indices:
        print(index)
