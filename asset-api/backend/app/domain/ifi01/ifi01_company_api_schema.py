from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class Ifi01CompanyApiBase(BaseModel):
    ifi01_company_id: int
    ifi01_config_api_id: int
    ifi01_start_date: Optional[date] = None
    ifi01_close_date: Optional[date] = None
    ifi01_app_key: Optional[str] = None

class Ifi01CompanyApiCreate(Ifi01CompanyApiBase):
    pass

class Ifi01CompanyApiResponse(Ifi01CompanyApiBase):
    ifi01_company_api_id: int
    ifi01_created_date: Optional[datetime] = None

    class Config:
        model_config = {
            'from_attributes': True  # ORM 모드 활성화
        }
