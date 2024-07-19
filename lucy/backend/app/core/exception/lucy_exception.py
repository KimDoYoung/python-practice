class LucyException(Exception):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(self.detail)

class KisException(LucyException):
    pass

class KisApiException(LucyException):
    pass


class LsException(LucyException):
    pass

class AccessTokenExpireException(KisException):
    pass

class AccessTokenInvalidException(KisException):
    pass

class LsApiException(LsException):
    pass

class InvalidResponseException(LucyException):
    pass

