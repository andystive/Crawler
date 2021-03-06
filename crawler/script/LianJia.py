#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
爬取链家网在售二手房数据
# @Time    : 2019/05/13 8:59
# @Author  : Virus
# @FileName: LianJia.py
# @Software: PyCharm
"""

import re
import random
import requests
from crawler.proxy.user_agent import *
from crawler.proxy.get_proxy import *
from crawler.database.mysql import *


def get_url_page(header, proxy, coon, cur):
    """获取链家网在售二手房源详细信息url地址并实时写入到数据库"""
    page = 100
    while page < 101:
        url = 'https://wh.lianjia.com/ershoufang/pg{}/'.format(page)
        try:
            response = requests.get(url=url, headers=header, proxies=proxy)
            pattern = re.compile(
                '<div class="title"><a class=.*?href="(.*?)" target=.*?data-sl="">(.*?)</a>.*?<div class="totalPrice"><span>(.*?)</span>.*?data-price="(.*?)">',
                re.S)
            content = re.findall(pattern, str(response.text))
            for element in content:
                sql_insert = "insert into Element" \
                             "(url, description, totalPrice, price)" \
                             "values" \
                             "(%s, %s, %s, %s)"
                params = (element[0], element[1], element[2], element[3])
                cur.execute(sql_insert, params)
            print("第{}页数据写入数据库成功...".format(page))
            page += 1
        except Exception as err :
            print("第{}页数据爬取失败，重试中...".format(page))
    coon.commit()
    cur.close()
    coon.close()


def get_detail_page(url, header, proxy):
    """爬取链家在售二手房详情页面信息，并获取详细数据"""
    response = requests.get(url=url, headers=header)
    res = '<div class="room"><div class="mainInfo">(.*?)</div><div class="subInfo">(.*?)</div>.*?<div class="area"><div class="mainInfo">(.*?)</div>.*?class="info ">(.*?)</a>.*?target="_blank">(.*?)</a>.*?target="_blank">(.*?)</a>'
    pattern = re.compile(res, re.S)
    content = re.findall(pattern, str(response.text))
    for element in content:
        sql_insert = "insert into Element" \
                     "(type, floor, area, communityName, areaName, location)" \
                     "values" \
                     "(%s, %s, %s, %s, %s, $s)"
        params = (
            element[0],
            element[1],
            element[2],
            element[3],
            element[4],
            element[5])
        cur.execute(sql_insert, params)
    print("第{}页数据写入数据库成功...".format(page))
    page = page + 1
    except Exception:
    print("第{}页数据爬取失败，重试中...".format(page))
    coon.commit()
    cur.close()
    coon.close()


def main():
    """函数入口，初始化url、headers、proxies、cur、coon值，并调用其他函数"""
    header = {'User-Agent': random.choice(user_agent_list)}
    proxy = random.sample(get_proxy(), 1)[0]
    coon, cur = connect_local_db()
    url = 'https://wh.lianjia.com/ershoufang/104101555272.html'
    # return get_url_page(header, proxy), get_detail_page(url, header, proxy)
    # get_url_page(header, proxy, coon, cur)
    get_detail_page(url, header, proxy)


if __name__ == '__main__':
    main()
