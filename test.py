import requests

api = 'http://ip.jiangxianli.com/'
response = requests.get(api)
print(response.text)