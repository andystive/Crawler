'''
第二版代理ip地址池，目前在用
'''
import requests
import re
import os

def get_proxy_page():
    eff_ip = []
    proxys = []
    content = requests.get('http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp=')
    pattern = re.compile('a href=.*?>.*?<div id=.*?>.*?</div>.*?<script type=.*?>.*?</script>\n(.*)<br>', re.S)
    items = re.findall(pattern, str(content.text))
    for item in items:
        ip_addr = item.split('<br>')
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
                print(proxy)
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
