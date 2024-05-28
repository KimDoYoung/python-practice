from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field

class ConfigData(BaseModel):
    key: str
    value: str

class DbConfig(Document):
    key: str = Field(unique=True)
    value: str

    class Settings:
        collection = "Config"  # MongoDB에서 사용할 컬렉션 이름
