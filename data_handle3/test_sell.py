'''
1参数测试
#参数必填项校验
#组合参数校验（投注金额与注码不符）
#参数类型：字符串、整数、时间
参数格式
#参数边界值校验：最大，最小值，字符串长度
#包含特殊字符
#枚举值：比如投注方式可选1或2

2.业务功能测试
#正常投注功能（查表sell_bet_code，可覆盖所有玩法和投注类型 ）
#异常投注（
投注号码格式校验，投注金额与注码不符，数据通过查sell_error_bet_code）'''
#玩法不存在
import pytest
import allure


class Test_sell:

    @pytest.mark.run(order=1)
    @pytest.mark.smoke
    def test_sell_api(self,per_sell_case):

        per_record, recv, sell_term_code = per_sell_case
        allure.dynamic.feature("投注测试_" + per_record['playEname'])
        allure.dynamic.story(per_record['playEname'] + '_' + per_record['playType'] + '_case')
        allure.dynamic.severity(allure.severity_level.CRITICAL)
        allure.dynamic.description("用例信息：" + "期号：" + sell_term_code + "金额：" +
                                   str(per_record['money']) + "    测试点：" + per_record['description'])
        assert '100000' == recv['BackCode']

    @allure.feature("销售模块")
    def test_sell_param(self,sellparams_test_case):
        expect, recv ,case,test_id= sellparams_test_case
        if test_id == "paramcheck":
            allure.dynamic.story('参数测试' )
        elif test_id=="normaltest":
            allure.dynamic.story('正常投注测试')
        else:
            allure.dynamic.story('异常投注测试')

        allure.dynamic.title(case)
        allure.dynamic.severity(allure.severity_level.NORMAL)
        allure.dynamic.description(case)
        assert expect == recv['BackCode']


