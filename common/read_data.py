#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project    ：python-autotest-trae 
@File       ：read_data.py
@IDE        ：PyCharm 
@Date       ：2025/12/23 22:32:41 
@Author     ：JinJiacheng
@description：读取文件工具类
'''
import os.path
from configparser import ConfigParser

import yaml
import json
from common.logger import logger


class MyConfigParserf(ConfigParser):

    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    # 重写 configparser 中的 optionxform 函数，解决 .ini 文件中的 键option 自动转为小写的问题
    def optionxform(self, optionstr: str) -> str:
        return optionstr


class ReadFileData():

    def __init__(self):
        pass

    def load_ini(self, file_path):
        """
        加载ini配置文件
        :param file_path: 文件路径
        :return: data
        """
        logger.info(f"【加载配置文件】：{file_path} ")
        config = MyConfigParserf()
        config.read(file_path, encoding="UTF-8")
        data = dict(config._sections)
        return data

    def load_yaml(self, file_path):
        """
        加载yaml配置文件
        :param file_path: 文件路径
        :return: data
        """
        logger.info(f"【加载配置文件】：{file_path} ")
        with open(file_path, encoding="UTF-8") as f:
            # 使用yaml.safe_load()方法加载yaml文件，不是用load()方法避免yaml被反序列化存在漏洞
            data = yaml.safe_load(f)
        return data


# 初始化实例
data = ReadFileData()
