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
from typing import List, Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, field_validator, validator


class MyStockBase(BaseModel):
    stk_code: str
    stk_name: Optional[str] = None
    stk_types: Optional[List[str]] = None

    @field_validator('stk_code')
    def validate_stk_code(cls, v):
        if not v.isdigit() or len(v) != 6:
            raise ValueError('stk_code must be a string of 6 digits')
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
