from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Sys08CodeKindBase: 공통코드 종류의 기본 스키마
class Sys08CodeKindBase(BaseModel):
    sys08_kind_cd: str  # 공통코드 종류 코드
    sys08_kind_nm: str  # 공통코드 종류 명칭
    sys08_sys_yn: Optional[str] = None  # 시스템 여부 (선택적 필드)
    sys08_note: Optional[str] = None  # 비고 (선택적 필드)

# Sys08CodeKindCreate: 공통코드 종류 생성 스키마
class Sys08CodeKindCreate(Sys08CodeKindBase):
    pass

# Sys08CodeKindUpdate: 공통코드 종류 업데이트 스키마
class Sys08CodeKindUpdate(Sys08CodeKindBase):
    pass

# Sys08CodeKindOut: 공통코드 종류 응답 스키마
class Sys08CodeKindOut(Sys08CodeKindBase):
    sys08_code_kind_id: int  # 공통코드 종류 ID

    class Config:
        orm_mode = True  # ORM 모델에서 데이터를 불러오는데 사용
        from_attributes = True  # ORM에서 데이터를 불러올 때 from_orm 설정 활성화


# Sys09CodeBase: 공통코드의 기본 스키마
class Sys09CodeBase(BaseModel):
    sys09_code: str  # 공통코드
    sys09_name: str  # 공통코드명
    sys09_seq: Optional[str] = None  # 순번 (선택적 필드)
    sys09_note: Optional[str] = None  # 비고 (선택적 필드)
    sys09_apply_date: datetime  # 적용일
    sys09_close_yn: Optional[str] = None  # 마감 여부 (선택적 필드)

# Sys09CodeCreate: 공통코드 생성 스키마
class Sys09CodeCreate(Sys09CodeBase):
    sys09_code_kind_id: int  # 공통코드 종류 ID
    sys09_company_id: int  # 회사 ID

# Sys09CodeUpdate: 공통코드 업데이트 스키마
class Sys09CodeUpdate(Sys09CodeBase):
    pass

# Sys09CodeOut: 공통코드 응답 스키마
class Sys09CodeOut(Sys09CodeBase):
    sys09_code_id: int  # 공통코드 ID

    class Config:
        orm_mode = True  # ORM 모델에서 데이터를 불러오는데 사용
        from_attributes = True  # ORM에서 데이터를 불러올 때 from_orm 설정 활성화
