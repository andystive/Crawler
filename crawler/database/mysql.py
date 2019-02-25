from sshtunnel import SSHTunnelForwarder
import pymysql

def connect_create_sql():
    try:
        with SSHTunnelForwarder(
                ssh_address_or_host = ('120.77.81.131',22),
                ssh_username="root",
                ssh_password="vbjkWGh*&dw3",
                remote_bind_address=('127.0.0.1',3306)) as server:
            #print(server.local_bind_address)
            coon = pymysql.connect(host='127.0.0.1',
                                   port=server.local_bind_port,
                                   user='root',
                                   password='ShuRuMiMa1234',
                                   db='python_test',
                                   charset='utf8mb4')
            cursor = coon.cursor()
            cursor.execute('SELECT VERSION()')
            data = cursor.fetchone()
            print('连接数据库成功，数据库版本为:{}'.format(data))
            sql = 'CREATE TABLE IF NOT EXISTS qb_data(' \
                  'id INT AUTO_INCREMENT NOT NULL ,' \
                  'qb_content VARCHAR (300) NOT NULL,' \
                  'PRIMARY KEY (id))'
            cursor.execute(sql)
            print('数据表创建成功！')
            coon.close()
    except:
        print('数据库连接失败！')


if __name__ == '__main__':
    connect_create_sql()

    try:
        cursor.execute('INSERT INTO  qb_data (qb_content) VALUES (%s)', result)
        coon.commit()
        print('写入第{}页数据成功！'.format(page))
    except:
        print('写入数据库失败！')
