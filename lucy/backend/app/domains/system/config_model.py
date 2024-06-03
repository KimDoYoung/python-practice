from typing import Optional
from beanie import Document, Indexed
from pydantic import BaseModel, Field

class DbConfigRequest(BaseModel):
    mode:str
    key: str
    value: str
    note:str

class DbConfig(Document):
    mode: str = Field(default="System", description="System or User")
    key: str = Indexed(unique=True, description="Unique key for the config")
    value: str
    note : Optional[str] = None

    class Settings:
            name = "Config"