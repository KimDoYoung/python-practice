from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

from backend.app.domains.base_sql_model import BaseSQLModel

class User(BaseSQLModel, table=True, schema="public"):
    __tablename__ = "users"
    __table_args__ = {'schema': 'public'}
    user_id: str = Field(primary_key=True, max_length=30)
    user_name: str = Field(max_length=50, nullable=False)
    email: str = Field(max_length=100, nullable=False)
    password: str = Field(max_length=100, nullable=False)
    kind: str = Field(default='P', max_length=1, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
