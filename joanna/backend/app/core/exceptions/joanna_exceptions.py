class JoannaError(Exception):
    """Joannan 애플리케이션에서 발생하는 기본 예외"""
    pass

class RestfulError(JoannaError):
    """Restful API에서 발생하는 예외"""
    pass

class KoreaInvestmentError(RestfulError):
    """한국투자증권 API에서 발생하는 예외"""
    def __init__(self, message="한국투자증권 API에서 에러가 발생했습니다."):
        self.message = message
        super().__init__(self.message)