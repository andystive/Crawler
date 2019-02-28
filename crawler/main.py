from crawler.proxy.get_proxy import *
import os
import sys
#print(get_proxy())
print(os.path.split(os.path.realpath(__file__))[0])
print(os.path.split(os.path.realpath(__file__))[1])
print(os.path.realpath(__file__))



'''
            except Exception as err:
                print('代理ip错误！',err)
                page = page -1
'''


except:
print('代理ip池为空')