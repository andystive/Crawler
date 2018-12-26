import requests
import re
import random
import os

def get_proxy_page():
    current_path = os.getcwd()
    r = requests.get('http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp=')
    pattern = re.compile('a href=.*?>.*?<div id=.*?>.*?</div>.*?<script type=.*?>.*?</script>\n(.*)<br>', re.S)
    items = re.findall(pattern, str(r.text))
    with open(r'{}\IP.txt'.format(current_path),'w', encoding='utf-8') as f:
        for item in items:
            result = item.replace('<br>', '\n')
            print(result, file=f)


if __name__ == '__main__':
    get_proxy_page()
    #result=random.sample(proxies_list, 1)[0]
    #print(result)