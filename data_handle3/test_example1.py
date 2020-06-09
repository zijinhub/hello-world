import pytest
import basic_data
# @pytest.mark.parametrize("x", [1,2,3])
# @pytest.mark.parametrize("y", [0])
list1=[[{"RunCode":155551},{"expect":"10002"},{"case_id":"runcode参数为空"}],[{"userid":11},{"expect":"10002"}
,{"case_id":"userid参数为空"}]]

@pytest.fixture()
def para(request):
    general_out_content = {"PartnerId": 'basic_data.partner_id',
                           "TimeStamp": Toolkit.time_stamp_gen(),
                           "SerialNum": basic_data.serial_num_gen(),
                           "Version": basic_data.version,
                           "Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                           "ReqContent": ""}
    sell_data={"RunCode": 11,
     "UserId": 22,
     "AccessType": 2,
     "PlayEname": 33,
     "SellTermCode": "",
     "LoginSession": 44,
     "Money": 55,
     "DrawWay": 1,
     "TicketCode": 66,
     "CheckCode": ""}
    sell_data.items()
    sell_data.update(request.param[0])
    general_out_content.update(ReqContent=sell_data)


    # for dict_key in request.param.keys():
    #     para_name=dict_key
    return request.param[1]["expect"],request.param[2]["case_id"]
data =[{"RunCode":12},{"userid":11}]

def case_id(item):
    return item[2]['case_id']

@pytest.mark.parametrize("para", list1, ids=case_id,indirect=True)
def test_para(para):
    print(para)
    assert para

# case_id(data)


