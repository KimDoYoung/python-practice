from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Sys01CompanyBase(BaseModel):
    sys01_company_nm: str  # 회사명
    sys01_biz_no: str  # 사업자등록번호
    sys01_office_tel_no: Optional[str] = None  # 전화번호1 (선택적 필드)
    sys01_emgrcy_passwd: Optional[str] = None  # 전화번호2 (선택적 필드)
    sys01_office_fax_no: Optional[str] = None  # 팩스번호1 (선택적 필드)
    sys01_zip_cd: Optional[str] = None  # 우편번호 (선택적 필드)
    sys01_zip_addr: Optional[str] = None  # 주소 (선택적 필드)
    sys01_zip_detail: Optional[str] = None  # 상세주소 (선택적 필드)
    sys01_loc_nm: Optional[str] = None  # 지역명 (선택적 필드)
    sys01_anniv_date: Optional[datetime] = None  # 기념일 (선택적 필드)
    sys01_note: Optional[str] = None  # 비고 (선택적 필드)
    sys01_mail_info: Optional[str] = None  # 메일서버 정보 (선택적 필드)
    sys01_mobile_tel_no: Optional[str] = None  # 비상전화 (선택적 필드)
    sys01_email_addr: Optional[str] = None  # 비상이메일 (선택적 필드)
    sys01_start_date: Optional[datetime] = None  # 설립일 (선택적 필드)
    sys01_close_date: Optional[datetime] = None  # 계약종료일 (선택적 필드)
    sys01_use_yn: Optional[str] = None  # 사용여부 (선택적 필드)
    sys01_emp_info: Optional[str] = None  # 담당자(이름/부서/직책) (선택적 필드)

class Sys01CompanyCreate(Sys01CompanyBase):
    pass  # 회사 생성 시 필요한 스키마

class Sys01CompanyUpdate(Sys01CompanyBase):
    pass  # 회사 업데이트 시 필요한 스키마

class Sys01CompanyOut(Sys01CompanyBase):
    sys01_company_id: int  # 회사ID (응답 시 포함되는 필드)

    class Config:
        orm_mode = True  # ORM 모델에서 데이터를 불러오는데 사용
        from_attributes = True  # ORM에서 데이터를 불러올 때 from_orm 설정 활성화


class Sys08CodeKindBase(BaseModel):
    sys08_kind_cd: str  # 코드 종류 코드
    sys08_kind_nm: str  # 코드 종류 명칭
    sys08_sys_yn: Optional[str] = None  # 시스템 여부 (선택적 필드)
    sys08_note: Optional[str] = None  # 비고 (선택적 필드)

class Sys08CodeKindCreate(Sys08CodeKindBase):
    pass  # 코드 종류 생성 시 필요한 스키마

class Sys08CodeKindUpdate(Sys08CodeKindBase):
    pass  # 코드 종류 업데이트 시 필요한 스키마

class Sys08CodeKindOut(Sys08CodeKindBase):
    sys08_code_kind_id: int  # 코드 종류 ID (응답 시 포함되는 필드)

    class Config:
        orm_mode = True  # ORM 모델에서 데이터를 불러오는데 사용
        from_attributes = True  # ORM에서 데이터를 불러올 때 from_orm 설정 활성화


class Sys09CodeBase(BaseModel):
    sys09_code: str  # 코드
    sys09_name: str  # 코드명
    sys09_seq: Optional[str] = None  # 순번 (선택적 필드)
    sys09_note: Optional[str] = None  # 비고 (선택적 필드)
    sys09_apply_date: datetime  # 적용일
    sys09_close_yn: Optional[str] = None  # 마감 여부 (선택적 필드)

class Sys09CodeCreate(Sys09CodeBase):
    sys09_code_kind_id: int  # 코드 종류 ID (필수 필드)
    sys09_company_id: int  # 회사 ID (필수 필드)

class Sys09CodeUpdate(Sys09CodeBase):
    pass  # 코드 업데이트 시 필요한 스키마

class Sys09CodeOut(Sys09CodeBase):
    sys09_code_id: int  # 코드 ID (응답 시 포함되는 필드)

    class Config:
        orm_mode = True  # ORM 모델에서 데이터를 불러오는데 사용
        from_attributes = True  # ORM에서 데이터를 불러올 때 from_orm 설정 활성화
