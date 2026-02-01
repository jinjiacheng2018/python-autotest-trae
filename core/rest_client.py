#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project    ：python-autotest-trae 
@File       ：rest_client.py
@IDE        ：PyCharm 
@Date       ：2025/12/27 23:21:49 
@Author     ：JinJiacheng
@description：封装request类
'''
import requests
import json as complexjson

from requests import RequestException

from common.logger import logger
from core.result_base import ResultBase


class RestClient():
    """
        requests 二次封装
        目标：
        1. 统一请求入口
        2. 统一异常处理
        3. 自动拼接 base_url
        4. 支持 session / token
    """

    def __init__(self, base_url):
        """
        实例化时，将环境地址带入
        :param base_url: 接口url
        """
        self.base_url = base_url

        # requests.session()创建一个“有记忆的HTTP客户端”，让多次请求像同一用户在连续操作；若不用则每次请求都是一个全新的，无历史关联
        self.session = requests.session()

    def get(self, url, **kwargs):
        """
        get请求（注意要有返回）
        """
        return self.request(url, "GET", **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """
        post请求（注意要有返回）
        """
        return self.request(url, "POST", data, json, **kwargs)

    def put(self, url, data=None, **kwargs):
        """
        put请求（注意要有返回）
        """
        return self.request(url, "PUT", data, **kwargs)

    def delete(self, url, **kwargs):
        """
        delete请求（注意要有返回）
        """
        return self.request(url, "DELETE", **kwargs)

    def request(self, url, method, data=None, json=None, **kwargs):
        """
        封装request方法
        :param url: 接口url地址
        :param method: 请求方法
        :param data: 表单请求参数
        :param json: json请求参数
        :param kwargs: 其他可变长度参数
        :return:
        """
        url = self.base_url + url
        headers = dict(**kwargs).get("headers")
        params = dict(**kwargs).get("params")
        files = dict(**kwargs).get("params")
        cookies = dict(**kwargs).get("params")
        self.request_log(url, method, data, json, headers, params, files, cookies)

        try:
            if method == "GET":
                return ResultBase.from_response(self.session.get(url, **kwargs))
            if method == "POST":
                return ResultBase.from_response(self.session.post(url, data, json, **kwargs))
            if method == "DELETE":
                return ResultBase.from_response(self.session.delete(url, **kwargs))
            if method == "PUT":
                if json is not None:
                    # PUT 和 PATCH 中没有提供直接使用json参数的方法，因此需要用data来传入
                    data = complexjson.dumps(json)
                return ResultBase.from_response(self.session.put(url, data, **kwargs))
            if method == "PATCH":
                if json is not None:
                    data = complexjson.dumps(json)
                return ResultBase.from_response(self.session.patch(url, data, **kwargs))
        except TimeoutError as e:
            logger.error(f"请求超时，异常信息：{e}")
            return ResultBase(success=False, msg="请求超时", response=None)
        except ConnectionError as e:
            logger.error(f"连接失败，异常信息：{e}")
            return ResultBase(success=False, msg="连接错误", response=None)
        except RequestException as e:
            logger.error(f"请求异常，异常信息：{e}")
            return ResultBase(success=False, msg="请求异常", response=None)

    def request_log(self, url, method, data=None, json=None, headers=None, params=None, files=None, cookies=None):
        """
        请求方法日志打印方法（使用if判断：None / "" / False 都不会打印）
        :param url: 请求url
        :param method: 请求方法
        :param data: 表单请求参数
        :param json: json请求参数
        :param headers: 请求头
        :param params: 请求参数
        :param files: 请求文件
        :param cookies: 请求cookies
        :return: None
        """
        logger.info("------------------------------------请求开始------------------------------------")
        if url: logger.info(f"【请求url】：{url}")
        if method: logger.info(f"【请求方法】：{method}")
        if headers: logger.info(f"【请求头】：{headers}")
        if data: logger.info(f"【表单参数】：{data}")
        if json: logger.info(f"【JSON参数】：{json}")
        if params:
            logger.info(f"【其他参数】：{params}")
            logger.info(f"【请求文件】：{files}")
            logger.info(f"【请求cookies】：{cookies}")
        logger.info("------------------------------------请求结束------------------------------------")
