import math
from typing import List, Optional, Union
from pydantic import BaseModel, Field, validator


class QueryCondition(BaseModel):
    테마목록: Optional[List[str]] = Field(None, description="검색할 테마 목록") 
    시장종류: Optional[str] = Field(None, description="시장 종류")
    시가총액: Optional[int] = Field(None, description="시가 총액")
    현재가: Optional[Union[int, List[int]]] = Field(None, description="현재가 범위 또는 특정 값")


class JudalStock(BaseModel):
    종목명: str
    종목코드: str
    현재가: int
    시가총액: int
    시장종류: str
    관련테마: Optional[str] = Field(None, alias="관련테마")
    전일비: float
    삼일합산: Optional[float] = Field(None, alias="3일합산")
    소외지수_52주: Optional[int] = Field(None, alias="52주 소외지수")
    소외지수_3년: Optional[int] = Field(None, alias="3년 소외지수")
    주가지수_3년: Optional[int] = Field(None, alias="3년 주가지수")
    기대수익률: Optional[float] = None
    PBR: Optional[float] = None
    PER: Optional[float] = None
    EPS: Optional[int] = None
    거래량지수_당일: Optional[float] = Field(None, alias="당일 거래량지수")
    거래량지수_최근7일: Optional[float] = Field(None, alias="최근7일 거래량지수")
    등락가: Optional[int] = None
    최고_52주: Optional[int] = Field(None, alias="52주최고")
    최저_52주: Optional[int] = Field(None, alias="52주최저")
    변동률최저_52주: Optional[float] = Field(None, alias="52주변동률최저")
    변동률최고_52주: Optional[float] = Field(None, alias="52주변동률최고")
    최고_3년: Optional[int] = Field(None, alias="3년최고")
    최저_3년: Optional[int] = Field(None, alias="3년최저")
    변동률최저_3년: Optional[float] = Field(None, alias="3년변동률최저")
    변동률최고_3년: Optional[float] = Field(None, alias="3년변동률최고")

    class Config:
        allow_population_by_field_name = True
    
class JudalTheme(BaseModel):
    name:str
    href:str

class JudalCsvData(BaseModel):
    종목명: str
    전일비: float
    삼일합산: Optional[float] = Field(None, alias="3일합산")
    소외지수_52주: Optional[int] = Field(None, alias="52주 소외지수")
    소외지수_3년: Optional[int] = Field(None, alias="3년 소외지수")
    주가지수_3년: Optional[int] = Field(None, alias="3년 주가지수")
    기대수익률: Optional[float] = None
    PBR: Optional[float] = None
    PER: Optional[float] = None
    EPS: Optional[int] = None
    시가총액: Optional[int] = None
    거래량지수_당일: Optional[float] = Field(None, alias="당일 거래량지수")
    거래량지수_최근7일: Optional[float] = Field(None, alias="최근7일 거래량지수")
    버핏초이스: Optional[int] = None
    관련테마: Optional[str] = None
    업데이트: Optional[str] = None
    시장종류: Optional[str] = None
    종목코드: Optional[str] = None  # 문자열로 처리
    현재가: Optional[int] = None
    등락가: Optional[int] = None
    최고_52주: Optional[int] = Field(None, alias="52주최고")
    최저_52주: Optional[int] = Field(None, alias="52주최저")
    변동률최저_52주: Optional[float] = Field(None, alias="52주변동률최저")
    변동률최고_52주: Optional[float] = Field(None, alias="52주변동률최고")
    최고_3년: Optional[int] = Field(None, alias="3년최고")
    최저_3년: Optional[int] = Field(None, alias="3년최저")
    변동률최저_3년: Optional[float] = Field(None, alias="3년변동률최저")
    변동률최고_3년: Optional[float] = Field(None, alias="3년변동률최고")
    
    @validator('업데이트', pre=True, always=True)
    def validate_update(cls, v):
        if isinstance(v, float) and math.isnan(v):
            return None
        return v

    class Config:
        allow_population_by_field_name = True