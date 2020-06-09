import pytest
import json
from test.utils.readconfig import config
from test.utils.myrequest import myrequest
from test.utils.sm4 import getcheckcode
import allure
import time
import random

@allure.step("收集测试数据")
@pytest.fixture(scope="session")
def logindata(request):
    if request:
        uid = "2290110100003"
        pwd = "123456"
    else:
        uid = request.param[0]
        pwd = request.param[1]

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

'''
设置fixture，在测试方法中需要sessionid，那么就把sessionid这个函数，传递给类方法
'''
@pytest.fixture(scope="session")
def sessionid(logindata):
    login_url=config().getconfig("jl","ip")+config().getconfig("jl","loginpath")
    data=logindata
    res=myrequest().post(login_url,data)
    return res['RespContent']['LoginSession']



runcode =time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + str(random.randrange(1, 9999)) + str(random.randrange(1, 9999)) + str(random.randrange(1, 9999))
@pytest.fixture(scope="session")
def selldata(request,sessionid):
    runcode = str(random.randrange(1, 9999))
    userid = '2290110100003'
    tickecode = request.param[1]
    money = request.param[2]
    session = sessionid
    checkcode = getcheckcode(runcode + "00101"+ userid + tickecode + money + session)
    parm ={"RunCode":runcode,
        "UserId":"2290110100003",
        "AccessType":"2",
        "PlayEname":"S3",
        "SelltermCode":"2020028",
        "ValidtermCode":"2020028",
        "LoginSession":session,
        "Money": money,
        "Drawway":"1",
        "CheckCode":checkcode,
        "TicketCode":tickecode}
    req_content = {
        "PartnerId": "00101",
        "SerialNum": "2016040003",
        "Version": "1.0.0.0",
        "Token": "2016040003",
        "ReqContent": parm,
        "TimeStamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    }
    print(req_content)
    return req_content

def test_1(sessionid):
    print(sessionid)


if __name__ =='__main__':
    pytest.main(['-s',"conftest.py"])