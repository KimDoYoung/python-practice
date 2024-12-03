from typing import Optional
from pydantic import BaseModel

class GroupItemResponse(BaseModel):
    title: str
    count: int

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
