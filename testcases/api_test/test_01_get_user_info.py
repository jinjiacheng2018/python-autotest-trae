'''
@Project    ：python-autotest-trae
@File       ：test_01_get_user_info.py
@Date       ：2026/1/5 22:33:03
@Author     ：JinJiacheng
@description：描述信息
'''

import allure
import pytest

from testcases.conftest import api_data
from common.logger import logger


@allure.step("步骤1 ==>> 获取所有用户信息")
def step_1():
    logger.info("步骤1 ==>> 获取所有用户信息")


@allure.step("步骤2 ==>> 获取某个用户的信息")
def step_2(username):
    logger.info(f"步骤2 ==>> 获取【{username}】的信息")


# @allure.severity 标注测试报告中的“严重级别（Severity）”，用于给测试用例打重要性标签，方便在报告中分类、筛选、统计和决策。
# @allure.epic 用于描述测试用例所属的大模块，比如：用户模块、订单模块等等。
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("xxx管理系统")
@allure.feature("用户管理")
class TestGetUserInfo():

    @allure.title("获取用户信息")
    @allure.story("功能：获取所有用户")
    @allure.description("获取所有用户的用例")
    @pytest.mark.single
    @pytest.mark.parametrize("except_result,except_code,except_msg", api_data["test_get_all_user_info"])
    def test_get_all_user_info(self, user_business, except_result, except_code, except_msg):
        """获取所有用户的用例"""
        logger.info("\n******************** 开始执行用例 ********************")
        step_1()
        result = user_business.get_all_users_info()
        assert result.response.status_code == 200
        assert result.success == except_result, logger.error("用例执行失败")
        logger.info(f"code ==>> 期望结果是：{except_code}，实际结果是：{result.code}")
        assert result.code == except_code
        assert except_msg in result.msg
        logger.info("******************** 结束执行用例 ********************")

    @allure.title("根据用户名获取某个用户")
    @allure.story("功能：根据用户名获取某个用户")
    @allure.description("获取某个用户的用例")
    @pytest.mark.single
    @pytest.mark.parametrize("username,except_result,except_code,except_msg", api_data["test_get_one_user_info"])
    def test_get_one_user_info(self, user_business, username, except_result, except_code, except_msg):
        """获取某个用户的用例"""
        logger.info("\n******************** 开始执行用例 ********************")
        step_1()
        result = user_business.get_one_user_info(username)
        assert result.response.status_code == 200
        assert result.success == except_result, logger.error("用例执行失败")
        logger.info(f"code ==>> 期望结果是：{except_code}，实际结果是：{result.code}")
        assert result.code == except_code
        assert except_msg in result.msg
        logger.info("******************** 结束执行用例 ********************")


if __name__ == "__main__":
    pytest.main(["-q", "-s", "test_01_get_user_info.py"])
