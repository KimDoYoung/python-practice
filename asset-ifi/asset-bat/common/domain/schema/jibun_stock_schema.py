from pydantic import BaseModel, Field
from typing import List, Optional

class JibunStockParam(BaseModel):
    ''' 지분증권 보고서 파라메터 '''
    crtfc_key: str = Field(..., min_length=40, max_length=40, description="API 인증키 (필수) - 발급받은 40자리 인증키")
    corp_code: str = Field(..., min_length=8, max_length=8, description="고유번호 (필수) - 공시대상회사의 8자리 고유번호")
    bgn_de: str = Field(..., pattern=r"^\d{8}$", description="시작일 (필수) - 검색 시작 접수일자(YYYYMMDD)")
    end_de: str = Field(..., pattern=r"^\d{8}$", description="종료일 (필수) - 검색 종료 접수일자(YYYYMMDD)")
    

    class Config:
        json_schema_extra  = {
            "example": {
                "crtfc_key": "YOUR_CERTIFICATION_KEY",
                "corp_code": "12345678",
                "bgn_de": "20230101",
                "end_de": "20231231"
            }
        }
        

class GeneralInfoItem(BaseModel):
    rcept_no: str  # 접수 번호
    corp_cls: str  # 법인 구분
    corp_code: str  # 고유번호
    corp_name: str  # 회사명
    sbd: Optional[str] = None  # 신주 발행일 범위
    pymd: Optional[str] = None  # 지급일
    sband: Optional[str] = None  # 신주 배정일
    asand: Optional[str] = None  # 구주 배정일
    asstd: Optional[str] = None  # 배정 기준일
    exstk: Optional[str] = None  # 배정 기준 주식 수
    exprc: Optional[str] = None  # 주식 매입가
    expd: Optional[str] = None  # 주식 매입기한
    rpt_rcpn: Optional[str] = None  # 보고서 수령인

class StockTypeItem(BaseModel):
    rcept_no: str  # 접수 번호
    corp_cls: str  # 법인 구분
    corp_code: str  # 고유번호
    corp_name: str  # 회사명
    stksen: Optional[str] = None  # 증권의 종류
    stkcnt: Optional[str] = None  # 발행 주식 수
    fv: Optional[str] = None  # 액면가
    slprc: Optional[str] = None  # 발행가
    slta: Optional[str] = None  # 발행 총액
    slmthn: Optional[str] = None  # 발행 방식 (예: 일반공모)

class GroupItem(BaseModel):
    title: str  # 그룹 제목 (예: 일반사항, 증권의종류)
    list: List[GeneralInfoItem] = []  # 그룹별 정보 항목

class JibunStockResponse(BaseModel):
    ''' 지분증권 보고서 응답 '''
    status: str  # API 상태 코드 (예: "000" - 정상)
    message: str  # API 응답 메시지 (예: "정상")
    group: Optional[List[GroupItem]] = None  # 그룹 정보 목록

    class Config:
        json_schema_extra  = {
            "example": {
                "status": "000",
                "message": "정상",
                "group": [
                    {
                        "title": "일반사항",
                        "list": [
                            {
                                "rcept_no": "20241015000072",
                                "corp_cls": "Y",
                                "corp_code": "00968607",
                                "corp_name": "더본코리아",
                                "sbd": "2024년 10월 28일 ~ 2024년 10월 29일",
                                "pymd": "2024년 10월 31일",
                                "sband": "2024년 10월 28일",
                                "asand": "2024년 10월 31일",
                                "asstd": "-",
                                "exstk": "-",
                                "exprc": "-",
                                "expd": "-",
                                "rpt_rcpn": "-"
                            }
                        ]
                    },
                    {
                        "title": "증권의종류",
                        "list": [
                            {
                                "rcept_no": "20241015000072",
                                "corp_cls": "Y",
                                "corp_code": "00968607",
                                "corp_name": "더본코리아",
                                "stksen": "보통주",
                                "stkcnt": "3,000,000",
                                "fv": "500",
                                "slprc": "23,000",
                                "slta": "69,000,000,000",
                                "slmthn": "일반공모"
                            }
                        ]
                    }
                ]
            }
        }
