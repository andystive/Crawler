#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# @Time    : 2020/4/25 9:50
# @Author  : Virus
# @FileName: initialize.py
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


if __name__ == '__main__':
    create_element_table()
