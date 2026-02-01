#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project    ：python-autotest-trae 
@File       ：mysql_operate.py
@IDE        ：PyCharm 
@Date       ：2025/12/23 22:41:07 
@Author     ：JinJiacheng
@description：MySQL操作库
'''

import os
import pymysql
from common.logger import logger
from common.read_data import data

# 获取项目的根目录
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# 组装mysql配置文件的路径,读取组装配置
MYSQL_CONFIG = os.path.join(BASE_PATH, "config", "mysql.ini")
mysql_data = data.load_ini(MYSQL_CONFIG)["mysql"]

DB_CONFIG = {
    "host": mysql_data["MYSQL_HOST"],
    "port": int(mysql_data["MYSQL_PORT"]),
    "user": mysql_data["MYSQL_USER"],
    "password": mysql_data["MYSQL_PWD"],
    "database": mysql_data["MYSQL_DB"]
}


class MySQLDB():

    def __init__(self, db_config=DB_CONFIG):
        # 初始方法设置连接(通过**传参，将数据拆包，避免挨个写参数。注意：端口需要是int类型)
        self.db_config = db_config
        self.connect = None
        self.cursor = None
        try:
            self.connect = pymysql.connect(**db_config, charset="utf8", autocommit=True)
            # 通过连接对象获取一个游标对象（执行语句均是用游标对象执行，设置查询结果以字典格式输出）
            self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as e:
            logger.error(f"初始化数据库连接失败: {e}")

    def select_db(self, sql):
        """
        查询数据库方法
        :param sql: 查询sql
        :return: data
        """
        if not self.connect:
             logger.error("数据库未连接，无法执行查询")
             return []
        # 检查连接是否断开，如果断开则重新连接
        self.connect.ping(reconnect=True)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        logger.info(f"【执行查询语句，影响 {len(data)} 行】：{sql}")
        return data

    def execute_db(self, sql):
        """
        执行增加/删除/修改语句
        :param sql: 增删改sql
        :return: rows
        """
        if not self.connect:
             logger.error("数据库未连接，无法执行操作")
             return 0
        try:
            # 检查是否断开连接，如果断开后则重连
            self.connect.ping(reconnect=True)
            # 使用游标对象执行sql
            counts = self.cursor.execute(sql)
            logger.info(f"【执行修改语句,影响 {counts} 行】：{sql}")
            # 执行提交事务
            self.connect.commit()
            return counts
        except Exception as e:
            # 执行语句报错则进行回滚
            logger.error(f"【执行 {sql} 报错回滚，原因】：{e}")
            self.connect.rollback()

    def __del__(self):
        # del方法释放资源,关闭游标、连接对象
        self.cursor.close()
        self.connect.close()


# 初始化数据库实例
mysql_db = MySQLDB()
