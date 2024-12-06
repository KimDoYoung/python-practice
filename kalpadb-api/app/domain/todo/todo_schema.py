from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class TodoCreateRequest(BaseModel):
    todos: List[str]
    
# 요청 데이터 스키마
class TodoRequest(BaseModel):
    content: str
    done_yn: Optional[str] = "N"

# 응답 데이터 스키마
class TodoResponse(TodoRequest):
    id: int
    input_dt: datetime
    done_dt: Optional[datetime] = None
