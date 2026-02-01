'''
@Project    ：python-autotest-trae
@File       ：demo_read_data.py
@Date       ：2026/1/3 23:17:35
@Author     ：JinJiacheng
@description：读取数据工具类
'''

from common.read_data import data
import os


def load_ini():
    # 获取项目的根目录
    BASE_PATH = os.path.dirname(os.path.dirname(__file__))

    # 组装mysql配置文件的路径
    MYSQL_CONFIG = os.path.join(BASE_PATH, "config", "mysql.ini")
    res = data.load_ini(file_path=MYSQL_CONFIG)
    print(res)


def load_yaml():
    # 获取项目的根目录
    BASE_PATH = os.path.dirname(os.path.dirname(__file__))
    YAML_FILE = os.path.join(BASE_PATH, "data", "base_data.yaml")
    res = data.load_yaml(file_path=YAML_FILE)
    print(res)


if __name__ == '__main__':
    load_yaml()
