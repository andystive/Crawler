from crawler.proxy.get_proxy import *
import os
import sys
#print(get_proxy())

print(os.path.split(os.path.realpath(__file__))[0])
print(os.path.split(os.path.realpath(__file__))[1])
print(os.path.realpath(__file__))


'''
            except:
                print('代理IP出错,更换代理IP！')
            else:
                print('写入第{}页数据成功！'.format(page))
'''


except:
print('代理ip池为空')