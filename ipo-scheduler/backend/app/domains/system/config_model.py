from typing import Literal, Optional
from beanie import Document
from pydantic import BaseModel, Field

class DbConfigRequest(BaseModel):
    mode:str
    key: str
    value: str
    note:str
    editable:Optional[bool] = False

class DbConfig(Document):
    mode: Literal['System', 'User'] = Field(default="System", description="System or User")
    key: str = Field(default=None, unique=True, description="Unique key for the config")
    value: str
    note: Optional[str] = None
    editable:Optional[bool] = False

    class Settings:
            name = "Config"