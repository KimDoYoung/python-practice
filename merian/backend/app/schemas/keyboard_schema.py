from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# 키보드 데이터를 생성하기 위한 스키마
class KeyboardCreateRequest(BaseModel):
    product_name: str
    manufacturer: str
    purchase_date: str
    purchase_amount: int
    key_type: str
    switch_type: str
    actuation_force: str
    interface_type: str
    overall_rating: int
    typing_feeling: Optional[str] = None

# 키보드 데이터를 업데이트하기 위한 스키마
# 일부 필드는 업데이트 시 선택적일 수 있음
class KeyboardUpdateRequest(BaseModel):
    product_name: Optional[str] = None
    manufacturer: Optional[str] = None
    purchase_date: Optional[str] = None
    purchase_amount: Optional[int] = None
    key_type: Optional[str] = None
    switch_type: Optional[str] = None
    actuation_force: Optional[str] = None
    interface_type: Optional[str] = None
    overall_rating: Optional[int] = None
    typing_feeling: Optional[str] = None

# 데이터베이스에서 읽어온 키보드 데이터를 응답으로 전송하기 위한 스키마
# 모든 필드가 포함됨
class KeyboardRequest(BaseModel):
    id: int
    product_name: str
    manufacturer: str
    purchase_date: str
    purchase_amount: int
    key_type: str
    switch_type: str
    actuation_force: str
    interface_type: str
    overall_rating: int
    typing_feeling: Optional[str] = None
    create_on: datetime
    create_by: Optional[str] = None

    class Config:
        from_attributes = True
