'''
@Project    ：python-autotest-trae
@File       ：test_02_register.py
@Date       ：2026/1/11 22:17:04
@Author     ：JinJiacheng
@description：描述信息
'''
import pytest

from common.logger import logger
import allure

from testcases.conftest import api_data


@allure.step("步骤1 ==>> 注册用户信息")
def step_1(username, password, telephone, sex, address):
    logger.info(f"步骤1 ==>> 注册用户信息是：{username} - {password} - {telephone} - {sex} - {address}")


# @allure.severity 用户标注用例的严重程度
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("xxx管理系统")
@allure.feature("注册管理")
class TestUserRegister():
    """
    用户注册模块
    """

    @allure.title("注册用户")
    @allure.story("功能：注册用户")
    @allure.description("测试用户注册")
    @pytest.mark.single
    # @pytest.mark.xfail(reason="这个功能暂时有 bug")
    @pytest.mark.parametrize("username, password, telephone, sex, address,except_result, except_code, except_msg",
                             api_data["test_register_user"])
    def test_register_user(self, user_business, delete_register_user, username, password, telephone, sex, address, except_result, except_code, except_msg):
        logger.info("\n******************** 测试开始 ********************")
        step_1(username, password, telephone, sex, address)
        result = user_business.register_user(username, password, sex, telephone, address)
        assert result.response.status_code == 200
        assert result.success == except_result, logger.error("注册用户用例执行失败")
        assert result.code == except_code
        assert except_msg in result.msg
        logger.info("******************** 测试结束 ********************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "--alluredir=./report/allure-results", "test_02_register.py"])
