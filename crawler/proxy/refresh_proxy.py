'''
第二版代理ip地址池，目前在用
'''
from bs4 import BeautifulSoup
import requests
# import re
import os
import random
from crawler.proxy.user_agent import *

def get_proxy_page():
    eff_ip = []
    proxys = []
    ip_addr = []
    '''
    #直接抓取89ip代理api
    content = requests.get('http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp=')
    pattern = re.compile('a href=.*?>.*?<div id=.*?>.*?</div>.*?<script type=.*?>.*?</script>\n(.*)<br>', re.S)
    items = re.findall(pattern, str(content.text))
    for item in items:
        ip_addr = item.split('<br>')
        '''
    # 抓取西刺高匿代理第一页
    url = 'https://www.xicidaili.com/nn/1'
    headers = {'User-Agent': random.choice(user_agent_list)}
    html = requests.get(url=url, headers=headers).content
    soup = BeautifulSoup(html,'lxml')
    # 从返回的网页中提取<tr>标签内的内容，[1:]为从1号列表读取，因为0号列表没有<td>标签，故执行tds[1]时会报错，列表越界
    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        init_ip = tds[1].text+':'+tds[2].text
        #print (ip_addr)
        ip_addr.append(init_ip)
        # 将代理ip单个提取出来
    for i in range(0, len(ip_addr)):
        proxy_host = 'https://' + ip_addr[i]
        proxy_temp = {'https': proxy_host}
        proxys.append(proxy_temp)
    '''
    进行代理ip有效性检测
    '''
    url = 'https://www.baidu.com'
    for proxy in proxys:
        try:
            response = requests.get(url, proxies=proxy, timeout=5)
            if response.status_code == 200:
                #print(proxy)
                print(str(proxy) + '代理可用，已添加到列表！')
                eff_ip.append(proxy)
        except:
            print(str(proxy) + '代理不可用！')
    '''
    将有效的代理ip写入到文件
    '''
    with open(r'{}\IP.txt'.format(os.getcwd()), 'w', encoding='utf-8') as f:
        for ip in eff_ip:
            print(ip, file=f)



if __name__ == '__main__':
    get_proxy_page()
