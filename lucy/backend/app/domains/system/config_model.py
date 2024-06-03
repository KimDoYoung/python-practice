from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field

class ConfigData(BaseModel):
    mode:str
    key: str
    value: str
    note:str

class DbConfig(Document):
    mode:str = Field("System") # System, User
    key: str = Field(unique=True)
    value: str
    note : Optional[str] = None

    class Settings:
        collection = "Config"  # MongoDB에서 사용할 컬렉션 이름
