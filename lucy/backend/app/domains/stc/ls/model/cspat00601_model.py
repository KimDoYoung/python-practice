# cspat00601_model.py
"""
모듈 설명: 
    - LS 현물주문 모델들

작성자: 김도영
작성일: 2024-07-08
버전: 1.0
"""
from typing import Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class CSPAT00601OUTBLOCK1(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	AcntNo: str # 계좌번호 
	InptPwd: str # 입력비밀번호 
	IsuNo: str # 종목번호 
	OrdQty: int # 주문수량 
	OrdPrc: float # 주문가 
	BnsTpCode: str # 매매구분 
	OrdprcPtnCode: str # 호가유형코드 
	PrgmOrdprcPtnCode: str # 프로그램호가유형코드 
	StslAbleYn: str # 공매도가능여부 
	StslOrdprcTpCode: str # 공매도호가구분 
	CommdaCode: str # 통신매체코드 
	MgntrnCode: str # 신용거래코드 
	LoanDt: str # 대출일 
	MbrNo: str # 회원번호 
	OrdCndiTpCode: str # 주문조건구분 
	StrtgCode: str # 전략코드 
	GrpId: str # 그룹ID 
	OrdSeqNo: int # 주문회차 
	PtflNo: int # 포트폴리오번호 
	BskNo: int # 바스켓번호 
	TrchNo: int # 트렌치번호 
	ItemNo: int # 아이템번호 
	OpDrtnNo: str # 운용지시번호 
	LpYn: str # 유동성공급자여부 
	CvrgTpCode: str # 반대매매구분 

class CSPAT00601OUTBLOCK2(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	OrdNo: int # 주문번호 
	OrdTime: str # 주문시각 
	OrdMktCode: str # 주문시장코드 
	OrdPtnCode: str # 주문유형코드 
	ShtnIsuNo: str # 단축종목번호 
	MgempNo: str # 관리사원번호 
	OrdAmt: int # 주문금액 
	SpareOrdNo: int # 예비주문번호 
	CvrgSeqno: int # 반대매매일련번호 
	RsvOrdNo: int # 예약주문번호 
	SpotOrdQty: int # 실물주문수량 
	RuseOrdQty: int # 재사용주문수량 
	MnyOrdAmt: int # 현금주문금액 
	SubstOrdAmt: int # 대용주문금액 
	RuseOrdAmt: int # 재사용주문금액 
	AcntNm: str # 계좌명 
	IsuNm: str # 종목명 

class CSPAT00601_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	CSPAT00601OutBlock1: Optional[CSPAT00601OUTBLOCK1]=None
	CSPAT00601OutBlock2: Optional[CSPAT00601OUTBLOCK2]=None


class CSPAT00601InBlock1(StockApiBaseModel):
	IsuNo : str # 종목번호  주식/ETF : 종목코드 or A+종목코드(모의투자는 A+종목코드) ELW : J+종목코드 ETN : Q+종목코드
	OrdQty : int # 주문수량 
	OrdPrc : float # 주문가 
	BnsTpCode : str # 매매구분  1:매도, 2:매수
	OrdprcPtnCode : str # 호가유형코드  00@지정가 03@시장가 05@조건부지정가 06@최유리지정가 07@최우선지정가 61@장개시전시간외종가 81@시간외종가 82@시간외단일가
	MgntrnCode : Optional[str] = "000"  #신용거래코드  000:보통 003:유통/자기융자신규 005:유통대주신규 007:자기대주신규 101:유통융자상환 103:자기융자상환 105:유통대주상환 107:자기대주상환 180:예탁담보대출상환(신용)
	LoanDt : Optional[str] = "" # 대출일  nan
	OrdCndiTpCode : Optional[str] = "0" # 주문조건구분  0:없음,1:IOC,2:FOK

class CSPAT00601_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	CSPAT00601InBlock1 : CSPAT00601InBlock1