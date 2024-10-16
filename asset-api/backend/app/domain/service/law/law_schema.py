from pydantic import  BaseModel, Field

from backend.app.domain.ifi.ifi10.ifi10_law_schema import Ifi10LawResponse
from backend.app.domain.service.base_schema import ServiceBase



class Law010_Request(BaseModel):
    conti_limit: int = Field(10, ge=1, le=1000, description="연속 조회 LIMIT (기본값: 10, 최소: 1, 최대: 1000)")
    conti_start_idx: int = Field(0, ge=0, description="연속 조회 START INDEX (기본값: 0)")
    conti_yn: str = Field("N", description="연속 조회 여부 (기본값: N, Y/N)")

    class Config:
        schema_extra = {
            "example": {
                "conti_limit": 10,
                "conti_start_idx": 0,
                "conti_yn": "Y"
            }
        }

class Law010_Response(ServiceBase):
    output : list[Ifi10LawResponse] = Field([], description="법령조문 목록")