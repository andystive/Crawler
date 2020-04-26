#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库操作，连接数据库，建立新表，写入数据
# @Time    : 2019/05/13 15:41
# @Author  : Virus
# @FileName: mysql.py
# @Software: PyCharm
"""
import pymysql


def connect_local_db():
    """连接数据库"""
    coon = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='password',
        db='crawler'
    )
    cur = coon.cursor()
    return coon, cur




def insert_element_data():
    """将爬取到的链家数据存储到数据库"""
    data = main()
    for i in data:
        sql_insert = "insert into Element" \
                     "(url, description, totalPrice, price)" \
                     "values" \
                     "(%s, %s, %s, %s)"
        params = (i[0], i[1], i[2], i[3])
        cur.execute(sql_insert, params)
    coon.commit()
    cur.close()
    coon.close()

if __name__ == '__main__':
    create_element_table()
