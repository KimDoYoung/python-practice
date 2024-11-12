from pydantic import BaseModel, Field
from typing import Optional, List

class GosiListParam(BaseModel):
    ''' 공시리스트 파라메터 '''
    crtfc_key: str = Field(..., min_length=40, max_length=40, description="API 인증키 (필수) - 발급받은 40자리 인증키")
    corp_code: Optional[str] = Field(None, min_length=8, max_length=8, description="고유번호 - 공시대상회사의 8자리 고유번호")
    bgn_de: Optional[str] = Field(None, pattern=r"^\d{8}$", description="시작일 - 검색 시작 접수일자(YYYYMMDD)")
    end_de: Optional[str] = Field(None, pattern=r"^\d{8}$", description="종료일 - 검색 종료 접수일자(YYYYMMDD)")
    last_reprt_at: Optional[str] = Field("N", pattern=r"^[YN]$", description="최종보고서 검색여부 (Y 또는 N, 기본값: N)")
    pblntf_ty: Optional[str] = Field(None, pattern=r"^[A-J]$", description="공시유형 - A: 정기공시, B: 주요사항보고, C: 발행공시 등")
    pblntf_detail_ty: Optional[str] = Field(None, max_length=4, description="공시상세유형 - 4자리 상세 유형")
    corp_cls: Optional[str] = Field(None, pattern=r"^[YKNE]$", description="법인구분 - Y(유가), K(코스닥), N(코넥스), E(기타)")
    sort: Optional[str] = Field("date", pattern=r"^(date|crp|rpt)$", description="정렬 - date(접수일자), crp(회사명), rpt(보고서명), 기본값: date")
    sort_mth: Optional[str] = Field("desc", pattern=r"^(asc|desc)$", description="정렬방법 - asc(오름차순), desc(내림차순), 기본값: desc")
    page_no: Optional[int] = Field(1, ge=1, description="페이지 번호 - 1부터 시작, 기본값: 1")
    page_count: Optional[int] = Field(10, ge=1, le=100, description="페이지 별 건수 - 1~100 사이 값, 기본값: 10")


    class Config:
        json_schema_extra  = {
            "example": {
                "crtfc_key": "YOUR_CERTIFICATION_KEY",
                "corp_code": "12345678",
                "bgn_de": "20220101",
                "end_de": "20221231",
                "last_reprt_at": "Y",
                "pblntf_ty": "A",
                "pblntf_detail_ty": "0101",
                "corp_cls": "Y",
                "sort": "date",
                "sort_mth": "desc",
                "page_no": 1,
                "page_count": 10
            }
        }


class GosiListItem(BaseModel):
    corp_code: str  # 공시 대상 회사의 고유번호
    corp_name: str  # 회사명
    stock_code: Optional[str] = None  # 주식 코드 (없을 수 있음)
    corp_cls: str  # 법인 구분 (Y: 유가, K: 코스닥, N: 코넥스, E: 기타)
    report_nm: str  # 보고서명
    rcept_no: str  # 접수 번호
    flr_nm: str  # 제출인명
    rcept_dt: str  # 접수 일자 (YYYYMMDD 형식)
    rm: Optional[str] = None  # 비고 (정정 여부 표시)

class GosiListResponse(BaseModel):
    ''' 공시 리스트 응답 '''
    status: str  # API 요청 상태 코드 (예: "000" - 정상)
    message: str  # API 응답 메시지 (예: "정상")
    page_no: int  # 페이지 번호
    page_count: int  # 페이지당 건수
    total_count: int  # 총 데이터 건수
    total_page: int  # 총 페이지 수
    list: List[GosiListItem]  # 공시 목록

    class Config:
        json_schema_extra  = {
            "example": {
                "status": "000",
                "message": "정상",
                "page_no": 1,
                "page_count": 100,
                "total_count": 348,
                "total_page": 4,
                "list": [
                    {
                        "corp_code": "01706794",
                        "corp_name": "아이언디바이스",
                        "stock_code": "464500",
                        "corp_cls": "K",
                        "report_nm": "증권발행실적보고서",
                        "rcept_no": "20240912000065",
                        "flr_nm": "아이언디바이스",
                        "rcept_dt": "20240912",
                        "rm": ""
                    },
                    {
                        "corp_code": "01293485",
                        "corp_name": "제닉스",
                        "stock_code": "381620",
                        "corp_cls": "K",
                        "report_nm": "[기재정정]증권신고서(지분증권)",
                        "rcept_no": "20240912000167",
                        "flr_nm": "제닉스",
                        "rcept_dt": "20240912",
                        "rm": "정"
                    }
                ]
            }
        }



