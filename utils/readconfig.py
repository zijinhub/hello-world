# -*- coding: utf-8 -*-
import configparser
from configparser import  ConfigParser
import os
class config:
    def __init__(self):

        self.config=configparser.ConfigParser()
        # curpath = os.path.dirname(os.path.realpath(__file__))
        file_name = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        # 获取pytest.ini文件路径
        self.configpath = os.path.join(file_name, "pytest.ini")

    def getconfig(self,key,value):
        # print(self.configpath)
        self.config.read(self.configpath)
        return self.config.get(key,value)

if __name__=="__main__":
    url=config().getconfig("jl","ip")+config().getconfig("jl","loginpath")
    print(url)