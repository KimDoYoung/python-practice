from typing import Optional
from pydantic import BaseModel

class Header(BaseModel):
    approval_key: str
    personalseckey: str
    custtype: Optional[str] = "P"
    tr_type: str
    content_type: Optional[str] = "utf-8"

class Input(BaseModel):
    tr_id: str
    tr_key: str

class Body(BaseModel):
    input: Input

class KisWsRequest(BaseModel):
    header: Header
    body: Body    