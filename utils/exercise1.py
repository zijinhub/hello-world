# -*- coding: utf-8 -*-
import configparser
from configparser import  ConfigParser
import os
#实例化configParser对象
config=configparser.ConfigParser()
# 获取当前脚本所在文件夹路径
curpath = os.path.dirname(os.path.realpath(__file__))
print(curpath)
# 获取上一级目录
file_name = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print(file_name)
# 获取pytest.ini文件路径
configpath = os.path.join(file_name, "pytest.ini")
print(configpath)
#读取ini文件
config.read(configpath)
#-sections 得到所有的section，并以列表的形式返回
print(config.sections())
#-option 得到该sectiond 的所有option
print(config.options("jl"))
#-items 得到该sections的所有键值对
print(config.items("jl"))
#-get(section,option),得到section中option值，返回为string类型
print(config.get("jl","base_url"))
#-getint(section,option),得到section中option值，返回为int类型
'''首先得到配置文件的所有分组，然后根据分组逐一展示所有'''
for sections in config.sections():
    for items in config.items(sections):
        print(items)