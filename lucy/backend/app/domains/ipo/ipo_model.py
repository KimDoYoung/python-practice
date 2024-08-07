from datetime import datetime
from typing import List, Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel


class Underwriter(BaseModel):
    주간사: str
    청약한도: Optional[int] = 0

class CompetitionRate(BaseModel):
    균등: Optional[float] = None
    비례: Optional[float] = None

class Offering(BaseModel):
    총공모주식수: int
    액면가: int
    확정공모가: Optional[float] = None
    주간사_리스트: List[Underwriter]
    경쟁율: CompetitionRate

class Days(BaseModel):
    청약일: str
    납입일: str
    환불일: str
    상장일: Optional[str] = None

class IpoDays(BaseModel):
    company: str
    name: str
    ymd: str
    title: str
    scrap_url: Optional[str] = None

class EvalData(BaseModel):
    확정공모가 : Optional[int] = None
    매출액 : Optional[float] = None
    기관경쟁률: Optional[float] = None
    의무보유확약 : Optional[float] = None
    순이익 : Optional[float] = None
    액면가 : Optional[float] = None

class Ipo(Document):
    stk_name: str
    days: Days
    name: str
    category: Optional[str] = None
    offering: Offering
    processed_time: datetime
    scrap_id: PydanticObjectId
    title: str
    scrap_url : Optional[str] = None
    hp_url : Optional[str] = None #홈페이지 url
    eval_data: EvalData
    expect_cost: Optional[int] = None # 예상 공모가
    class Settings:
        collection = "Ipo"