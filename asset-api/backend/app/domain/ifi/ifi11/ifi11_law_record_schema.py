from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class Ifi11LawRecordBase(BaseModel):
    ifi11_dml_type: Optional[str]
    ifi11_dml_date: Optional[date]
    ifi11_dml_date_time: Optional[datetime]
    ifi11_ics_class_tree_id: Optional[int]

class Ifi11LawRecordCreate(Ifi11LawRecordBase):
    pass

class Ifi11LawRecordResponse(Ifi11LawRecordBase):
    ifi11_law_record_id: int

    class Config:
        orm_mode = True  # 반드시 orm_mode를 활성화해야 함
        from_attributes = True  # from_orm 사용을 위한 설정 추가
