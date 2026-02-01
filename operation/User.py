'''
@Project    ：python-autotest-trae
@File       ：User.py
@Date       ：2026/1/3 21:53:15
@Author     ：JinJiacheng
@description：用户关键字封装类
'''

from common.logger import logger
from core.result_base import ResultBase


class UserBusiness:
    def __init__(self, client):
        self.client = client

    def get_all_users_info(self) -> ResultBase:
        """
        获取所有的用户
        :return: 自定义个关键字返回结果
        """
        result = self.client.list_all_users()
        if result.code == 0:
            result.success = True
        else:
            logger.error("【获取所有用户信息失败】")

        # 关键字中根据项目要求是否需要返回业务数据，若不需求则删除该行代码
        return result

    def get_one_user_info(self, username: str) -> ResultBase:
        """
        获取某个用户信息
        :param username: 用户名
        :return: 自定义个关键字返回结果
        """
        result = self.client.list_user_by_name(username)
        if result.code == 0:
            result.success = True
        else:
            logger.error("【获取单个用户信息失败】")

        # 关键字中根据项目要求是否需要返回业务数据，若不需求则删除该行代码
        return result

    def register_user(self, username: str, password: str, sex: str, telephone: str, address: str) -> ResultBase:
        """
        注册用户
        :param username: 用户名
        :param password: 密码
        :param sex: 性别
        :param telephone: 手机号
        :param address: 地址
        :return: 自定义个关键字返回结果
        """
        user_json = {
            "username": username,
            "password": password,
            "sex": sex,
            "telephone": telephone,
            "address": address
        }
        headers = {
            "Content-Type": "application/json"
        }

        result = self.client.register(json=user_json, headers=headers)
        if result.code == 0:
            result.success = True
        else:
            logger.error("【注册用户失败】")

        return result

    def login_user(self, username: str, password: str) -> ResultBase:
        """
        登录用户
        :param username: 用户名
        :param password: 密码
        :return: 自定义个关键字返回结果
        """
        user_json = {
            "username": username,
            "password": password
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        result = self.client.login(data=user_json, headers=headers)
        if result.code == 0:
            result.success = True
        else:
            logger.error("【登录用户失败】")

        return result

    def update_user(self, id: str, admin_user: str, password: str, sex: str, telephone: str, address: str,
                    token: str) -> ResultBase:
        """
        修改用户信息
        :param id: 用户id
        :param admin_user: 管理员用户
        :param password: 密码
        :param sex: 性别
        :param telephone: 手机号
        :param address: 地址
        :param token: 令牌
        :return: 自定义个关键字返回结果
        """
        user_json = {
            "admin_user": admin_user,
            "password": password,
            "token": token,
            "sex": sex,
            "address": address,
            "telephone": telephone
        }
        headers = {
            "Content-Type": "application/json"
        }

        result = self.client.update(user_id=id, json=user_json, headers=headers)

        return result
