class KisException(Exception):
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

