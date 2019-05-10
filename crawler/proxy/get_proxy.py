# -*- coding: utf-8 -*-
# @Time    : 19/05/09
# @Author  : Virus
# @FileName: get_proxy.py
# @Software: PyCharm
# 本模块作用：将保存在本地ip.txt中的ip地址读取并返回到列表

import os

ip_path = os.path.split(os.path.realpath(__file__))[0]
# os.path.realpath(__file__)获取当前文件路径，os.path.split将文件路径和文件名分割，[0]取文件路径
def get_proxy():
    proxy_ip = []
    with open(r'{}\IP.txt'.format(ip_path), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            ip = lines[i].strip('\n')
            dict_ip = eval(ip)
            # 将代理ip列表，从字符串转换成字典，否则proxies报错
            # print(type(dict_ip))
            proxy_ip.append(dict_ip)
    return proxy_ip


if __name__ == '__main__':
   get_proxy()
