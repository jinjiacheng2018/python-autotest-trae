from api.User import User
from common.logger import logger

# Demo usage with hardcoded URL
user = User("http://127.0.0.1:9999")


def search_all_users():
    """
    查询所有用户
    """
    print(user.list_all_users().data)


def search_user_by_name():
    """
    根据名字查询用户
    """
    print(user.list_user_by_name("周芷若").data)


def register():
    """
    注册用户
    """
    user_json = {
        "username": "成昆",
        "password": "123456",
        "role": 2,
        "sex": "0",
        "telephone": "15000000006",
        "address": "上海迪士尼"
    }
    headers = {
        "Content-Type": "application/json"
    }
    print(user.register(headers=headers, json=user_json))


def login():
    """
    登录用户
    """
    data = {
        "username": "张无忌",
        "password": "123456"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    result_base = user.login(data=data, headers=headers)
    print(result_base)
    token = result_base.response.json()["login_info"]["token"]
    return token


def update():
    """
    修改用户信息
    """
    user_json = {
        "admin_user": "张无忌",
        "password": "123456",
        "token": f"{login()}",
        "sex": "1",
        "address": "广州市天河区",
        "telephone": "13500010003"
    }
    headers = {
        "Content-Type": "application/json"
    }
    print(user.update(user_id=4, headers=headers, json=user_json))


def delete():
    """
    删除用户
    """
    user_json = {
        "admin_user": "张无忌",
        "token": f"{login()}"
    }
    headers = {
        "Content-Type": "application/json"
    }
    print(user.delete(user_name="成昆", headers=headers, json=user_json))


if __name__ == '__main__':
    # search_all_users()
    # search_user_by_name()
    # login()
    update()
    # register()
    # delete()
