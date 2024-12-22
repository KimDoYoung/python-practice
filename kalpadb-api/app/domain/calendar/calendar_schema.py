from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class CalendarBase(BaseModel):
    gubun: str = Field(..., max_length=1, description="종류")
    sorl: str = Field('S', max_length=1, description="S: Sun, L: Lunar")
    ymd: Optional[str] = Field(None, max_length=8, description="날짜")
    content: str = Field(..., max_length=100, description="내용")

    @field_validator('sorl')
    def validate_sorl(cls, value):
        if value not in ('S', 'L'):
            raise ValueError("sorl must be 'S' or 'L'")
        return value
    
    @field_validator('gubun')
    def validate_gubun(cls, value):
        if value not in ('H', 'E', 'Y', 'M'):
            raise ValueError("gubun must be one of 'H', 'E', 'Y', 'M'")
        return value

# gubun H: Holiday, E: Event, Y: PeriadYear, M: PeriadMonth, L: Lunar


class CalendarRequest(CalendarBase):
    pass


class CalendarResponse(CalendarBase):
    id: int = Field(..., description="ID")
    modify_dt: datetime = Field(..., description="수정일시")

    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }
