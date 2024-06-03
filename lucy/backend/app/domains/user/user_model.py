from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from typing import List, Optional

class LoginFormData(BaseModel):
    username: str
    email:Optional[str] = None
    password: Optional[str] = None

class AccessToken(LoginFormData):
    access_token: str
    token_type: str

class UserAdditionalAttribute(BaseModel):
    key_name: str
    key_value: str
    use_yn: str = 'Y'
    issuer: Optional[str] = None
    note: Optional[str] = None
    created_at: datetime =  Field(default_factory=lambda: datetime.now(timezone.utc))

class UserRequest(BaseModel):
    user_id: str
    user_name: str
    email: EmailStr
    password: str
    kind: str = 'P'
    additional_attributes: List[UserAdditionalAttribute] = []

class User(Document):
    user_id: str = Field(json_schema_extra={"unique": True})
    user_name: str
    email: EmailStr = Field(json_schema_extra={"unique": True})
    password: str
    kind: str = 'P'
    created_at: datetime =  Field(default_factory=lambda: datetime.now(timezone.utc))
    additional_attributes: List[UserAdditionalAttribute] = []

    class Settings:
        name = "Users"