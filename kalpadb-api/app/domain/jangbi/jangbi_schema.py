from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class JangbiRequest(BaseModel):
    ymd: str = Field(..., max_length=8, description="구입일")
    item: str = Field(..., max_length=100, description="품목")
    location: Optional[str] = Field(None, max_length=200, description="위치")
    cost: Optional[int] = Field(None, description="가격")
    spec: Optional[str] = Field(None, description="스펙(특징)")
    lvl: str = Field(default="2", max_length=1, description="등급")

class JangbiResponse(BaseModel):
    id: int
    ymd: str
    item: str
    location: Optional[str]
    cost: Optional[int]
    spec: Optional[str]
    lvl: str
    modify_dt: datetime

    class Config:
        orm_mode = True
