from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator

class FBFileResponse(BaseModel):
    file_id: int
    org_name: str
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


# 키보드 데이터를 생성하기 위한 스키마
class KeyboardCreateRequest(BaseModel):
    product_name: Optional[str] = None
    manufacturer: str
    purchase_date: str # 이제 이 필드는 문자열이며 YYYYMMDD 형식을 기대합니다.
    purchase_amount: int
    key_type: str
    switch_type: str
    actuation_force: str
    interface_type: str
    overall_rating: int
    typing_feeling: Optional[str] = None

    @validator('purchase_date')
    def validate_purchase_date(cls, v):
        try:
            datetime.strptime(v, "%Y%m%d")
        except ValueError:
            raise ValueError("purchase_date must be in YYYYMMDD format")
        return v

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
    delete_file_ids: Optional[List[int]] = None  # 삭제할 이미지 ID 배열

# 데이터베이스에서 읽어온 키보드 데이터를 응답으로 전송하기 위한 스키마
# 모든 필드가 포함됨
class KeyboardRequest(BaseModel):
    id: Optional[int] = None
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

class KeyboardResponse(KeyboardRequest):
    files: List[FBFileResponse] = []

class Config:
    orm_mode = True
