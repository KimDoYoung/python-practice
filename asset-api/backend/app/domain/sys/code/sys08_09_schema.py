from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Sys08CodeKindBase(BaseModel):
    sys08_kind_cd: str
    sys08_kind_nm: str
    sys08_sys_yn: Optional[str] = None
    sys08_note: Optional[str] = None

class Sys08CodeKindCreate(Sys08CodeKindBase):
    pass

class Sys08CodeKindUpdate(Sys08CodeKindBase):
    pass

class Sys08CodeKindOut(Sys08CodeKindBase):
    sys08_code_kind_id: int

    class Config:
        orm_mode = True  # 반드시 orm_mode를 활성화해야 함
        from_attributes = True  # from_orm 사용을 위한 설정 추가


class Sys09CodeBase(BaseModel):
    sys09_code: str
    sys09_name: str
    sys09_seq: Optional[str] = None
    sys09_note: Optional[str] = None
    sys09_apply_date: datetime
    sys09_close_yn: Optional[str] = None

class Sys09CodeCreate(Sys09CodeBase):
    sys09_code_kind_id: int
    sys09_company_id: int

class Sys09CodeUpdate(Sys09CodeBase):
    pass

class Sys09CodeOut(Sys09CodeBase):
    sys09_code_id: int

    class Config:
        orm_mode = True  # 반드시 orm_mode를 활성화해야 함
        from_attributes = True  # from_orm 사용을 위한 설정 추가