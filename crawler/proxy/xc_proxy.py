#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
获取西刺代理中的IP地址，并将地址保存到本地IP.txt文件中
@Time    : 2019/05/09
@Author  : Virus
@FileName: xc_proxy.py
@Software: PyCharm
"""

import os
import random
import requests
from bs4 import BeautifulSoup
from crawler.proxy.user_agent import *


def get_proxy_page(url):
    """抓取西刺代理页面，并用bs4解析出ip，最后进行ip数据清洗后存入本地IP.txt文件"""
    all_ip = []  # 从api提取的ip地址，已去除<br>标签
    proxy_list = []  # 从all_ip列表中分解出的单个ip，并添加https头，构成代理ip字典
    eff_ip = []  # 最终写入到本地IP.txt文件中的有效ip列表
    '''
    抓取西刺高匿代理第一页
    '''
    headers = {'User-Agent': random.choice(user_agent_list)}
    html = requests.get(url=url, headers=headers).content
    soup = BeautifulSoup(html, 'lxml')
    '''
    从返回的网页中提取<tr>标签内的内容，[1:]为从1号列表读取，
    因为0号列表没有<td>标签，故执行tds[1]时会报错，列表越界
    '''
    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        init_ip = tds[1].text + ':' + tds[2].text
        all_ip.append(init_ip)
    '''
    将代理ip单个提取出来
    '''
    for i in range(0, len(all_ip)):
        proxy_host = 'https://' + all_ip[i]
        proxy_temp = {'https': proxy_host}
        proxy_list.append(proxy_temp)
    '''
    进行代理ip有效性检测
    '''
    url = 'https://www.baidu.com'
    for proxy in proxy_list:
        # noinspection PyBroadException
        try:
            response = requests.get(url, proxies=proxy, timeout=5)
            if response.status_code == 200:
                print(str(proxy) + '代理可用，已添加到列表！')
                eff_ip.append(proxy)
        except Exception:
            print(str(proxy) + '代理不可用！')
    '''
    将有效的代理ip写入到文件
    '''
    with open(r'{}\IP.txt'.format(os.getcwd()), 'w+', encoding='utf-8') as f:
        for ip in eff_ip:
            print(ip, file=f)


def main():
    """函数入口，定义url地址及调用其他函数"""
    url = 'https://www.xicidaili.com/wn/'
    get_proxy_page(url)


if __name__ == '__main__':
    main()
