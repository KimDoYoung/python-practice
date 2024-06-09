from backend.app.core.exception.lucy_exception import LucyException


class KisException(LucyException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class KisAccessTokenExpireException(KisException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class KisAccessTokenInvalidException(KisException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

