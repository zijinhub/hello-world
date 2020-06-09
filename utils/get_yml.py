# coding:utf-8
import yaml
import os


def read_yaml(x):
    # 获取当前脚本所在文件夹路径
    curpath = os.path.dirname(os.path.realpath(__file__))
    print(curpath)
    #获取上一级目录
    file_name=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    print(file_name)
    # 获取yaml文件路径
    yamlpath = os.path.join(file_name, "data",x)
    print(yamlpath)

    # open方法打开直接读出来
    f = open(yamlpath, 'r', encoding='utf-8')
    content=yaml.load(f.read(),Loader=yaml.Loader)
    # d = yaml.safe_load(f.read())  # 用load方法转字典
    return content

if __name__=="__main__":
    # data=read_yaml("params.yml")
    # print(data["selldata"]["S3"])
    data=read_yaml("paramcheck.yml")
    print(data)
    a=data["sell_params"]
    print(type(a))
    print(a['checkparam'])
