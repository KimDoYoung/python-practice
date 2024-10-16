from pydantic import BaseModel
from typing import Optional

class ServiceBase(BaseModel):
    msg_cd: str  # 응답코드
    msg: str  # 응답메세지
    count: Optional[int] = 0  # 조회건수 (기본값 0)
    exists_yn: Optional[str] = "N"  # 추가데이터 존재여부
    conti_last_idx: Optional[int] = None  # 연속 조회 LAST INDEX

    class Config:
        schema_extra = {
            "example": {
                "msg_cd": "0000",
                "msg": "Success",
                "count": 100,
                "conti_yn": "Y",
                "conti_last_idx": 99
            }
        }
