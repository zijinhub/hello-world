# !/usr/bin/env python
# -*-coding: utf-8-*-
# @ProjectName : scp_rewrite
# @FileName : testcase_set.py
# @Time : 2020/4/27 15:21
# @Author : Nick


import pytest
import allure


@pytest.mark.run(order=1)
@pytest.mark.smoke
def test_sell_api(per_sell_case):
    """
    1.下面的函数可以将数据库的备注动态的输入到allure的报告中，这个方法allure.dynamic，看官网通常是添加加到函数体内，使用函数内的数据动态生成；
它下面的方法使用和之前的都有一样，唯一多的就是他可以使用函数体内的数据
    2.可以使用数据库中的caseid动态添加allure标签，
    3.根据玩法名（playEname）allure.dynamic.feature("销售接口_" + per_record['playEname'])、
      投注方式（allure.dynamic.story(per_record['playEname'] + '_' + per_record['playType'] + '_case')）动态
      生成报告中的层级结构
    :param per_sell_case:test
    :return:
    """
    per_record, recv, sell_term_code = per_sell_case
    allure.dynamic.feature("销售接口_" + per_record['playEname'])
    allure.dynamic.story(per_record['playEname'] + '_' + per_record['playType'] + '_case')
    allure.dynamic.severity(allure.severity_level.CRITICAL)
    allure.dynamic.description("用例信息：" + "期号：" + sell_term_code + "金额：" +
                               str(per_record['money']) + "    测试点：" + per_record['description'])
    assert '100000' == recv['BackCode']






@pytest.mark.run(order=2)
@pytest.mark.smoke
def test_query_api(per_query_test):
    """
    # 下面的函数测试了，可以将数据库的备注动态的输入到allure的报告中，可以使用数据库中的caseid
    测试了动态添加allure标签，不用再去处理
    :param per_query_test:
    :return:
    """
    sell_term_code, ticket_code, playEname, runcode, recv = per_query_test
    print(sell_term_code, ticket_code, playEname)

    allure.dynamic.feature("查询接口_" + playEname)
    allure.dynamic.story(playEname + '_' + sell_term_code + '_case')
    allure.dynamic.severity(allure.severity_level.CRITICAL)
    allure.dynamic.description("查询用例详情：{}, 期号：{}, 流水号：{},票号：{}".format(playEname, sell_term_code, runcode, ticket_code))
    assert '100000' == recv['BackCode']


@pytest.mark.run(order=3)
# @pytest.mark.smoke
def test_encash_api(encash_test_case):
    """
    # 下面的函数测试了，可以将数据库的备注动态的输入到allure的报告中，可以使用数据库中的caseid
    测试了动态添加allure标签，不用再去处理
    :param query_test_case:
    :return:
    """
    playEname, sell_term_code, ticket_code, recv = encash_test_case

    allure.dynamic.feature("兑奖接口_" + playEname)
    allure.dynamic.story(playEname + '_' + sell_term_code + '_case')
    allure.dynamic.severity(allure.severity_level.CRITICAL)
    allure.dynamic.description("兑奖用例详情：玩法{}, 期号：{}, 票号：{} ".format(playEname, sell_term_code, ticket_code))
    assert '100000' == recv['BackCode']
