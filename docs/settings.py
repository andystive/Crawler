from bs4 import BeautifulSoup
with open(r'C:\Users\LHY\Desktop\test.html', 'r', encoding='utf-8') as f:
    content = f.read()
    #print(content)
    soup = BeautifulSoup(content,'lxml')
    # 从返回的网页中提取<tr>标签内的内容，[1:]为从1号列表读取，因为0号列表没有<td>标签，故执行tds[1]时会报错，列表越界
    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        proxy = tds[1].text+':'+tds[2].text
        print (proxy)
        print(tds)


