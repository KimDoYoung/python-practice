
from pydantic import BaseModel, Field
from typing import Optional

# 요청 시 사용하는 모델 (요청에 app_key와 app_secret_key는 포함되지 않음)
class CompanyRequest(BaseModel):
    company_id: int
    service_nm: str = Field(..., max_length=100)
    start_ymd: str = Field(..., max_length=8)  # YYYYMMDD 형태로 받기
    end_ymd: Optional[str] = Field(default='99991231', max_length=8)

# 응답 시 사용하는 모델 (app_key와 app_secret_key 포함)
class CompanyResponse(CompanyRequest):
    app_key: Optional[str] = Field(None, max_length=64)
    app_secret_key: Optional[str] = Field(None, max_length=64)