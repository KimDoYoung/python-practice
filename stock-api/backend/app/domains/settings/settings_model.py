from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field

class SettingsRequest(BaseModel):
    key: str
    value: str
    note:str
    editable:Optional[bool] = False

class Settings(Document):
    key: str = Field(default=None, unique=True, description="Unique key for the settings")
    value: str
    note: Optional[str] = None
    editable:Optional[bool] = False

    class Settings:
        name = "Settings"