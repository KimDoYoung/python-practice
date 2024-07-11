
# cspaq12300_model.py
"""
모듈 설명: 
    - [주식] 계좌-BEP단가조회
	- tr_cd : CSPAQ12300

작성자: 김도영
작성일: 2024-07-11
버전: 1.0
"""
from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel


class CSPAQ12300InBlock1(StockApiBaseModel):
	BalCreTp : str = "0" # 잔고생성구분 0:전체 1:현물 9:선물대용
	CmsnAppTpCode : str = "1" # 수수료적용구분 0:평가시 수수료 미적용 1:평가시 수수료 적용
	D2balBaseQryTp : str = "0" # D2잔고기준조회구분 0:전부조회 1:D2잔고 0이상만 조회
	UprcTpCode : str = "1" # 단가구분 0:평균단가 1:BEP단가

class CSPAQ12300_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	CSPAQ12300InBlock1 : CSPAQ12300InBlock1 

class CSPAQ12300OUTBLOCK1(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	AcntNo: str # 계좌번호 
	Pwd: str # 비밀번호 
	BalCreTp: str # 잔고생성구분 
	CmsnAppTpCode: str # 수수료적용구분 
	D2balBaseQryTp: str # D2잔고기준조회구분 
	UprcTpCode: str # 단가구분 
	

class CSPAQ12300OUTBLOCK2(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	BrnNm: str # 지점명 
	AcntNm: str # 계좌명 
	MnyOrdAbleAmt: int # 현금주문가능금액 
	MnyoutAbleAmt: int # 출금가능금액 
	SeOrdAbleAmt: int # 거래소금액 
	KdqOrdAbleAmt: int # 코스닥금액 
	HtsOrdAbleAmt: int # HTS주문가능금액 
	MgnRat100pctOrdAbleAmt: int # 증거금률100퍼센트주문가능금액 
	BalEvalAmt: int # 잔고평가금액 
	PchsAmt: int # 매입금액 
	RcvblAmt: int # 미수금액 
	PnlRat: float # 손익율 
	InvstOrgAmt: int # 투자원금 
	InvstPlAmt: int # 투자손익금액 
	CrdtPldgOrdAmt: int # 신용담보주문금액 
	Dps: int # 예수금 
	D1Dps: int # D1예수금 
	D2Dps: int # D2예수금 
	OrdDt: str # 주문일 
	MnyMgn: int # 현금증거금액 
	SubstMgn: int # 대용증거금액 
	SubstAmt: int # 대용금액 
	PrdayBuyExecAmt: int # 전일매수체결금액 
	PrdaySellExecAmt: int # 전일매도체결금액 
	CrdayBuyExecAmt: int # 금일매수체결금액 
	CrdaySellExecAmt: int # 금일매도체결금액 
	EvalPnlSum: int # 평가손익합계 
	DpsastTotamt: int # 예탁자산총액 
	Evrprc: int # 제비용 
	RuseAmt: int # 재사용금액 
	EtclndAmt: int # 기타대여금액 
	PrcAdjstAmt: int # 가정산금액 
	D1CmsnAmt: int # D1수수료 
	D2CmsnAmt: int # D2수수료 
	D1EvrTax: int # D1제세금 
	D2EvrTax: int # D2제세금 
	D1SettPrergAmt: int # D1결제예정금액 
	D2SettPrergAmt: int # D2결제예정금액 
	PrdayKseMnyMgn: int # 전일KSE현금증거금 
	PrdayKseSubstMgn: int # 전일KSE대용증거금 
	PrdayKseCrdtMnyMgn: int # 전일KSE신용현금증거금 
	PrdayKseCrdtSubstMgn: int # 전일KSE신용대용증거금 
	CrdayKseMnyMgn: int # 금일KSE현금증거금 
	CrdayKseSubstMgn: int # 금일KSE대용증거금 
	CrdayKseCrdtMnyMgn: int # 금일KSE신용현금증거금 
	CrdayKseCrdtSubstMgn: int # 금일KSE신용대용증거금 
	PrdayKdqMnyMgn: int # 전일코스닥현금증거금 
	PrdayKdqSubstMgn: int # 전일코스닥대용증거금 
	PrdayKdqCrdtMnyMgn: int # 전일코스닥신용현금증거금 
	PrdayKdqCrdtSubstMgn: int # 전일코스닥신용대용증거금 
	CrdayKdqMnyMgn: int # 금일코스닥현금증거금 
	CrdayKdqSubstMgn: int # 금일코스닥대용증거금 
	CrdayKdqCrdtMnyMgn: int # 금일코스닥신용현금증거금 
	CrdayKdqCrdtSubstMgn: int # 금일코스닥신용대용증거금 
	PrdayFrbrdMnyMgn: int # 전일프리보드현금증거금 
	PrdayFrbrdSubstMgn: int # 전일프리보드대용증거금 
	CrdayFrbrdMnyMgn: int # 금일프리보드현금증거금 
	CrdayFrbrdSubstMgn: int # 금일프리보드대용증거금 
	PrdayCrbmkMnyMgn: int # 전일장외현금증거금 
	PrdayCrbmkSubstMgn: int # 전일장외대용증거금 
	CrdayCrbmkMnyMgn: int # 금일장외현금증거금 
	CrdayCrbmkSubstMgn: int # 금일장외대용증거금 
	DpspdgQty: int # 예탁담보수량 
	BuyAdjstAmtD2: int # 매수정산금(D+2) 
	SellAdjstAmtD2: int # 매도정산금(D+2) 
	RepayRqrdAmtD1: int # 변제소요금(D+1) 
	RepayRqrdAmtD2: int # 변제소요금(D+2) 
	LoanAmt: int # 대출금액 

class CSPAQ12300OUTBLOCK3(StockApiBaseModel):
	IsuNo: str # 종목번호 
	IsuNm: str # 종목명 
	SecBalPtnCode: str # 유가증권잔고유형코드 
	SecBalPtnNm: str # 유가증권잔고유형명 
	BalQty: int # 잔고수량 
	BnsBaseBalQty: int # 매매기준잔고수량 
	CrdayBuyExecQty: int # 금일매수체결수량 
	CrdaySellExecQty: int # 금일매도체결수량 
	SellPrc: float # 매도가 
	BuyPrc: float # 매수가 
	SellPnlAmt: int # 매도손익금액 
	PnlRat: float # 손익율 
	NowPrc: float # 현재가 
	CrdtAmt: int # 신용금액 
	DueDt: str # 만기일 
	PrdaySellExecPrc: float # 전일매도체결가 
	PrdaySellQty: int # 전일매도수량 
	PrdayBuyExecPrc: float # 전일매수체결가 
	PrdayBuyQty: int # 전일매수수량 
	LoanDt: str # 대출일 
	AvrUprc: float # 평균단가 
	SellAbleQty: int # 매도가능수량 
	SellOrdQty: int # 매도주문수량 
	CrdayBuyExecAmt: int # 금일매수체결금액 
	CrdaySellExecAmt: int # 금일매도체결금액 
	PrdayBuyExecAmt: int # 전일매수체결금액 
	PrdaySellExecAmt: int # 전일매도체결금액 
	BalEvalAmt: int # 잔고평가금액 
	EvalPnl: int # 평가손익 
	MnyOrdAbleAmt: int # 현금주문가능금액 
	OrdAbleAmt: int # 주문가능금액 
	SellUnercQty: int # 매도미체결수량 
	SellUnsttQty: int # 매도미결제수량 
	BuyUnercQty: int # 매수미체결수량 
	BuyUnsttQty: int # 매수미결제수량 
	UnsttQty: int # 미결제수량 
	UnercQty: int # 미체결수량 
	PrdayCprc: float # 전일종가 
	PchsAmt: int # 매입금액 
	RegMktCode: str # 등록시장코드 
	LoanDtlClssCode: str # 대출상세분류코드 
	DpspdgLoanQty: int # 예탁담보대출수량 

class CSPAQ12300_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	CSPAQ12300OutBlock1: CSPAQ12300OUTBLOCK1
	CSPAQ12300OutBlock2: CSPAQ12300OUTBLOCK2
	CSPAQ12300OutBlock3: List[CSPAQ12300OUTBLOCK3]
