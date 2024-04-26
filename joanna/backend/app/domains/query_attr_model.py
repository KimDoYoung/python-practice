from sqlmodel import SQLModel
from typing import Optional

from backend.app.domains.base_sql_model import BaseSQLModel

class QueryAttr(BaseSQLModel):
    searchText: Optional[str] = None
    limit: int = 10
    skip: int = 0
    next: bool = False 