import re
import requests
import random
from crawler.proxy.user_agent import *
from crawler.proxy.get_proxy import *

proxies_list = get_proxy()

def get_qb_content():
    qb_content = []
    for page in range(1,3):
        url = 'https://www.qiushibaike.com/text/page/' + str(page)
        headers = {'User-Agent': random.choice(user_agent_list)}
        try:
            proxy = random.sample(proxies_list, 1)[0]
            # 从从proxies_list中随机选取1个地址，[0]取该地址
            print(proxy)
            try:
                request = requests.get(url=url, proxies=proxy, headers=headers)
                pattern = re.compile('<div.*?content">.*?<span>(.*?)</span>.*?</div>.*?</span>', re.S)
                items = re.findall(pattern, str(request.text))
                for item in items:
                    result = item.replace("<br/>", ",").strip()
                    #print(result)
                    qb_content.append(result)
            except: AttributeError
                print()
            else:
                print('写入第{}页数据成功！'.format(page))
        except:
            print('代理ip池为空')
    print(len(qb_content))
    return qb_content


if __name__ == '__main__':
    get_qb_content()