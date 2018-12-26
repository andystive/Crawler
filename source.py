import re
import requests
import random
import pymysql
import threading

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

def get_proxy_page():
    source_ip = []
    r = requests.get('http://www.89ip.cn/tqdl.html?api=1&num=10&port=&address=&isp=')
    pattern = re.compile('a href=.*?>.*?<div id=.*?>.*?</div>.*?<script type=.*?>.*?</script>\n(.*)<br>', re.S)
    items = re.findall(pattern, str(r.text))
    for item in items:
        result = item.replace('<br>', '\n')
        source_ip.append(result)
        print(source_ip)

def check_proxy_ip():
    effective_ip = []
    with open(r'C:\Users\LHY\Desktop\IP\IP.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        proxys = []
        for i in range(0, len(lines)):
            ip = lines[i].strip('\n').split('\t')
            proxy_host = 'http://' + ip[0]
            proxy_temp = {'http': proxy_host}
            proxys.append(proxy_temp)
        url = 'http://www.chaipip.com/index.php'
        headers = {'User-Agent': random.choice(user_agent_list)}
        for proxy in proxys:
            try:
                response = requests.get(url, proxies=proxy, headers=headers, timeout=5)
                if response.status_code == 200:
                    print(str(proxy) + '代理可用，已添加到列表！')
                    effective_ip.append(proxy)
            except:
                print(str(proxy) + '代理不可用！')
    return effective_ip

def get_qb_content():
    for page in range(1,10):
        url = 'https://www.qiushibaike.com/text/page/' + str(page)
        headers = {'User-Agent': random.choice(user_agent_list)}
        proxy = random.sample(proxies_list, 1)[0]
        #print(proxy)
        try:
            request = requests.get(url=url, proxies=proxy, headers=headers)
            try:
                pattern = re.compile('<div.*?content">.*?<span>(.*?)</span>.*?</div>.*?</span>', re.S)
                items = re.findall(pattern, str(request.text))
                for item in items:
                    result = item.replace("<br/>", ",").strip()
                    #print(result)
                    try:
                        cursor.execute('INSERT INTO  qb_data (qb_content) VALUES (%s)', result)
                        coon.commit()
                        #print('写入第{}页数据成功！'.format(page))
                    except:
                        print('写入数据库失败！')
            except:
                print('代理IP出错,更换代理IP！')
        except:
            print('循环运行出错，请检查！')
        else:
            print('写入第{}页数据成功！'.format(page))
    coon.close()

def connect_create_sql():
    try:
        coon = pymysql.connect(host='rm-wz90h3cpn5z9g62fdso.mysql.rds.aliyuncs.com',
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


def time_control():
    get_proxy_page()
    proxies_list = get_proxy_page()
    global timer
    timer = threading.Timer(300,time_control)
    timer.start()


if __name__ == '__main__':
    time_control()
    print(proxies_list)
    coon, cursor = connect_create_sql()
    get_qb_content()



