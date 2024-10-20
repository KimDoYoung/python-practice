class IPOSchedulerException(Exception):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(self.detail)

class KisException(IPOSchedulerException):
    pass

class KisApiException(IPOSchedulerException):
    pass


class LsException(IPOSchedulerException):
    pass

class AccessTokenExpireException(KisException):
    pass

class AccessTokenInvalidException(KisException):
    pass

class LsApiException(LsException):
    pass

class InvalidResponseException(IPOSchedulerException):
    pass


class JudalException(IPOSchedulerException):
    pass