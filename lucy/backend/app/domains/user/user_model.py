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

class KeyValueData(BaseModel):
    key: str
    value: str
    use_yn: str = 'Y'
    issuer: Optional[str] = None
    note: Optional[str] = None
    created_at: datetime =  Field(default_factory=lambda: datetime.now(timezone.utc))

class StkAccount(BaseModel):
    abbr: str
    account_no: str
    account_pw: str
    hts_id: Optional[str] = None
    key_values: List[KeyValueData] = []
    created_at: datetime =  Field(default_factory=lambda: datetime.now(timezone.utc))

#TODO upsert addtion을 빼는 것이 좋지 않을까?
class User(Document):
    user_id: str = Field(json_schema_extra={"unique": True})
    user_name: str
    email: EmailStr = Field(json_schema_extra={"unique": True})
    password: str
    kind: str = 'P'
    created_at: datetime =  Field(default_factory=lambda: datetime.now(timezone.utc))
    key_values: List[KeyValueData] = []
    accounts: List[StkAccount] = []

    def to_dict(self):
        kv = [kv.model_dump() for kv in self.key_values]
        return {
            "user_id" : self.user_id,
            "user_name" : self.user_name,
            "email" : self.email,
            "kind" : self.kind,
            "key_values" : kv
        }
    
    def get_value_by_key(self, key: str) -> Optional[str]:
        for kv in self.key_values:
            if kv.key == key:
                return kv.value
        return None
    
    def set_value_by_key(self, key: str, value: str):
        for kv in self.key_values:
            if kv.key == key:
                kv.value = value
                return
        self.key_values.append(KeyValueData(key=key, value=value))

    class Settings:
        name = "Users"