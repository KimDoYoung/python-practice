from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    kind: Optional[str] = None

class UserResponse(BaseModel):
    user_id: str
    user_name: str
    email: EmailStr
    kind: str
    created_at: str

class UserInfo(BaseModel):
    key_name: str
    key_value: str
    use_yn: Optional[str] = 'Y'
    issuer: Optional[str] = None
    note: Optional[str] = None
