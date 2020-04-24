#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
读取本地IP.txt文件内容，并返回代理ip字典
@Time    : 2019/05/09
@Author  : Virus
@FileName: 89_proxy.py
@Software: PyCharm
"""
import os


def get_proxy():
    """获取IP.txt内容，返回ip字典"""
    ip_path = os.path.split(os.path.realpath(__file__))[0]
    # os.path.realpath(__file__)获取当前文件路径，os.path.split将文件路径和文件名分割，[0]取文件路径
    proxy_ip = []
    with open(r'{}\IP.txt'.format(ip_path), encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            ip = lines[i].strip('\n')
            dict_ip = eval(ip)      # 将代理ip列表，从字符串转换成字典，否则proxies报错
            # print(type(dict_ip))
            proxy_ip.append(dict_ip)
    return proxy_ip


if __name__ == '__main__':
    print(get_proxy())
