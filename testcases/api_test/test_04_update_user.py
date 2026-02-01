'''
@Project    ：python-autotest-trae
@File       ：test_04_update_user.py
@Date       ：2026/1/21 22:01:02
@Author     ：JinJiacheng
@description：更新用户用例
'''
import allure
import pytest

from testcases.conftest import api_data
from common.logger import logger


# @allure.severity 标注测试报告中的“严重级别（Severity）”，用于给测试用例打重要性标签，方便在报告中分类、筛选、统计和决策。
# @allure.epic 系统的名称
# @allure.feature 用于描述测试用例所属的大模块，比如：用户模块、订单模块等等。
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("xxx管理系统")
@allure.feature("用户管理")
class TestUpdateUser:

    @allure.story("场景：更新用户")
    @allure.title("功能：更新用户")
    @allure.description("更新用户的用例")
    @pytest.mark.single
    @pytest.mark.parametrize(
        "id, new_password, new_telephone, new_sex, new_address, except_result, except_code, except_msg",
        api_data["test_update_user"])
    def test_update_user(self, login_fixture, user_business, id, new_password, new_telephone, new_sex, new_address,
                         except_result, except_code, except_msg):
        """更新用户的用例"""
        logger.info("\n******************** 测试开始 ********************")
        admin_user = login_fixture["login_info"]["username"]
        token = login_fixture["login_info"]["token"]
        result = user_business.update_user(id, admin_user, new_password, new_sex, new_telephone, new_address, token)
        print(f"=============>{result}")
        assert result.response.status_code == 200
        assert result.success == except_result, logger.error("更新用户用例执行失败")
        assert result.code == except_code
        assert except_msg in result.msg
        logger.info("******************** 测试结束 ********************")
