import requests
import re
import os

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

class GetProxiesIp(object)

    current_path = os.getcwd()

    def __init__(self):


    def get_proxy_page():
        content = requests.get('http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp=')
        pattern = re.compile('a href=.*?>.*?<div id=.*?>.*?</div>.*?<script type=.*?>.*?</script>\n(.*)<br>', re.S)
        items = re.findall(pattern, str(content.text))
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
    proxy_list = GetProxiesIp.check_proxy_ip()