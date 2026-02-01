'''
@Project    ：python-autotest-trae
@File       ：conftest.py
@Date       ：2026/1/5 22:20:21
@Author     ：JinJiacheng
@description：描述信息
'''
import pytest

from testcases.conftest import api_data


@pytest.fixture(scope="function")
def testcase_data(request):
    """
    获取测试用例数据
    :param request: 是pytest的内建fixture，框架会自动注入request
    :return: 测试用例的值
    """
    testcase_name = request.function.__name__

    if testcase_name not in api_data:
        pytest.fail(f"❌ YAML 中未定义测试用例数据: {testcase_name}")
    return api_data[testcase_name]
