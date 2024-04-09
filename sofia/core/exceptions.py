class SofiaError(Exception):
    """Joannan 애플리케이션에서 발생하는 기본 예외"""
    pass

class RestfulError(SofiaError):
    """Restful API에서 발생하는 예외"""
    pass

class FolderNotFoundError(RestfulError):
    """폴더가 존재하지 않을 때 발생하는 예외"""
    def __init__(self, message="폴더가 존재하지 않습니다."):
        self.message = message
        super().__init__(self.message)