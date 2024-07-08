
# cspat00701_model.py
"""
모듈 설명: 
    - LS 정정주문 
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-07-08
버전: 1.0
"""

from typing import Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel


class CSPAT00701OUTBLOCK1(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	OrgOrdNo: int # 원주문번호 
	AcntNo: str # 계좌번호 
	InptPwd: str # 입력비밀번호 
	IsuNo: str # 종목번호 
	OrdQty: int # 주문수량 
	OrdprcPtnCode: str # 호가유형코드 
	OrdCndiTpCode: str # 주문조건구분 
	OrdPrc: float # 주문가 
	CommdaCode: str # 통신매체코드 
	StrtgCode: str # 전략코드 
	GrpId: str # 그룹ID 
	OrdSeqNo: int # 주문회차 
	PtflNo: int # 포트폴리오번호 
	BskNo: int # 바스켓번호 
	TrchNo: int # 트렌치번호 
	ItemNo: int # 아이템번호 
	SPAT00701OutBlock2: int # CSPAT00701OutBlock2 
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
	OrdAmt: int # 주문금액 
	BnsTpCode: str # 매매구분 
	SpareOrdNo: int # 예비주문번호 
	CvrgSeqno: int # 반대매매일련번호 
	RsvOrdNo: int # 예약주문번호 
	MnyOrdAmt: int # 현금주문금액 
	SubstOrdAmt: int # 대용주문금액 
	RuseOrdAmt: int # 재사용주문금액 
	AcntNm: str # 계좌명 
	IsuNm: str # 종목명 

class CSPAT00701OUTBLOCK2(StockApiBaseModel):
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
	OrdAmt: int # 주문금액 
	BnsTpCode: str # 매매구분 
	SpareOrdNo: int # 예비주문번호 
	CvrgSeqno: int # 반대매매일련번호 
	RsvOrdNo: int # 예약주문번호 
	MnyOrdAmt: int # 현금주문금액 
	SubstOrdAmt: int # 대용주문금액 
	RuseOrdAmt: int # 재사용주문금액 
	AcntNm: str # 계좌명 
	IsuNm: str # 종목명 

class CSPAT00701_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	CSPAT00701OutBlock1: CSPAT00701OUTBLOCK1
	CSPAT00701OutBlock2: CSPAT00701OUTBLOCK2


class CSPAT00701InBlock1(StockApiBaseModel):
	OrgOrdNo : int # 원주문번호 # nan
	IsuNo : str # 종목번호 # 주식 : 종목코드 or A+종목코드(모의투자는 A+종목코드) ELW : J+종목코드 ETN : Q+종목코드
	OrdQty : int # 주문수량 # nan
	OrdprcPtnCode : str # 호가유형코드 # 00@지정가 03@시장가 05@조건부지정가 06@최유리지정가 07@최우선지정가 61@장개시전시간외종가 81@시간외종가 82@시간외단일가
	OrdCndiTpCode : str # 주문조건구분 # 0:없음, 1:IOC, 2:FOK
	OrdPrc : int # 주문가 # nan

class CSPAT00701_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	CSPAT00701InBlock1 :CSPAT00701InBlock1