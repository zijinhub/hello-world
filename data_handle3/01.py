import pytest
@pytest.fixture()
def is_null(request):
    param1 = request.param
    content1 = {"aa":11 ,
                "bb": 22,
                "cc": 33
                }
    content1.update(param1)
    print(param1)
    print(type(param1))
    print(content1)
    return content1


data = [
    {"aa": "name1"},
    {"bb": "name2"},
    {"cc": ''},
]


@pytest.mark.parametrize("logins", data, indirect=True)
def test_name_pwd(logins):
    print(logins)
    # print(f"账号是：{logins['username']}，密码是：{logins['pwd']}")


data=[{"RunCode":""},
      {"UserId":""},
        {"AccessType":""},
        {"PlayEname": ""},
        {"SellTermCode": ""},
        {"LoginSession": ""},
        {"Money": ""},
        {"DrawWay": ""},
        {"TicketCode": ""},
      {"CheckCode": ""}]