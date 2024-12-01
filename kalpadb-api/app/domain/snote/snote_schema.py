from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# 요청 데이터 스키마
class SNoteRequest(BaseModel):
    hint: Optional[str] = None
    note: Optional[str] = None

# 응답 데이터 스키마
class SNoteResponse(SNoteRequest):
    id: int
    create_dt: datetime

    class Config:
        orm_mode = True
