# **武汉二手房售价**
### 链家在售二手房数据爬取、分析
---
### **爬虫模块** 
1. **user_agent**  
*作用：提供爬虫所需user_agent*
```
user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; \
    SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36']
```
2. **89_proxy.py**  
*作用：通过89代理网站提供的api，正则提取并保存代理ip到本地IP.txt文件*  

代码分析  
- 需要os、re、requests三个库文件，其中os为获取IP.txt文件路径，re为正则表达式提取api内ip地址时使用，requests为获取网站api接口代理ip数据
```
import os
import re
import requests
```
- 定义函数中存放变量的列表和字典
```
def get_proxy_page(api):
    """通过api抓取代理ip，然后写入到本地文件"""
    all_ip = []         # 从api提取的ip地址，已去除<br>标签
    proxy_list = []     # 从all_ip列表中分解出的单个ip，并添加https头，构成代理ip字典
    eff_ip = []         # 最终写入到本地IP.txt文件中的有效ip列表
```
- 直接抓取89ip代理api，变量content用于接收requests获取的api数据，pattern用于存放compile函数创建模式对象。split('\<br>')为通过指定分隔符（\<br>）对字符串进行分割切片，即删除返回ip数据中的（\<br>）标签
>直接使用字符串表示的正则表达式进行search,match和findall操作时，python会将字符串转换为正则表达式对象。而使用compile完成一次转换之后，在每次使用模式的时候就不用重复转换实现，更有效率的匹配
```
    content = requests.get(api)
    pattern = re.compile(
        'a href=.*?>.*?<div id=.*?>.*?</div>.*?<script type=.*?>.*?</script>\n(.*)<br>',
        re.S)
    items = re.findall(pattern, str(content.text))
    for item in items:
        all_ip = item.split('<br>')
```
- 将代理ip单个提取出来，len函数获取all_ip列表中元素的数量，proxy_host变量存储加上https://头的ip地址，proxy_temp变量格式化元素，格式为'https': https://IP',proxy_list为key-value字典，将格式化后的元素存储到字典
```
    for i in range(0, len(all_ip)):
        proxy_host = 'https://' + all_ip[i]
        proxy_temp = {'https': proxy_host}
        proxy_list.append(proxy_temp)
```
- 进行代理ip有效性检测，通过访问百度获取返回码，等待时间设为5s，若返回码为200则证明代理ip可以用，然后将代理ip地址写入到eff_ip列表中，否则代理ip地址已失效。
```
    url = 'https://www.baidu.com'
    for proxy in proxy_list:
        # noinspection PyBroadException
        try:
            response = requests.get(url, proxies=proxy, timeout=5)
            if response.status_code == 200:
                print(str(proxy) + '代理可用，已添加到列表！')
                eff_ip.append(proxy)
        except Exception:
            print(str(proxy) + '代理不可用！')
```
- 将有效的代理ip写入到IP.txt文件，其中w+为写入操作，若文件不存在，则创建。
```
    with open(r'{}\IP.txt'.format(os.getcwd()), 'w+', encoding='utf-8') as f:
        for ip in eff_ip:
            print(ip, file=f)
```
- 定义函数入口，并初始化api变量
```

def main():
    """函数入口，定义api地址及调用其他函数"""
    api = 'http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp='
    get_proxy_page(api)


if __name__ == '__main__':
    main()

```
3. **xc_proxy.py**  
*作用：通过爬取西刺代理网站ip页面，bs4提取并保存代理ip到本地IP.txt文件*  

