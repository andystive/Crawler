# -*- coding: utf-8 -*-

"""
数据库操作，连接数据库，建立新表，写入数据
# @Time    : 19/05/13 15:41
# @Author  : Virus
# @FileName: mysql.py
# @Software: PyCharm
"""
import pymysql
from crawler.script.lianjia import *

def connect_local_db():
    """连接数据库"""
    coon = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='shurumima1234',
        db='crawler'
    )
    cur = coon.cursor()
    return coon, cur

def create_element_table():
    """创建数据表"""
    coon, cur = connect_local_db()
    sql_create = "create table if not exists Element(" \
                 "id int not null auto_increment," \
                 "url char(51) not null," \
                 "description varchar(100) not null," \
                 "totalPrice varchar(10) not null," \
                 "price int not null," \
                 "type char(8)," \
                 "floor varchar(20)," \
                 "area varchar(15)," \
                 "communityName varchar(35)," \
                 "areaName varchar(20)," \
                 "location varchar(20)," \
                 "primary key (id)" \
                 ")engine=InnoDB default charset=utf8"

    cur.execute(sql_create)
    coon.commit()

def insert_element_data():
    """将爬取到的链家数据存储到数据库"""
    data=main()
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