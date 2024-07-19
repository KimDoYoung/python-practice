# stock_api.py
"""
모듈 설명: 
    - 주식회사 API를 사용하기 위한 추상 클래스
    - kis_stock_api (KisStockApi)와 ls_stock_api (LsStockApi)가 상속받는다.
주요 기능:
    - user_id, acctno를 가지고, user_service를 가지고 있다.
작성자: 김도영
작성일: 2024-07-08
버전: 1.0
"""
from abc import ABC, abstractmethod
from datetime import datetime

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
    def get_access_token_time(self)->datetime:
        pass  # token 발급시간 반환 