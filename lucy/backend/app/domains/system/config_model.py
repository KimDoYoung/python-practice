from typing import Literal, Optional
from beanie import Document, Indexed
from pydantic import BaseModel, Field

class DbConfigRequest(BaseModel):
    mode:str
    key: str
    value: str
    note:str

class DbConfig(Document):
    mode: Literal['System', 'User'] = Field(default="User", description="System or User")
    key: str = Field(default=None, unique=True, description="Unique key for the config")
    value: str
    note: Optional[str] = None

    class Settings:
            name = "Config"