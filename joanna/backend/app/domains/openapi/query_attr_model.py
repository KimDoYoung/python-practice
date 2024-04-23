from sqlmodel import SQLModel
from typing import Optional

class QueryAttr(SQLModel):
    searchText: Optional[str] = None
    limit: int = 10
    skip: int = 0
    next: bool = False 