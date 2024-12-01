from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# 요청 데이터 스키마
class MovieReviewRequest(BaseModel):
    title: str
    nara: Optional[str] = None
    year: Optional[str] = None
    lvl: Optional[int] = None
    ymd: Optional[str] = None
    content: Optional[str] = None
    lastmodify_dt: Optional[datetime] = None

# 응답 데이터 스키마
class MovieReviewResponse(MovieReviewRequest):
    id: int

    class Config:
        orm_mode = True