代码分析  
- 需要os、random、requests、BeautifulSoup四个库以及user_agent模块，其中os为获取IP.txt文件路径，requests为获取网站代理ip页面源码数据，random为从user_agent中随机choice一个头文件，BeautifulSoup为格式化源码并提取代理ip数据，user_agent模块为浏览器头文件
```
import os
import random
import requests
from bs4 import BeautifulSoup
from crawler.proxy.user_agent import *
```
- 定义函数中存放变量的列表和字典
```
def get_proxy_page(url):
    """抓取西刺代理页面，并用bs4解析出ip，最后进行ip数据清洗后存入本地IP.txt文件"""
    all_ip = []  # 从格式化后的源码中提取出的代理ip地址
    proxy_list = []  # 从all_ip列表中分解出的单个ip，并添加https头，构成代理ip字典
    eff_ip = []  # 最终写入到本地IP.txt文件中的有效ip列表
```
- 抓取西刺高匿代理第一页代理ip数据，headers变量为构造的头文件，html变量为requests获取到content内容，soup变量为格式化解析后的源码，最后将解析出的代理ip地址存储到列表all_ip
```
    headers = {'User-Agent': random.choice(user_agent_list)}
    html = requests.get(url=url, headers=headers).content
    soup = BeautifulSoup(html, 'lxml')
    '''
    从返回的网页中提取<tr>标签内的内容，[1:]为从1号列表读取，
    因为0号列表没有<td>标签，故执行tds[1]时会报错，列表越界
    '''
    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        init_ip = tds[1].text + ':' + tds[2].text
        all_ip.append(init_ip)
```
- 将代理ip单个提取出来，len函数获取all_ip列表中元素的数量，proxy_host变量存储加上https://头的ip地址，proxy_temp变量格式化元素，格式为'https': https://IP',proxy_list为key-value字典，将格式化后的元素存储到字典
```
    for i in range(0, len(all_ip)):
        proxy_host = 'https://' + all_ip[i]
        proxy_temp = {'https': proxy_host}
        proxy_list.append(proxy_temp)
```
- 进行代理ip有效性检测，通过访问百度获取返回码，等待时间设为5s，若返回码为200则证明代理ip可以用，然后将代理ip地址写入到eff_ip列表中，否则代理ip地址已失效。
```
    url = 'https://www.baidu.com'
    for proxy in proxy_list:
        # noinspection PyBroadException
        try:
            response = requests.get(url, proxies=proxy, timeout=5)
            if response.status_code == 200:
                print(str(proxy) + '代理可用，已添加到列表！')
                eff_ip.append(proxy)
        except Exception:
            print(str(proxy) + '代理不可用！')
```
- 将有效的代理ip写入到IP.txt文件，其中w+为写入操作，若文件不存在，则创建。
```
    with open(r'{}\IP.txt'.format(os.getcwd()), 'w+', encoding='utf-8') as f:
        for ip in eff_ip:
            print(ip, file=f)
```
- 定义函数入口，并初始化api变量
```
def main():
    """函数入口，定义url地址及调用其他函数"""
    url = 'https://www.xicidaili.com/nn/1'
    get_proxy_page(url)


if __name__ == '__main__':
    main()

```
4. **get_proxy.py**
*作用：获取本地IP.txt文件中的ip地址，然后返回字典格式代理ip*

代码分析
- 需要os库，作用为获取IP.txt文件地址
```
import os
```
- 定义函数，获取IP.txt文件内容，open函数默认参数为r（只读）；readlines函数一次性读取IP.txt所以行文件，并将每一行进行分离，方便后续for循环遍历；len函数为统计lines中行数，即IP.txt文件中ip地址的行数；split('\n')为通过指定分隔符（\n）对字符串进行分割切片，即删除返回ip数据中的（\n）标签，即删除换行符；eval函数将代理ip列表转换为字典；最后将读取分离后的代理ip地址存储到proxy_ip字典中，并返回字典
```
def get_proxy(ip_path):
    """获取IP.txt内容，返回ip字典"""
    proxy_ip = []
    with open(r'{}\IP.txt'.format(ip_path), encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            ip = lines[i].strip('\n')
            dict_ip = eval(ip)      # 将代理ip列表，从字符串转换成字典，否则proxies报错
            # print(type(dict_ip))
            proxy_ip.append(dict_ip)
    return proxy_ip
```
- 定义函数入口，并初始化ip_path变量
```
def main():
    """函数入口，定义api地址及调用其他函数"""
    ip_path = os.path.split(os.path.realpath(__file__))[0]
    # os.path.realpath(__file__)获取当前文件路径，os.path.split将文件路径和文件名分割，[0]取文件路径
    get_proxy(ip_path)


if __name__ == '__main__':
    main()
```
