# XXX 异常系统
class BotException(Exception):
    default_detail = 'Bot异常'

    def __init__(self, detail=None):
        if detail is None:
            self.detail = self.default_detail

    def __str__(self):
        return str(self.detail)


class APIException(BotException):
    default_detail = '官方提供API异常'
