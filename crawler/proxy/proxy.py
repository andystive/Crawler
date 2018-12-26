import requests
import re
import os

current_path = os.getcwd()

def get_proxy_page():
    r = requests.get('http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp=')
    pattern = re.compile('a href=.*?>.*?<div id=.*?>.*?</div>.*?<script type=.*?>.*?</script>\n(.*)<br>', re.S)
    items = re.findall(pattern, str(r.text))
    with open(r'{}\IP.txt'.format(current_path),'w', encoding='utf-8') as f:
        for item in items:
            result = item.replace('<br>', '\n')
            print(result, file=f)

def check_proxy_ip():
    effective_ip = []
    with open(r'{}\IP.txt'.format(current_path), 'r', encoding='utf-8') as f:
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

if __name__ == '__main__':
    get_proxy_page()
