import pytest

'''
# 注册自定义参数 cmdopt 到配置对象
def pytest_addoption(parser):
    parser.addoption("--cmdopt", action="store",
                     default="None",
                     help="将自定义命令行参数 ’--cmdopt' 添加到 pytest 配置中")

def pytest_addoption(parser):
    parser.addoption("--env",    ##注册一个命令行选项
                    default="test",
                    dest="env",
                    help="set test run env")

# 从配置对象获取 cmdopt 的值
@pytest.fixture(scope='session')
def cmdopt(pytestconfig):
    return pytestconfig.getoption('--cmdopt')'''





# def pytest_addoption(parser):
#     parser.addoption(
#         "--stringinput",
#         action="append",
#         default=[],
#         help="list of stringinputs to pass to test functions",
#     )
#
#
# def pytest_generate_tests(metafunc):
#     if "stringinput" in metafunc.fixturenames:
#         metafunc.parametrize("stringinput", metafunc.config.getoption("stringinput"))



##conftest.py
def pytest_addoption(parser):   #parser是一个对象，用来解析命令行参数和ini文件值
    parser.addoption("--cmdopt", action="store",
                     default="type",
                     help="my option:type1 or type2")

    parser.addoption("--env",    ##注册一个命令行选项
                    default="test",
                    dest="env",
                    help="set test run env")

# 从配置对象获取 cmdopt 的值


@pytest.fixture(scope="session")
def cmdopt(request):
    return request.config.getoption("--cmdopt")




