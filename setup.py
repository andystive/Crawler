import requests
import re
import random
from crawler.proxy.user_agent import *
from crawler.proxy.get_proxy import *

url = "https://www.xicidaili.com/nn/"
proxies_list = get_proxy()
proxy = random.sample(proxies_list, 1)[0]

headers = {'User-Agent': random.choice(user_agent_list)}
#content = requests.get(url=url, proxies=proxy, headers=headers)
#print(content)
print(proxy)
print(headers)