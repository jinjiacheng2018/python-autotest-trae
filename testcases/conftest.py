'''
@Project    ：python-autotest-trae
@File       ：conftest.py
@Date       ：2026/1/3 23:33:19
@Author     ：JinJiacheng
@description：描述信息
'''

import os
import pytest
import allure
from common.mysql_operate import mysql_db
from common.read_data import data
from common.logger import logger
from api.User import User
from operation.User import UserBusiness

BASE_PATH = os.path.dirname(os.path.dirname(__file__))


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="选择运行环境: dev, test, prod"
    )


@pytest.fixture(scope="session")
def env_config(request):
    """
    获取当前环境配置
    """
    env_name = request.config.getoption("--env")
    config_path = os.path.join(BASE_PATH, "config", f"env_{env_name}.ini")
    if not os.path.exists(config_path):
        # 如果指定环境文件不存在，尝试加载默认 setting.ini
        config_path = os.path.join(BASE_PATH, "config", "setting.ini")
        if not os.path.exists(config_path):
             pytest.fail(f"配置文件未找到: {config_path}")
    
    return data.load_ini(config_path)


@pytest.fixture(scope="session")
def api_client(env_config):
    """
    初始化 API 客户端
    """
    base_url = env_config["host"]["base_url"]
    return User(base_url)


@pytest.fixture(scope="session")
def user_business(api_client):
    # api_client 是通过 pytest 的依赖注入机制注入进来的。
    # 因为 api_client 被定义为一个 @pytest.fixture，
    # 当 user_business fixture 声明了 api_client 作为参数时，
    # pytest 会先执行 api_client fixture，并将其返回值传递给 user_business。
    """
    初始化业务层
    """
    return UserBusiness(api_client)


def get_data(yaml_file_name):
    """
    定义方法获取yaml文件数据
    """
    try:
        yaml_file_path = os.path.join(BASE_PATH, "data", yaml_file_name)
        yaml_data = data.load_yaml(file_path=yaml_file_path)
    except Exception as e:
        pytest.skip("没有找到yaml文件")
    else:
        return yaml_data


base_data = get_data("base_data.yaml")
api_data = get_data("api_test_data.yml")


@allure.step("前置步骤 ==>> 清理数据")
def step_first():
    logger.info("*****************************")
    logger.info("前置步骤开始 ==>> 清理数据")


@allure.step("后置步骤 ==>> 清理数据")
def step_last():
    logger.info("后置步骤开始 ==>> 清理数据")


@allure.step("登录")
def step_login(username):
    logger.info(f"管理员【{username}】登录。")


@pytest.fixture(scope="session")
def login_fixture(api_client):
    """
    登录
    """
    username = base_data["init_admin_user"]["username"]
    passwodd = base_data["init_admin_user"]["password"]

    user_data = {
        "username": username,
        "password": passwodd
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    result = api_client.login(data=user_data, headers=headers)
    step_login(username)

    # yield前是setup，yield后是teardown。yield 的值就是注入到测试用例中的fixture返回值
    yield result.response.json()


@pytest.fixture(scope="session")
def insert_delete_user():
    """删除用户前，先往数据库中插入1条数据"""
    insert_sql = base_data["init_sql"]["insert_delete_user"][0]
    mysql_db.execute_db(insert_sql)
    step_first()
    logger.info(f"【删除用户操作：插入新用户。并执行前置SQL：{insert_sql}】")
    yield
    # yield是在测试用例执行完后执行(ps：有些情况下不给删除管理员用户，需要手动清理插入的数据)
    del_sql = base_data["init_sql"]["del_delete_user"][1]
    mysql_db.execute_db(del_sql)
    step_last()
    logger.info(f"【清理用户操作：清理用户，并执行后置SQL：{del_sql}】")


@pytest.fixture(scope="session")
def delete_register_user():
    """注册用户前，先删除数据，用例执行后要再次清理数据"""
    del_sql = base_data["init_sql"]["delete_register_user"]
    mysql_db.execute_db(del_sql)
    step_first()
    logger.info(f"【注册用户操作：清理用户，并执行前置SQL：{del_sql}】")
    yield
    mysql_db.execute_db(del_sql)
