# ipo_data_model.py
"""
모듈 설명: 
    - 예상체결가를 정하는 수식을 만들기 위한 데이터 모델
주요 기능:
    

작성자: 김도영
작성일: 2024-07-22
버전: 1.0
"""
from beanie import Document
from bson import ObjectId
from pydantic import Field


class IpoHistory(Document):
    Company: str  # 회사명
    StkCode: str  # 종목코드
    FinalOfferingPrice: int  # 확정공모가
    Revenue: int  # 매출액
    InstitutionalSubscriptionRatio: float  # 기관경쟁률
    LockupAgreement: float  # 의무보유확약
    NetIncome: float  # 순이익
    MaxValue: int  # 최고체결가
    MultipleVariable: float = Field(default=0.0)  # 곱하기변수
    Notes: str  # 비고

    def calculate_multiple_variable(self):
        if self.FinalOfferingPrice != 0:
            self.MultipleVariable = self.MaxValue / self.FinalOfferingPrice
        else:
            self.MultipleVariable = 2

    async def save(self, *args, **kwargs):
        self.calculate_multiple_variable()
        await super().save(*args, **kwargs)
    
    class Settings:
        collection = "Ipo_History"
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}