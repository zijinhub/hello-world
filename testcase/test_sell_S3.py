from test.utils.get_yml import read_yaml
from test.utils.myrequest import myrequest
import allure
import pytest
from test.utils.readconfig import config
import logging
@allure.feature("销售接口")
class Test_sell:
    myrequest=myrequest()
    content=read_yaml("params.yml")
    data=content["sell"]["S3"]

    sellids=[]
    for x in data:
        sellids.append(x[0])

    sell_url=config().getconfig("jl","ip")+config().getconfig("jl","sellpath")

    @allure.story("3D玩法正常销售")
    @pytest.mark.parametrize("selldata", data, indirect=True,ids=sellids)
    @allure.title("")
    def test_sell(self,selldata):
        res=self.myrequest.post(url=self.sell_url,data=selldata)
        # print(res)
        assert "成功" == res["BackMsg"]
        assert "100000"==res["BackCode"]

        # print(res)