from sshtunnel import SSHTunnelForwarder
import pymysql
from script.QiuBai import *

def connect_create_sql():
    try:
        #通过ssh远程连接到服务器
        with SSHTunnelForwarder(
                ssh_address_or_host = ('129.28.104.83',22),
                ssh_username="root",
                ssh_password="-x9_ZJ_ptv4eEjv",
                remote_bind_address=('127.0.0.1',3306)) as server:
            #print(server.local_bind_address)
            # 连接服务器本地数据库
            coon = pymysql.connect(host='127.0.0.1',
                                   # 因未指定server.local_bind_address，故host须为127.0.0.1
                                   port=server.local_bind_port,
                                   user='root',
                                   password='shurumima1234',
                                   db='python_test',
                                   charset='utf8mb4')
            cursor = coon.cursor()
            cursor.execute('SELECT VERSION()')
            # 检测数据库是否正常连接，查询数据库版本
            data = cursor.fetchone()
            # 只获取查询结果中的第一条数据
            print('连接数据库成功，数据库版本为:{}'.format(data))
            sql = 'CREATE TABLE IF NOT EXISTS qb_data(' \
                  'id INT AUTO_INCREMENT NOT NULL ,' \
                  'qb_content VARCHAR (300) NOT NULL,' \
                  'PRIMARY KEY (id))'
            cursor.execute(sql)
            print('数据表创建成功！')


            # 将QiuBai所获取的数据写入到数据库
            i = 0
            for result in get_qb_content():
                i += 1
                try:
                    cursor.execute('INSERT INTO  qb_data (qb_content) VALUES (%s)', result)
                    coon.commit()
                    print('写入第{}条数据成功！'.format(i))
                except Exception as err:
                    print('写入数据库失败！',err)
            coon.close()
    except Exception as err:
        print('数据库连接失败！',err)


if __name__ == '__main__':
    connect_create_sql()