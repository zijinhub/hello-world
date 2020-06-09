import pytest
import random


# data = [{"Userid": "2290110100003", "LoginPass": "123456"}]
# data = [( "2290110100003",  "123456","first"),( "2290110100004",  "123456","second")]
data=[['2290110100003', '123456', 'normal'], ["2290110100004",  "123456","second"], ["2290110100004",  "123456","third"]]
# print(type(data))
# print(data["Userid"])
'''
@pytest.mark.parametrize(argnames,argvalues)装饰器可以达到批量传送参数的目的，第一个参数是用逗号分隔的
字符串列表，第二个参数是一个值列表，不能是字典（这里被坑过），
添加indirect=true参数是为了把logindata当成一个函数执行，而不是参数，在运行test_login之前，会把data的数据
传递给logindata函数，然后在执行test_login函数时，logindata函数将req_content赋给变量req
'''
loginids=[]
for x in data:
    loginids.append(x[2])
@pytest.mark.parametrize("logindata", data, indirect=True,ids=loginids)
def test_login( logindata):
    req=logindata
    print(req)

