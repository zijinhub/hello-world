
import  pytest
# 注册自定义参数 cmdopt 到配置对象
def pytest_addoption(parser):
    parser.addoption("--cmdopt", action="store",
                     default="这个是默认值...",
                     help="将命令行参数 ’--cmdopt' 添加到 pytest 配置中")


# 从配置对象中读取自定义参数的值
@pytest.fixture(scope="session")
def cmdopt(request):
    return request.config.getoption("--cmdopt")


# 将自定义参数的值打印出来
@pytest.fixture(autouse=True)
def fix_1(cmdopt):
    print('\n --cmdopt的值：', cmdopt)


if __name__ == '__main__':
    # 使用参数
    pytest.main(['-s', '--cmdopt=98k'])             #-s: 显示程序中的print/logging输出