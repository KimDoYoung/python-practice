# schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class Ifi05JobScheduleBase(BaseModel):
    ifi05_job_schedule_nm: Optional[str] = Field(None, description="스케줄명")
    ifi05_run_type: Optional[str] = Field(None, description="구분 (예: cron)")
    ifi05_args:Optional[str] = Field(None, description="argument")
    ifi05_cron_str: Optional[str] = Field(None, description="cron 표현식")
    ifi05_description: Optional[str] = Field(None, description="설명")
    ifi05_note: Optional[str] = Field(None, description="비고")

    class Config:
        from_attributes = True  # from_orm 사용을 위한 설정 추가

class Ifi05JobScheduleCreate(Ifi05JobScheduleBase):
    """새로운 작업 스케줄을 만들기 위한 필수 필드"""
    pass

class Ifi05JobScheduleUpdate(Ifi05JobScheduleBase):
    """작업 스케줄을 업데이트할 때 선택적으로 업데이트할 필드"""
    pass

class Ifi05JobScheduleResponse(Ifi05JobScheduleBase):
    """응답 스키마, id 포함"""
    ifi05_job_schedule_id: int = Field(..., description="작업스케줄 관리ID (PK)")
