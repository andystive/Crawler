import requests
from bs4 import BeautifulSoup
import re
import time
import pymysql

user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
]

def get_boss_page():
    for page in range(1,2):
        url = "https://www.zhipin.com/c101280100/?query=python&page={page}&ka=page-{page}".format(page=page)
        headers = {'User-Agent': random.choice(user_agent_list)}
        try:
            proxy = random.sample(proxies_list, 1)[0]
            print(proxy)
            try:
                request = requests.get(url=url, proxies=proxy, headers=headers)
                pattern = re.compile(r'<a href="(.*?)" data-jid=.*?')
                items = re.findall(pattern, str(request.text))
                for item in items:
                    result = item.replace("<br/>", ",").strip()
                      # print(result)
                    try:
                        cursor.execute('INSERT INTO  qb_data (qb_content) VALUES (%s)', result)
                        coon.commit()
                        print('写入第{}页数据成功！'.format(page))
                    except:
                        print('写入数据库失败！')
            except:
                print('代理IP出错,更换代理IP！')
            else:
                print('写入第{}页数据成功！'.format(page))
        except:
            print('代理ip池为空')
    coon.close()


def connect_create_sql():
    try:
        with SSHTunnelForwarder(
                ssh_address_or_host = ('120.77.81.131',22),
                ssh_username="root",
                ssh_password="vbjkWGh*&dw3",
                remote_bind_address=('127.0.0.1',3306)) as server:
            print(server.local_bind_address)

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
            try:
                sql = 'CREATE TABLE IF NOT EXISTS qb_data(' \
                      'id INT AUTO_INCREMENT NOT NULL ,' \
                      'qb_content VARCHAR (300) NOT NULL,' \
                      'PRIMARY KEY (id))'
                cursor.execute(sql)
                print('数据表创建成功！')
            except:
                print('创建表失败或表已存在！')
            return coon, cursor
    except:
        print('数据库连接失败！')