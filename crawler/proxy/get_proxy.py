import os

ip_path = os.path.split(os.path.realpath(__file__))[0]
# os.path.realpath(__file__)获取当前文件路径，os.path.split将文件路径和文件名分割，[0]取文件路径
def get_proxy():
    proxy_ip = []
    with open(r'{}\IP.txt'.format(ip_path), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            ip = lines[i].strip('\n')
            proxy_ip.append(ip)
    return proxy_ip


if __name__ == '__main__':
    ip = get_proxy()
    for i in ip:
        print(i)