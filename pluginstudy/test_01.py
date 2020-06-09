# content of test_sample.py
import pytest
def test_answer(cmdopt):
    if cmdopt == "type1":
        print ("first")
    elif cmdopt == "type2":
        print ("second")
    assert 0 # to see what was printed
if __name__ == '__main__':
    # 使用参数
    pytest.main('-s', '--cmdopt=98k')