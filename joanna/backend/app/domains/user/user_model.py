from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

#from backend.app.domains.openapi.appkey_model import AppKey

class User(SQLModel, table=True, schema="public"):
    __tablename__ = "users"
    user_id: str = Field(primary_key=True, max_length=30)
    user_name: str = Field(max_length=50, nullable=False)
    email: str = Field(max_length=100, nullable=False)
    password: str = Field(max_length=100, nullable=False)
    kind: str = Field(default='P', max_length=1, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

#    appkeys: list["AppKey"] = Relationship(back_populates="user")
