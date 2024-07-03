from abc import ABC, abstractmethod

from backend.app.domains.stc.kis.model.kis_order_cash_model import OrderCashRequest, OrderCashResponse

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

    @abstractmethod  # 추상 메서드로 선언
    def order_cash(self, order_cash_request: OrderCashRequest)-> OrderCashResponse:
        pass  # 하위 클래스에서 반드시 구현해야 함
