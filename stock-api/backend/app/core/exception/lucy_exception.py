class LucyException(Exception):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(self.detail)

class KisException(LucyException):
    pass

class KisAccessTokenExpireException(KisException):
    pass

class KisAccessTokenInvalidException(KisException):
    pass
