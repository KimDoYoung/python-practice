from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional

class UserAdditionalAttribute(BaseModel):
    key_name: str
    key_value: str
    use_yn: str = 'Y'
    issuer: Optional[str] = None
    note: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class User(Document):
    user_id: str = Field(unique=True)
    user_name: str
    email: EmailStr = Field(unique=True)
    password: str
    kind: str = 'P'
    created_at: datetime = Field(default_factory=datetime.utcnow)
    additional_attributes: List[UserAdditionalAttribute] = []

    class Settings:
        name = "users"  # MongoDB에서 사용할 컬렉션 이름
