from test.utils.get_yml import read_yaml
from test.utils.myrequest import myrequest
import allure
import pytest
from test.utils.readconfig import config
import logging

@allure.feature("登录接口")
class Test_login:
    myrequest = myrequest()
    content=read_yaml("params.yml")
    data=content["login"]
    loginids=[]
    for x in data:
        loginids.append(x[2])

    login_url=config().getconfig("jl","ip")+config().getconfig("jl","loginpath")


    '''使用allure.title(title)可以重命名测试用例在allure报告中的名称,test_login'''

    # @allure.description("登录成功")
    @allure.title("登录")
    @pytest.mark.parametrize("logindata", data, indirect=True,ids=loginids)
    def test_login(self, logindata):
        res=self.myrequest.post(url=self.login_url,data=logindata)
        # logging.info(req)
        print(res)
        assert "成功" == res["BackMsg"]

