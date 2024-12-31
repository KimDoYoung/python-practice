from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# 요청 데이터 스키마
class EssayRequest(BaseModel):
    title: str
    content: Optional[str] = None

# 응답 데이터 스키마
class EssayResponse(EssayRequest):
    id: int
    create_dt: datetime
    lastmodify_dt: Optional[datetime] = None

    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }
class EssayUpsertRequest(BaseModel):
    id: Optional[int] = None
    title: str
    content: Optional[str] = None

class EssayListRequest(BaseModel):
    ''' 에세이 리스트 조회 요청 '''
    search_text: Optional[str] = None
    start_index: int = 0
    limit: int = 10
    title_only: Optional[bool] = False

class EssayListResponse(BaseModel):
    ''' 에세이 리스트 조회 응답 '''
    list: List[EssayResponse]
    exists_next: bool
    last_index: int
    data_count: int
    page_size : int
    start_index: int
