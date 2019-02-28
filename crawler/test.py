import requests
import re
import random
from crawler.proxy.user_agent import *
from crawler.proxy.get_proxy import *

url = "https://www.xicidaili.com/nn/"
headers = {'User-Agent': random.choice(user_agent_list)}
content = requests.get(url=url, headers=headers)
print(content.text)
#print(headers)