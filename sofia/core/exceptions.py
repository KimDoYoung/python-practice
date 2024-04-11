class SofiaError(Exception):
    """Sofia 애플리케이션에서 발생하는 기본 예외"""
    pass

class RestfulError(SofiaError):
    """Restful API에서 발생하는 예외"""
    def __init__(self, detail: str = None):
        self.detail = detail or "Restful API에서 오류가 발생했습니다."
        super().__init__(self.detail)

class FolderNotFoundError(RestfulError):
    """폴더가 존재하지 않을 때 발생하는 예외"""
    def __init__(self, detail: str = "폴더가 존재하지 않습니다."):
        super().__init__(detail)
