from abc import ABC, abstractmethod

class StockApi(ABC):
    def __init__(self, user_id, acctno):
        self.user_id = user_id
        self.acctno = acctno
        self.user_service = None
    
    def set_user_service(self, user_service):
        self.user_service = user_service


    @abstractmethod  # 추상 메서드로 선언
    async def initialize(self)-> bool:
        pass  # stock company api 연결가능여부 확인

