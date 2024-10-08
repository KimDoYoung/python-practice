# mystock_model.py
"""
모듈 설명: 
    -   사용자가 관심있는 주식을 저장하는 모델
주요 기능:
    -   stk_type은 보유,관심,공모주로 구분

작성자: 김도영
작성일: 07
버전: 1.0
"""
import datetime
from typing import List, Optional
from beanie import Document
from pydantic import BaseModel, Field, field_validator

class MyStockBase(BaseModel):
    stk_code: str
    stk_name: Optional[str] = None
    sell_base_price: Optional[int] = None # 매도기준가격
    buy_base_price: Optional[int] = None # 매수기준가격
#------------------------------------------------- 단타머신에서 사용    
    buy_ordno : Optional[str] = '' # 매수주문번호
    buy_qty : Optional[int] = 0 # 매수수량
    buy_price: Optional[int] = 0 # 매수가격
    buy_time : Optional[str] = '' # 매수시간
    sell_ordno: Optional[str] = '' # 매도주문번호
    sell_qty : Optional[int] = 0 # 매도수량
    sell_price: Optional[int] = 0  # 매도가격
    sell_time: Optional[str] = '' # 매도시간    
    
    stk_company: Optional[str] = None # 증권사
    
    stk_types: Optional[List[str]] = None
    last_update_time: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now)
    @field_validator('stk_code')

    def validate_stk_code(cls, v):
        if len(v) != 6:
            raise ValueError('종목코드는 6개의 숫자입니다.')
        return v

    @field_validator('stk_types', mode='before')
    def ensure_unique_stk_type(cls, v):
        if v is None:
            return []
        return list(set(v))

class MyStockDto(MyStockBase):
    pass

class MyStock(Document, MyStockBase):
    # @field_validator('stk_types', mode='before')
    # def ensure_unique_stk_type(cls, v):
    #     if v is None:
    #         return []
    #     return list(set(v))

    class Settings:
        collection = "MyStock"
