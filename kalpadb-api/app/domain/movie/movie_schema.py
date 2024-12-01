from typing import Optional
from pydantic import BaseModel

# 요청 데이터 스키마
class MovieRequest(BaseModel):
    mid: Optional[str] = None
    gubun: str
    title1: str
    title2: Optional[str] = None
    title3: Optional[str] = None
    category: Optional[str] = None
    gamdok: Optional[str] = None
    make_year: Optional[str] = None
    nara: Optional[str] = None
    dvd_id: Optional[str] = None
    title1num: Optional[str] = None
    title1title2: Optional[str] = None

# 응답 데이터 스키마
class MovieResponse(MovieRequest):
    id: int

    class Config:
        orm_mode = True
