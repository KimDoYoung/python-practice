from typing import Optional
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

    class Config:
        orm_mode = True
