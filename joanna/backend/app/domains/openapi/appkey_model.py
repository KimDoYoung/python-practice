from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

from backend.app.domains.user.user_model import User

class AppKey(SQLModel, table=True, schema="public"):
    user_id: str = Field(foreign_key="users.user_id", max_length=30, nullable=False)
    key_name: str = Field(primary_key=True, max_length=30)
    key_value: str = Field(max_length=200, nullable=False)
    user_yn: str = Field(default='Y', max_length=1, nullable=False)
    issuer: Optional[str] = Field(default=None, max_length=100, nullable=True)
    note: Optional[str] = Field(default=None, max_length=500, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    user: User = Relationship(back_populates="appkeys")
