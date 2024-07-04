class StockApiException(Exception):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(self.detail)

class KisAccessTokenExpireException(StockApiException):
    pass

class KisAccessTokenInvalidException(StockApiException):
    pass
