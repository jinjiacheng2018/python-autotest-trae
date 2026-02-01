#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project    ：python-autotest-trae 
@File       ：logger.py
@IDE        ：PyCharm 
@Date       ：2025/12/23 22:54:52 
@Author     ：JinJiacheng
@description：日志模块
'''

import logging
import time
import os

# 获取项目的根目录
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# 定义日志存储的位置(没有则创建)
LOG_PATH = os.path.join(BASE_PATH, "logs")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


class Logger():
    def __init__(self):
        # 定义存储日志文件的路径，并创建日志实例及设置日志级别
        self.logName = os.path.join(LOG_PATH, "{}.log".format(time.strftime("%Y%m%d")))
        self.logger = logging.getLogger("log")
        self.logger.setLevel(logging.DEBUG)

        # 清除已有的处理器，避免重复添加
        self.logger.handlers.clear()

        # 定义基础日志格式（用于文件）
        formatter = logging.Formatter(
            '[%(asctime)s][%(filename)s %(lineno)d]%(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S"
        )

        # 定义控制台颜色格式器
        class ColorFormatter(logging.Formatter):
            COLOR_MAP = {
                logging.DEBUG: '\033[36m',  # 青色
                logging.INFO: '\033[37m',  # 白色
                logging.WARNING: '\033[33m',  # 黄色
                logging.ERROR: '\033[31m',  # 红色
                logging.CRITICAL: '\033[35m',  # 紫色
            }
            RESET = '\033[0m'

            def format(self, record):
                msg = super().format(record)
                color = self.COLOR_MAP.get(record.levelno, self.RESET)
                return f"{color}{msg}{self.RESET}"

        color_formatter = ColorFormatter(
            '[%(asctime)s][%(filename)s %(lineno)d]%(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S"
        )

        # 设置文件日志处理器
        file_handler = logging.FileHandler(self.logName, mode="a", encoding="UTF-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # 设置控制台日志处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(color_formatter)

        # 添加处理器到记录器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)


# 实例化日志类
logger = Logger().logger

if __name__ == '__main__':
    # 测试不同级别的日志输出
    logger.debug("---调试测试---")
    logger.info("---信息测试---")
    logger.warning("---警告测试---")
    logger.error("---错误测试---")
    logger.critical("---严重测试---")
