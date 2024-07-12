class StockApiException(Exception):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(self.detail)

class AccessTokenExpireException(StockApiException):
    pass

class AccessTokenInvalidException(StockApiException):
    pass

class LsApiException(StockApiException):
    pass

class InvalidResponseException(StockApiException):
    pass

class KisApiException(StockApiException):
    pass