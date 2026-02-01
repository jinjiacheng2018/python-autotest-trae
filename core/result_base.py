'''
@Project    ：python-autotest-trae
@File       ：result_base.py
@Date       ：2026/1/2 23:39:02
@Author     ：JinJiacheng
@description：定义自定义的返回结果类，主要用于自定义关键字返回结果。（例如：java开发中自定的标准json返回对象）
'''


class ResultBase:
    def __init__(self, success: bool = False, msg: str = None, response=None, data=None, code=None):
        """
        关键字执行结果基类，error是给测试看的，msg是接口的标准返回
        """
        self.code = code  # 接口返回 code
        self.success = success  # 接口关键字是否成功
        self.data = data  # 业务数据
        self.msg = msg  # 接口返回的 msg
        self.response = response  # 原始requests.Response对象

    def __repr__(self):
        """
        定义“这个对象被打印 / 查看时的样子，类似toString单不完全相同
        """
        return (
            f"<ResultBase success={self.success}, code={self.code}, "
            f"msg={self.msg}, data={self.data}>, "
        )

    @classmethod
    def from_response(cls, response):
        """
        定义一个类方法：从requests.Response构造 ResultBase
        """
        try:
            body = response.json()
        except Exception:
            body = None

        # 业务成功判断逻辑（可按后端接口的编码、规范调整）
        success = bool(body and body.get("code") == 0)

        return cls(
            success=success,
            code=body.get("code") if body else response.status_code,
            msg=body.get("msg") if body else response.reason,
            data=body.get("data") if body else None,
            response=response
        )
