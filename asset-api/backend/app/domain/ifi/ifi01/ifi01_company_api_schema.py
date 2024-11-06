from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class Ifi01CompanyApiBase(BaseModel):
    ifi01_company_id: int
    sys01_company_nm: Optional[str] = None
    ifi01_service_cd: str
    ifi01_service_nm: Optional[str] = None
    ifi01_start_date: Optional[date] = None
    ifi01_close_date: Optional[date] = None
    ifi01_app_key: Optional[str] = None

class Ifi01CompanyApiCreate(Ifi01CompanyApiBase):
    pass

class Ifi01CompanyApiResponse(Ifi01CompanyApiBase):
    ifi01_company_api_id: Optional[int]
    ifi01_created_date: Optional[datetime] = None
    ifi01_update_date: Optional[datetime] = None
    ifi01_app_secret_key: Optional[str] = None

    class Config:
        orm_mode = True  # 반드시 orm_mode를 활성화해야 함
        from_attributes = True  # from_orm 사용을 위한 설정 추가