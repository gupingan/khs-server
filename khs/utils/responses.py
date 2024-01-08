from flask import jsonify


class RespCode(object):
    SUCCESS = 200  # 成功
    FAIL = -1  # 失败
    NOT_FOUND = 404  # 未找到相关信息
    INVALID_ARGUMENT = 422  # 无效的参数
    ERROR = 500  # 其它错误


class RespBody(object):
    """
   封装响应体
   """

    def __init__(self, data=None, code=RespCode.SUCCESS,
                 msg="success"):
        if data is None:
            data = {}
        self._data = data
        self._msg = msg
        self._code = code

    def __call__(self, **kwargs):
        """
        采用关键词传参修改data中的值
        :param kwargs:
        :return:
        """
        self._data.update(kwargs)
        return self

    def update(self, code=None, data=None, msg=None):
        """
       更新默认响应文本
       :param code:响应状态码
       :param data: 响应数据
       :param msg: 响应消息
       :return:
       """
        if code is not None:
            self._code = code
        if data is not None:
            self._data = data
        if msg is not None:
            self._msg = msg

    @property
    def body(self):
        """
       输出响应文本内容
       :return:
       """
        temp = self.__dict__
        temp["data"] = temp.pop("_data")
        temp["msg"] = temp.pop("_msg")
        temp["code"] = temp.pop("_code")
        return jsonify(temp)
