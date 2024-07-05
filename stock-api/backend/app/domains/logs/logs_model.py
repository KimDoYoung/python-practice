from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field

class LogsRequest(BaseModel):
    at_time: datetime = Field(default_factory=datetime.now)
    user_id: Optional[str] = None
    stk_abbr: Optional[str] = None
    acct_no: Optional[bool] = False
    message: str

class Logs(Document):
    at_time: datetime = Field(default_factory=datetime.now)
    user_id: Optional[str] = None
    stk_abbr: Optional[str] = None
    acct_no: Optional[bool] = False
    message: str

    class Settings:
        name = "Logs"