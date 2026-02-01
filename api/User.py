#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project    ：python-autotest-trae 
@File       ：User.py.py
@IDE        ：PyCharm 
@Date       ：2025/12/28 20:33:36 
@Author     ：JinJiacheng
@description：描述信息用户
'''
import os.path
from common.read_data import data
from core.rest_client import RestClient

class User(RestClient):

    def __init__(self, base_url, **kwargs):
        super().__init__(base_url, **kwargs)

    def list_all_users(self, **kwargs):
        """
        获取所有的用户
        请求方式：GET
        请求地址：http://127.0.0.1:9999/users
        """
        return self.get("/users", **kwargs)

    def list_user_by_name(self, user_name: str, **kwargs):
        """
        根据名字获取用户
        请求方式：GET
        请求地址：http://127.0.0.1:9999/users/wintest
        """
        return self.get(f"/users/{user_name}", **kwargs)

    def register(self, **kwargs):
        """
        注册用户
        请求方式：POST
        请求地址：http://127.0.0.1:9999/register
        请求头：Content-Type: application/json
        Body：{"username": "wintest5", "password": "123456", "sex": "1", "telephone":"13500010005", "address": "上海市黄浦区"}
        """
        return self.post("/register", **kwargs)

    def login(self, **kwargs):
        """
        登录用户
        请求方式：POST
        请求地址：http://127.0.0.1:9999/login
        请求头：Content-Type: application/x-www-form-urlencoded
        Body：username=wintest&password=123456
        """
        return self.post("/login", **kwargs)

    def update(self, user_id: str, **kwargs):
        """
        更新用户信息
        请求方式：PUT
        请求地址：http://127.0.0.1:9999/update/user/3
        请求头：Content-Type: application/json
        请求Body：{"admin_user": "wintest", "token": "f54f9d6ebba2c75d45ba00a8832cb593", "sex": "1", "address": "广州市天河区", "password": "12345678", "telephone": "13500010003"}
        """
        return self.put(f"/update/user/{user_id}", **kwargs)

    def delete(self, user_name: str, **kwargs):
        """
        删除用户
        请求方式：POST
        请求地址：http://127.0.0.1:9999/delete/user/test
        请求头：Content-Type: application/json
        请求Body：{"admin_user": "wintest", "token": "f54f9d6ebba2c75d45ba00a8832cb593"}
        """
        # 注意，如果delete方法与父类方法同名，则需要使用super()
        # super().delete(f"/delete/user/{user_name}", **kwargs)
        return self.post(f"/delete/user/{user_name}", **kwargs)
