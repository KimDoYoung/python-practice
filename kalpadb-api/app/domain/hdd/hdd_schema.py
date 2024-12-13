from typing import List, Optional
from pydantic import BaseModel
import pydantic

class GroupItemResponse(BaseModel):
    title: str
    count: int

class HDDChildRequest(BaseModel):
    volumn_name: str
    pid: int
    gubun: str

    @pydantic.field_validator('gubun')
    def validate_gubun(cls, v):
        if v not in {'A', 'D', 'F'}:
            raise ValueError('gubun must be one of A, D, F')
        return v

# 요청 데이터 스키마
class HDDRequest(BaseModel):
    id: int
    volumn_name: Optional[str] = None
    gubun: str
    path: Optional[str] = None
    file_name: Optional[str] = None
    name: str
    pdir: Optional[str] = None
    extension: Optional[str] = None
    size: Optional[float] = None
    sha1_cd: Optional[str] = None
    srch_key: Optional[str] = None
    last_modified_ymd: Optional[str] = None
    pid: Optional[int] = None
    right_pid: Optional[int] = None

# 응답 데이터 스키마
class HDDResponse(HDDRequest):
    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }

class HDDSearchRequest(BaseModel):
    search_text: Optional[str] = None
    volumn_name: Optional[str] = None
    gubun: Optional[str] = 'A'
    start_index: int = 0
    limit: int = 10

    @pydantic.field_validator('gubun')
    def validate_gubun(cls, v):
        if v not in {'A', 'D', 'F'}:
            raise ValueError('gubun must be one of A, D, F')
        return v

class HDDSearchResponse(BaseModel):
    list: List[HDDResponse]
    data_count: int
    next_data_exists: bool
    start_index:int
    last_index: int
    limit: int


    

