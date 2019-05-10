# -*- coding: utf-8 -*-

"""
获取89代理中的IP地址，并将地址保存到本地IP.txt文件中
@Time    : 19/05/09
@Author  : Virus
@FileName: 89_proxy.py
@Software: PyCharm
"""

import os
import re
import requests


def get_proxy_page(api):
    """通过api抓取代理ip，然后写入到本地文件"""
    all_ip = []         # 从api提取的ip地址，已去除<br>标签
    proxy_list = []     # 从all_ip列表中分解出的单个ip，并添加https头，构成代理ip字典
    eff_ip = []         # 最终写入到本地IP.txt文件中的有效ip列表
    '''
    直接抓取89ip代理api
    '''
    content = requests.get(api)
    pattern = re.compile(
        'a href=.*?>.*?<div id=.*?>.*?</div>.*?<script type=.*?>.*?</script>\n(.*)<br>',
        re.S)
    items = re.findall(pattern, str(content.text))
    for item in items:
        all_ip = item.split('<br>')
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
    """函数入口，定义api地址及调用其他函数"""
    api = 'http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp='
    get_proxy_page(api)


if __name__ == '__main__':
    main()
