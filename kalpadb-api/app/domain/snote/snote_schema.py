from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class SnoteCreateRequest(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    note: str
    
# 요청 데이터 스키마
class SNoteRequest(BaseModel):
    title: Optional[str] = None
    note: Optional[str] = None

# 응답 데이터 스키마
class SNoteResponse(SNoteRequest):
    id: int
    create_dt: datetime

    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }

class SnoteListRequest(BaseModel):
    search_text: Optional[str] = None  
    start_index: int = 0
    limit: int = 10
    
class SnoteListResponse(BaseModel):
    snote_list: list[SNoteResponse]
    next_exist: bool
    limit: int
    start_index: int
    last_index: int
    
        
class SnoteHintResponse(BaseModel):
    hint: str
    password: str
    model_config = {
        'from_attributes': True
    }