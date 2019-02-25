import requests
import re
import os
import random
from crawler.proxy.user_agent import *

def get_proxy_page():
    content = requests.get('http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp=')
    pattern = re.compile('a href=.*?>.*?<div id=.*?>.*?</div>.*?<script type=.*?>.*?</script>\n(.*)<br>', re.S)
    items = re.findall(pattern, str(content.text))
    with open(r'{}\IP.txt'.format(os.getcwd()), 'w', encoding='utf-8') as f:
        for item in items:
            result = item.replace('<br>', '\n')
            print(result, file=f)

def check_proxy_ip():
    effective_ip = []
    with open(r'{}\IP.txt'.format(os.getcwd()), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        proxys = []
        for i in range(0, len(lines)):
            ip = lines[i].strip('\n').split('\t')
            proxy_host = 'https://' + ip[0]
            proxy_temp = {'https': proxy_host}
            proxys.append(proxy_temp)
        url = 'https://www.baidu.com'
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



if __name__ == '__main__':
    get_proxy_page()
    proxies_list = check_proxy_ip()
    print(proxies_list)