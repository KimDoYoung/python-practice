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
    
    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }

# 응답 데이터 스키마
class MovieResponse(MovieRequest):
    id: int

    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }

class MovieListResponse(BaseModel):
    list: list[MovieResponse]
    item_count : int
    next_data_exists: bool
    start_index: int
    next_index: int

class MovieSearchRequest(BaseModel):
    gubun: Optional[str] = None
    search_text: Optional[str] = None
    nara: Optional[str] = None
    category: Optional[str] = None
    gamdok: Optional[str] = None
    make_year: Optional[str] = None
    start_index: int = 0
    limit: int  = 10