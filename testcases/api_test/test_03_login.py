'''
@Project    ：python-autotest-trae
@File       ：test_03_login.py
@Date       ：2026/1/19 22:45:31
@Author     ：JinJiacheng
@description：描述信息
'''
import allure
import pytest

from testcases.conftest import api_data
from common.logger import logger


@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("xxx管理系统")
@allure.feature("登录管理")
class TestLogin():

    @allure.title("用户登录")
    @allure.story("功能：用户登录")
    @allure.description("用户登录的用例")
    @pytest.mark.single
    @pytest.mark.parametrize("username, password, except_result, except_code, except_msg",
                             api_data["test_login_user"])
    def test_login_user(self, user_business, username, password, except_result, except_code, except_msg):
        logger.info("\n******************** 测试开始 ********************")
        result = user_business.login_user(username, password)
        assert result.response.status_code == 200
        assert result.success == except_result, logger.error("登录用户用例执行失败")
        assert result.code == except_code
        assert except_msg in result.msg
        logger.info("******************** 测试结束 ********************")
