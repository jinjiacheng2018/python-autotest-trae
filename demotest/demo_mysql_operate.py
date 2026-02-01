#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project    ：python-autotest-trae 
@File       ：demo_mysql_operate.py
@IDE        ：PyCharm 
@Date       ：2025/12/27 16:08:56 
@Author     ：JinJiacheng
@description：描述信息
'''
from common.mysql_operate import mysql_db


def mysql_util():
    """ 测试mysql工具 """
    # 增
    insert_sql = "INSERT INTO emp VALUES (7789, 'SCOTT-2', 'ANALYST', 7566, '1982-12-09', 3000.00, NULL, 20);";
    mysql_db.execute_db(insert_sql)

    # 改
    update_sql = "UPDATE emp SET ename = 'SCOTT-2Up' WHERE empno = '7789';"
    mysql_db.execute_db(update_sql)

    # 删
    delete_sql = "DELETE FROM emp WHERE empno = '7789';"
    mysql_db.execute_db(delete_sql)

    # 查
    select_sql = "select * from emp;"
    data = mysql_db.select_db(select_sql)
    for i in data:
        print(i)

if __name__ == '__main__':
    mysql_util()