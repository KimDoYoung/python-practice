from typing import List, Optional, Union
from pydantic import BaseModel, Field


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
    관련테마: Optional[str]  # 관련테마는 없을 수도 있으므로 Optional로 설정
    
class JudalTheme(BaseModel):
    name:str
    href:str

class JudalCsvData(BaseModel):
    종목명: str
    전일비: str
    삼일합산: Optional[str] = None
    _52주_소외지수: Optional[int] = None
    _3년_소외지수: Optional[int] = None
    _3년_주가지수: Optional[int] = None
    기대수익률: Optional[float] = None
    PBR: Optional[float] = None
    PER: Optional[float] = None
    EPS: Optional[int] = None
    시가총액: Optional[int] = None
    당일_거래량지수: Optional[str] = None
    최근7일_거래량지수: Optional[str] = None
    버핏초이스: Optional[int] = None
    관련테마: Optional[str] = None
    업데이트: Optional[str] = None
    시장종류: Optional[str] = None
    종목코드: Optional[str] = None  # 문자열로 처리
    현재가: Optional[int] = None
    등락가: Optional[int] = None
    _52주_최고: Optional[int] = None
    _52주_최저: Optional[int] = None
    _52주_변동률_최저: Optional[float] = None
    _52주_변동률_최고: Optional[float] = None
    _3년_최고: Optional[int] = None
    _3년_최저: Optional[int] = None
    _3년_변동률_최저: Optional[float] = None
    _3년_변동률_최고: Optional[float] = None
