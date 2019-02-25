import requests
import re
import os
import random
from crawler.proxy.user_agent import *

def get_proxy_page():
    proxys = []
    content = requests.get('http://www.89ip.cn/tqdl.html?api=1&num=10&port=&address=&isp=')
    pattern = re.compile('a href=.*?>.*?<div id=.*?>.*?</div>.*?<script type=.*?>.*?</script>\n(.*)<br>', re.S)
    items = re.findall(pattern, str(content.text))
    for item in items:
        ip_addr = item.split('<br>')
    for i in range(0, len(ip_addr)):
        proxy_host = 'https://' + ip_addr[i]
        proxy_temp = {'https': proxy_host}
        proxys.append(proxy_temp)
        url = 'https://www.baidu.com'
        headers = {'User-Agent': random.choice(user_agent_list)}
        for proxy in proxys:
            print(proxy)



'''
            try:
                response = requests.get(url, proxies=proxy, headers=headers, timeout=5)
                if response.status_code == 200:
                    print(str(proxy) + '代理可用，已添加到列表！')
                    effective_ip.append(proxy)
            except:
                print(str(proxy) + '代理不可用！')
'''




if __name__ == '__main__':
    get_proxy_page()
