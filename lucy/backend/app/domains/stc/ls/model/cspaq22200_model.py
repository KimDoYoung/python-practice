# cspaq22200_model.py
"""
모듈 설명: 
    - [주식] 계좌-현물계좌예수금 주문가능금액 총평가2 모델

작성자: 김도영
작성일: 2024-08-29
버전: 1.0
"""
from typing import Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel
class CSPAQ22200InBlock1(StockApiBaseModel):
    BalCreTp: str = "0" # 잔고생성구분 0.0
    
class CSPAQ22200_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	CSPAQ22200InBlock1 : CSPAQ22200InBlock1 

class CSPAQ22200OUTBLOCK1(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	MgmtBrnNo: str # 관리지점번호 
	AcntNo: str # 계좌번호 
	Pwd: str # 비밀번호 
	BalCreTp: str # 잔고생성구분 

class CSPAQ22200OUTBLOCK2(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	BrnNm: str # 지점명 
	AcntNm: str # 계좌명 
	MnyOrdAbleAmt: int # 현금주문가능금액 
	SubstOrdAbleAmt: int # 대용주문가능금액 
	SeOrdAbleAmt: int # 거래소금액 
	KdqOrdAbleAmt: int # 코스닥금액 
	CrdtPldgOrdAmt: int # 신용담보주문금액 
	MgnRat100pctOrdAbleAmt: int # 증거금률100퍼센트주문가능금액 
	MgnRat35ordAbleAmt: int # 증거금률35%주문가능금액 
	MgnRat50ordAbleAmt: int # 증거금률50%주문가능금액 
	CrdtOrdAbleAmt: int # 신용주문가능금액 
	Dps: int # 예수금 
	SubstAmt: int # 대용금액 
	MgnMny: int # 증거금현금 
	MgnSubst: int # 증거금대용 
	D1Dps: int # D1예수금 
	D2Dps: int # D2예수금 
	RcvblAmt: int # 미수금액 
	D1ovdRepayRqrdAmt: int # D1연체변제소요금액 
	D2ovdRepayRqrdAmt: int # D2연체변제소요금액 
	MloanAmt: int # 융자금액 
	ChgAfPldgRat: float # 변경후담보비율 
	RqrdPldgAmt: int # 소요담보금액 
	PdlckAmt: int # 담보부족금액 
	OrgPldgSumAmt: int # 원담보합계금액 
	SubPldgSumAmt: int # 부담보합계금액 
	CrdtPldgAmtMny: int # 신용담보금현금 
	CrdtPldgSubstAmt: int # 신용담보대용금액 
	Imreq: int # 신용설정보증금 
	CrdtPldgRuseAmt: int # 신용담보재사용금액 
	DpslRestrcAmt: int # 처분제한금액 
	PrdaySellAdjstAmt: int # 전일매도정산금액 
	PrdayBuyAdjstAmt: int # 전일매수정산금액 
	CrdaySellAdjstAmt: int # 금일매도정산금액 
	CrdayBuyAdjstAmt: int # 금일매수정산금액 
	CslLoanAmtdt1: int # 매도대금담보대출금액 

class CSPAQ22200_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	CSPAQ22200OutBlock1: CSPAQ22200OUTBLOCK1
	CSPAQ22200OutBlock2: CSPAQ22200OUTBLOCK2