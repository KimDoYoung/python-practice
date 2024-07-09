# cspat00801_model.py
"""
모듈 설명: 
    - LS 현물주문 취소 모델들

작성자: 김도영
작성일: 2024-07-08
버전: 1.0
"""

from typing import Optional

from pydantic import Field
from backend.app.domains.stock_api_base_model import StockApiBaseModel


class CSPAT00801OUTBLOCK1(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	OrgOrdNo: int # 원주문번호 
	AcntNo: str # 계좌번호 
	InptPwd: str # 입력비밀번호 
	IsuNo: str # 종목번호 
	OrdQty: int # 주문수량 
	CommdaCode: str # 통신매체코드 
	GrpId: str # 그룹ID 
	StrtgCode: str # 전략코드 
	OrdSeqNo: int # 주문회차 
	PtflNo: int # 포트폴리오번호 
	BskNo: int # 바스켓번호 
	TrchNo: int # 트렌치번호 
	ItemNo: int # 아이템번호 

class CSPAT00801OUTBLOCK2(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	OrdNo: int # 주문번호 
	PrntOrdNo: int # 모주문번호 
	OrdTime: str # 주문시각 
	OrdMktCode: str # 주문시장코드 
	OrdPtnCode: str # 주문유형코드 
	ShtnIsuNo: str # 단축종목번호 
	PrgmOrdprcPtnCode: str # 프로그램호가유형코드 
	StslOrdprcTpCode: str # 공매도호가구분 
	StslAbleYn: str # 공매도가능여부 
	MgntrnCode: str # 신용거래코드 
	LoanDt: str # 대출일 
	CvrgOrdTp: str # 반대매매주문구분 
	LpYn: str # 유동성공급자여부 
	MgempNo: str # 관리사원번호 
	BnsTpCode: str # 매매구분 
	SpareOrdNo: int # 예비주문번호 
	CvrgSeqno: int # 반대매매일련번호 
	RsvOrdNo: int # 예약주문번호 
	AcntNm: str # 계좌명 
	IsuNm: str # 종목명 

class CSPAT00801_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	CSPAT00801OutBlock1: CSPAT00801OUTBLOCK1
	CSPAT00801OutBlock2: CSPAT00801OUTBLOCK2


class CSPAT00801InBlock1(StockApiBaseModel):
    OrgOrdNo: int = Field(..., description="원주문번호")
    IsuNo: str = Field(..., description="종목번호")
    OrdQty: int = Field(..., description="주문수량")

class CSPAT00801_Request(StockApiBaseModel):
    tr_cont: Optional[str] = 'N'
    tr_cont_key: Optional[str] = ''
    mac_address: Optional[str] = ''
    CSPAT00801InBlock1: CSPAT00801InBlock1	
