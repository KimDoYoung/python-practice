from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.domain.filenode.filenode_schema import AttachFileInfo

class JangbiUpsertRequest(BaseModel):
    id : Optional[int] = None
    ymd: str
    item: str
    location: Optional[str] = None
    cost: Optional[int] = None
    spec: Optional[str] = None
    lvl: Optional[str] = '2'

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
    attachments : Optional[list[AttachFileInfo]] = None

    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }

class JangbiListParam(BaseModel):
    start_ymd: str = '19700101'
    end_ymd: str = '99991231'
    search_text : str | None = None
    lvl : str | None = None
    order_direction : str = 'desc'
    start_idx : int = 0
    limit : int = 10

class JangbiListResponse(BaseModel):
    list: list[JangbiResponse]
    item_count : int
    next_data_exists: bool
    next_index: int
    start_index: int
