from sqlmodel import SQLModel, Field
from typing import Optional

from backend.app.domains.base_sql_model import BaseSQLModel


class DartCorpCode(BaseSQLModel, table=True, schema="stock"):
    __tablename__ = "dart_corp_code"
    __table_args__ = {'schema': 'stock'}
    corp_code: str = Field(primary_key=True, max_length=8)
    corp_name: str = Field(max_length=200, nullable=False)
    stock_code: Optional[str] = Field(default=None, max_length=50, nullable=True)
    modify_date: Optional[str] = Field(default=None, max_length=8, nullable=True)
