# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : scp_rewrite
# @FileName : conftest.py.py
# @Time : 2020/5/6 15:40
# @Author : Nick

import pytest
from test.data_handle2 import init_config

from test.data_handle2.toolkit import Toolkit
from test.data_handle2.init_config import basic_data
from test.utils.get_yml import read_yaml

def case_id(item):
    return item['id']


def bet_query_case_id(item):
    return item['PlayEname'] + '_' + item['SellTermCode'] + '_' + item['Runcode']

yaml_data=read_yaml("paramcheck.yml")
session = Toolkit.session_id()

general_out_content = {"PartnerId": basic_data.partner_id,
                       "TimeStamp": Toolkit.time_stamp_gen(),
                       "SerialNum": basic_data.serial_num_gen(),
                       "Version": basic_data.version,
                       "Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                       "ReqContent": ""}


@pytest.fixture()
def per_sell_case(request):
    sell_content = {"RunCode": basic_data.serial_num_gen(),
                    "UserId": basic_data.user_id,
                    "AccessType": 2,
                    "PlayEname": request.param['playEname'],
                    "SellTermCode": "",
                    "LoginSession": session,
                    "Money": request.param['money'],
                    "DrawWay": 1,
                    "TicketCode": request.param['code'],
                    "CheckCode": ""}

    check_code = Toolkit.check_code(sell_content['RunCode'] + general_out_content['PartnerId'] + sell_content['UserId']
                                    + sell_content['TicketCode'] + str(sell_content['Money']) + sell_content['LoginSession'])
    sell_content.update(Checkcode = check_code)
    if request.param['playEname'] == 'B001':
        sell_content.update(SellTermCode = basic_data.ball_term_code)
    if request.param['playEname'] == 'S3':
        sell_content.update(SellTermCode = basic_data.d3_term_code)
    if request.param['playEname'] == 'QL730':
        sell_content.update(SellTermCode = basic_data.QL730_term_code)
    if request.param['playEname'] == 'K3':
        sell_content.update(SellTermCode = basic_data.k3_term_code)
    general_out_content.update(ReqContent=sell_content)

    recv = Toolkit.executive_test(basic_data.sell_profix_url + basic_data.partner_id + '&hashType=md5&hash=',
                                  'sell', general_out_content)

    return request.param, recv, sell_content['SellTermCode']


@pytest.fixture()
def per_query_test(request):

    bet_query_content = {
        "RunCode": ""
    }
    sell_term_code = request.param['SellTermCode']
    ticket_code = request.param['TicketCode']
    playEname = request.param['PlayEname']
    runcode = request.param['Runcode']

    bet_query_content.update(RunCode=runcode)
    general_out_content.update(ReqContent=bet_query_content)

    recv = Toolkit.executive_test(basic_data.bet_query_url + basic_data.partner_id + '&hashType=md5&hash=',
                                  'bet_query', general_out_content)
    return sell_term_code, ticket_code, playEname, runcode, recv


@pytest.fixture()
def encash_test_case(request):
    encash_content = {
        "UserId": basic_data.user_id,
        "RunCode": request.param['Runcode'],
        "TicketCode": request.param['TicketCode'],
        "CheckCode": "",
        "LoginSession": session}
    check_code = Toolkit.check_code(encash_content['UserId'] + encash_content["TicketCode"])

    encash_content.update(CheckCode=check_code)
    general_out_content.update(ReqContent=encash_content)

    sell_term_code = request.param['SellTermCode']
    playEname = request.param['PlayEname']
    ticket_code = request.param['TicketCode']
    recv = Toolkit.executive_test(basic_data.encash_profix_url + basic_data.partner_id + '&hashType=md5&hash=',
                                  'encash', general_out_content)

    return playEname, sell_term_code, ticket_code, recv

#参数校验
@pytest.fixture()
def sellparams_test_case(request):
    sell_content = {"RunCode": basic_data.serial_num_gen(),
                    "UserId": basic_data.user_id,
                    "AccessType": 2,
                    "PlayEname": "B001",
                    "SellTermCode": basic_data.ball_term_code,
                    "LoginSession": session,
                    "Money": 2,
                    "DrawWay": 1,
                    "TicketCode": "0001010203040506~07^",
                    "CheckCode": ""}
    sell_content.update(request.param[0])
    if request.param[3]["id"]!="paramcheck":
        if sell_content['PlayEname'] == 'B001':
            sell_content.update(SellTermCode = basic_data.ball_term_code)
        if sell_content['PlayEname'] == 'S3':
            sell_content.update(SellTermCode = basic_data.d3_term_code)
        if sell_content['PlayEname'] == 'QL730':
            sell_content.update(SellTermCode = basic_data.QL730_term_code)
        if sell_content['PlayEname'] == 'K3':
            sell_content.update(SellTermCode = basic_data.k3_term_code)

    if 'CheckCode' not in request.param[0].keys():

        check_code = Toolkit.check_code(sell_content['RunCode'] + general_out_content['PartnerId'] + sell_content['UserId']
                                    + sell_content['TicketCode'] + str(sell_content['Money']) + sell_content['LoginSession'])
        sell_content.update(CheckCode = check_code)

    # sell_content.update(SellTermCode = basic_data.ball_term_code)

    # sell_content.update(request.param[0])
    # for dict_key in request.param.keys():
    #     para_name=dict_key


    general_out_content.update(ReqContent=sell_content)

    recv = Toolkit.executive_test(basic_data.sell_profix_url + basic_data.partner_id + '&hashType=md5&hash=',
                                  'sell', general_out_content)



    return request.param[1]["expect"], recv,request.param[2]["case"],request.param[3]["id"]

def check_case_id(item):
    return item[3]['id']

def pytest_addoption(parser):
    parser.addoption("--count", action='store', default=1,help="取值:all 或者 一个正整数")

@pytest.fixture(scope='session')
def count(request):
    return request.config.getoption("--count")



def pytest_generate_tests(metafunc):
    """
    #all 全部  6717
SELECT id, playEname,playType,CODE,money,description
FROM sell_bet_code
WHERE (playEname = 'K3' AND playType NOT IN ('baodan','dantuo','fushi','heshudanxuan','daxiaojiou','hezhidaxiao','kuadu','ren2'))
    OR (playEname = 'S3'  AND funPoint IN ('00','01','02','03','04','05','06','07','08','09',
'10','11','12','14','15','20','21','22','23','24',
'25','26','30','31','32','34','35','07','08','09'))
    OR playEname = 'B001'
    OR playEname = 'QL730'
UNION ALL
SELECT id, playEname,playType,CODE,money,description
FROM sell_error_bet_code


#smoke 每个玩法的投注方式，根据销售代码，取一行数据  110
SELECT id, playEname,playType,CODE,money,description
FROM sell_bet_code
WHERE (playEname = 'K3' AND playType NOT IN ('baodan','dantuo','fushi','heshudanxuan','daxiaojiou','hezhidaxiao','kuadu','ren2'))
    OR (playEname = 'S3'  AND funPoint IN ('00','01','02','03','04','05','06','07','08','09',
'10','11','12','14','15','20','21','22','23','24',
'25','26','30','31','32','34','35','07','08','09'))
    OR playEname = 'B001'
    OR playEname = 'QL730'
GROUP BY playEname ,funpoint
UNION ALL
SELECT id, playEname,playType,CODE,money,description
FROM sell_error_bet_code
GROUP BY playEname ,funpoint
    """
    # print(metafunc.config.option)

    if 'per_sell_case' in metafunc.fixturenames:
        # test_case_sell = "SELECT id, playEname,playType,code,money,description FROM sell_bet_code " \
        #                  "WHERE (playEname = 'K3' AND playType NOT IN " \
        #                  "('baodan','dantuo','fushi','heshudanxuan','daxiaojiou','hezhidaxiao','kuadu','ren2'))" \
        #                  "OR (playEname = 'S3'  AND funPoint " \
        #                  "IN ('00','01','02','03','04','05','06','07','08','09','10','11','12','14','15','20','21'," \
        #                  "'22','23','24','25','26','30','31','32','34','35','07','08','09'))" \
        #                  "OR playEname = 'B001' OR playEname = 'QL730'  " \
        #                  "GROUP BY playEname,funpoint,money " \
        #                  "UNION ALL SELECT id, playEname,playType,CODE,money,description FROM sell_error_bet_code " \
        #                  "GROUP BY playEname,funpoint ,money"
        if metafunc.config.getoption('--count'):
            # 查出吉林开通玩法的所有销售用例
            test_case_sell = "SELECT id, playEname,playType,code,money,description FROM sell_bet_code " \
                             "WHERE (playEname = 'K3' AND playType NOT IN " \
                             "('baodan','dantuo','fushi','heshudanxuan','daxiaojiou','hezhidaxiao','kuadu','ren2')) " \
                             "OR (playEname = 'S3'  AND " \
                             "funPoint IN ('00','01','02','03','04','05','06','07','08','09','10','11'," \
                             "'12','14','15','20','21','22','23','24','25','26','30','31','32','34','35'," \
                             "'07','08','09'))OR playEname = 'B001' OR playEname = 'QL730' " \
                             "UNION ALL SELECT id, playEname,playType,CODE,money,description FROM sell_error_bet_code"
        if metafunc.config.getoption('markexpr') == 'smoke':
            test_case_sell = "SELECT id, playEname,playType,code,money,description FROM sell_bet_code WHERE " \
                             "(playEname = 'K3' AND playType NOT IN ('baodan','dantuo','fushi','heshudanxuan'," \
                             "'daxiaojiou','hezhidaxiao','kuadu','ren2')) OR" \
                             " (playEname = 'S3'  AND " \
                             "funPoint IN ('00','01','02','03','04','05','06','07','08','09','10','11','12','14','15'," \
                             "'20','21','22','23','24','25','26','30','31','32','34','35','07','08','09')) " \
                             "OR playEname = 'B001' OR playEname = 'QL730' " \
                             "GROUP BY playEname ,funpoint UNION ALL SELECT id, playEname,playType," \
                             "CODE,money,description FROM sell_error_bet_code GROUP BY playEname ,funpoint"

        sell_data = init_config.get_db_data(test_case_sell, metafunc.config.getoption('--count'))
        metafunc.parametrize('per_sell_case', sell_data, ids=case_id, indirect = True)

    if 'per_query_test' in metafunc.fixturenames:
        test_case_query = "SELECT SellTermCode, TicketCode,PlayEname,Runcode FROM sell_result;"
        query_data = init_config.get_db_data(test_case_query,metafunc.config.getoption('--count'))
        metafunc.parametrize('per_query_test', query_data, ids = bet_query_case_id, indirect = True)

    if 'encash_test_case' in metafunc.fixturenames:
        test_case_encash = "SELECT SellTermCode, TicketCode,PlayEname,Runcode FROM sell_result;"
        encash_data = init_config.get_db_data(test_case_encash,metafunc.config.getoption('--count'))
        metafunc.parametrize('encash_test_case', encash_data, ids = bet_query_case_id, indirect = True)
    if 'sellparams_test_case' in metafunc.fixturenames:
        sellparams=yaml_data["sell_params"]['checkparam']
        metafunc.parametrize('sellparams_test_case',sellparams,ids=check_case_id,indirect=True)



def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
所有的测试用例收集完毕后调用, 可以再次过滤或者对它们重新排序
 items （收集的测试项目列表）
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")