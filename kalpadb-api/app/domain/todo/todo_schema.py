from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# 요청 데이터 스키마
class TodoRequest(BaseModel):
    content: str
    done_yn: Optional[str] = "N"

# 응답 데이터 스키마
class TodoResponse(TodoRequest):
    id: int
    input_dt: datetime
    done_dt: Optional[datetime] = None

    class Config:
        orm_mode = True
