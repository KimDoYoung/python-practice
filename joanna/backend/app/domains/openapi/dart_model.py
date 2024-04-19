from sqlmodel import SQLModel, Field
from typing import Optional


class DartCorpCode(SQLModel, table=True, schema="stock"):
    __tablename__ = "dart_corp_code"
    corp_code: str = Field(primary_key=True, max_length=8)
    corp_name: str = Field(max_length=200, nullable=False)
    stock_code: Optional[str] = Field(default=None, max_length=50, nullable=True)
    modify_date: Optional[str] = Field(default=None, max_length=8, nullable=True)
