import pytest
import json

@pytest.fixture(scope="module")
def logindata(request):
    uid = request.param["Userid"]
    pwd = request.param["LoginPass"]
    # url = request.param["url"]
    parm = {"Userid": uid, "LoginPass": pwd, "LoginType": "1", "MacAddress": "ABCDEFG123456"}
    req_content = {
        "PartnerId": "00101",
        "SerialNum": "2016040003",
        "Version": "1.0.0.0",
        "Token": "2016040003",
        "ReqContent": parm,
        "TimeStamp": "now"
    }
    return req_content


data = [{"Userid": "2290110100003", "LoginPass": "123456"}]


# print(type(data))
# print(data["Userid"])
'''
@pytest.mark.parametrize(argnames,argvalues)装饰器可以达到批量传送参数的目的，第一个参数是用逗号分隔的
字符串列表，第二个参数是一个值列表，不能是字典（这里被坑过），
添加indirect=true参数是为了把logindata当成一个函数执行，而不是参数，在运行test_login之前，会把data的数据
传递给logindata函数，然后在执行test_login函数时，logindata函数将req_content赋给变量req
'''
@pytest.mark.parametrize("logindata", data, indirect=True)
def test_login( logindata):
    req=logindata
    print(req)

