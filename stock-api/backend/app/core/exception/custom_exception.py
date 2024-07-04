class CustomException(Exception):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(self.detail)

class KisAccessTokenExpireException(CustomException):
    pass

class KisAccessTokenInvalidException(CustomException):
    pass
