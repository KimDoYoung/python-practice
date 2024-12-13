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

class MovieReviewUpsertRequest(BaseModel):
    id : Optional[int] = None
    title: str
    nara: Optional[str] = None
    year: Optional[str] = None
    lvl: Optional[int] = None
    ymd: Optional[str] = None
    content: Optional[str] = None


# 응답 데이터 스키마
class MovieReviewResponse(MovieReviewRequest):
    id: int

    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }


class MovieReviewListResponse(BaseModel):
    list: list[MovieReviewResponse]
    item_count : int
    next_data_exists: bool
    start_index: int
    next_index: int

class MovieReviewSearchRequest(BaseModel):
    search_text: Optional[str] = None
    nara: Optional[str] = None
    year: Optional[str] = None
    lvl: Optional[str] = None
    start_ymd: Optional[str] = None
    end_ymd: Optional[str] = None
    start_index: int = 0
    limit: int  = 10
    include_content: bool = False
