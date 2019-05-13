# -*- coding: utf-8 -*-

"""
爬取链家网在售二手房数据
# @Time    : 19/05/13 8:59
# @Author  : Virus
# @FileName: lianjia.py
# @Software: PyCharm
"""

import re
import random
import requests
# from bs4 import BeautifulSoup
from crawler.proxy.user_agent import *
from crawler.proxy.get_proxy import *

def get_url_page(header, proxy):
    """获取链家网在售二手房源详细信息url地址并实时写入到数据库"""
    page = 1
    while page < 2:
        url = 'https://wh.lianjia.com/ershoufang/pg{}/'.format(page)
        try:
            response = requests.get(url=url, headers=header, proxies=proxy)
            pattern = re.compile('<div class="title"><a class=.*?href="(.*?)" target=.*?data-sl="">(.*?)</a>.*?<div class="totalPrice"><span>(.*?)</span>.*?data-price="(.*?)">', re.S)
            content = re.findall(pattern, str(response.text))
            for i in content:
                sql_insert = "insert into Element" \
                             "(url, description, totalPrice, price)" \
                             "values" \
                             "(%s, %s, %s, %s)"
                params = (i[0], i[1], i[2], i[3])
                cur.execute(sql_insert, params)
            page = page + 1
        except Exception:
            print("第{}页数据爬取失败，重试中...".format(page))

# def get_detail_page(url, header, proxy):
#     """爬取链家在售二手房详情页面信息，并获取详细数据"""
#     response = requests.get(url=url, headers=header, proxies=proxy)
#     soup = BeautifulSoup(response, 'lxml')


def main():
    """函数入口，初始化url、headers、proxies值，并调用其他函数"""
    header = {'User-Agent': random.choice(user_agent_list)}
    proxy = random.sample(get_proxy(), 1)[0]
    # url = 'https://wh.lianjia.com/ershoufang/104101555272.html'
    # return get_url_page(header, proxy), get_detail_page(url, header, proxy)
    return get_url_page(header, proxy)


if __name__ == '__main__':
    main()