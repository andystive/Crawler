#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
读取本地xml文件内容，并返回所需字段
@Time    : 2020/07/20
@Author  : Virus
@FileName: test.py
@Software: PyCharm
"""

import re

#path = 'C:\Users\jobs\Desktop\a.xml'

with open(r'C:\Users\jobs\Desktop\a.xml', 'r') as f:
    content = f.readall()
    #print(html)

    patten = re.compile('<BioSample.*?<Attributes>(.*?)</Attributes>.*?</BioSample>')
    items = re.findall(patten, content)
    for item in items:
        print(item)

