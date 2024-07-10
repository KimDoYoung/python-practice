# cdpcq04700_model.py
"""
모듈 설명: 
    - LS 주식계좌내역 모델
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-07-09
버전: 1.0
"""

#요청모델 데이터
from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class CDPCQ04700InBlock1(StockApiBaseModel):
	QryTp : str = '0' # 조회구분 0@전체, 1@입출금, 2@입출고, 3@매매, 4@환전, 9@기타
	QrySrtDt : str # 조회시작일 
	QryEndDt : str # 조회종료일 
	SrtNo : int = 0 # 시작번호 
	PdptnCode : str = '01' # 상품유형코드 01
	IsuLgclssCode : str = '01' # 종목대분류코드 00@전체, 01@주식, 02@채권, 04@펀드, 03@선물, 05@해외주식, 06@해외파생
	IsuNo : str # 종목번호 12자리
	
class CDPCQ04700_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	CDPCQ04700InBlock1 : CDPCQ04700InBlock1

class CDPCQ04700OUTBLOCK1(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	QryTp: str # 조회구분 
	AcntNo: str # 계좌번호 
	Pwd: str # 비밀번호 
	QrySrtDt: str # 조회시작일 
	QryEndDt: str # 조회종료일 
	SrtNo: int # 시작번호 
	PdptnCode: str # 상품유형코드 
	IsuLgclssCode: str # 종목대분류코드 
	IsuNo: str # 종목번호 

class CDPCQ04700OUTBLOCK2(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	AcntNm: str # 계좌명 

class CDPCQ04700OUTBLOCK3(StockApiBaseModel):
	AcntNo: str # 계좌번호 
	TrdDt: str # 거래일자 
	TrdNo: int # 거래번호 
	TpCodeNm: str # 구분코드명 
	SmryNo: str # 적요번호 
	SmryNm: str # 적요명 
	CancTpNm: str # 취소구분 
	TrdQty: int # 거래수량 
	Trtax: int # 거래세 
	FcurrAdjstAmt: float # 외화정산금액 
	AdjstAmt: int # 정산금액 
	OvdSum: int # 연체합 
	DpsBfbalAmt: int # 예수금전잔금액 
	SellPldgRfundAmt: int # 매도담보상환금 
	DpspdgLoanBfbalAmt: int # 예탁담보대출전잔금액 
	TrdmdaNm: str # 거래매체명 
	OrgTrdNo: int # 원거래번호 
	IsuNm: str # 종목명 
	TrdUprc: float # 거래단가 
	CmsnAmt: int # 수수료 
	FcurrCmsnAmt: float # 외화수수료금액 
	RfundDiffAmt: int # 상환차이금액 
	RepayAmtSum: int # 변제금합계 
	SecCrbalQty: int # 유가증권금잔수량 
	CslLoanRfundIntrstAmt: int # 매도대금담보대출상환이자금액 
	DpspdgLoanCrbalAmt: int # 예탁담보대출금잔금액 
	TrxTime: str # 처리시각 
	Inouno: int # 출납번호 
	IsuNo: str # 종목번호 
	TrdAmt: int # 거래금액 
	ChckAmt: int # 수표금액 
	TaxSumAmt: int # 세금합계금액 
	FcurrTaxSumAmt: float # 외화세금합계금액 
	IntrstUtlfee: int # 이자이용료 
	MnyDvdAmt: int # 배당금액 
	RcvblOcrAmt: int # 미수발생금액 
	TrxBrnNo: str # 처리지점번호 
	TrxBrnNm: str # 처리지점명 
	DpspdgLoanAmt: int # 예탁담보대출금액 
	DpspdgLoanRfundAmt: int # 예탁담보대출상환금액 
	BasePrc: float # 기준가 
	DpsCrbalAmt: int # 예수금금잔금액 
	BoaAmt: int # 과표 
	MnyoutAbleAmt: int # 출금가능금액 
	BcrLoanOcrAmt: int # 수익증권담보대출발생금 
	BcrLoanBfbalAmt: int # 수익증권담보대출전잔금 
	BnsBasePrc: float # 매매기준가 
	TaxchrBasePrc: float # 과세기준가 
	TrdUnit: int # 거래좌수 
	BalUnit: int # 잔고좌수 
	EvrTax: int # 제세금 
	EvalAmt: int # 평가금액 
	BcrLoanRfundAmt: int # 수익증권담보대출상환금 
	BcrLoanCrbalAmt: int # 수익증권담보대출금잔금 
	AddMgnOcrTotamt: int # 추가증거금발생총액 
	AddMnyMgnOcrAmt: int # 추가현금증거금발생금액 
	AddMgnDfryTotamt: int # 추가증거금납부총액 
	AddMnyMgnDfryAmt: int # 추가현금증거금납부금액 
	BnsplAmt: int # 매매손익금액 
	Ictax: int # 소득세 
	Ihtax: int # 주민세 
	LoanDt: str # 대출일 
	CrcyCode: str # 통화코드 
	FcurrAmt: float # 외화금액 
	FcurrTrdAmt: float # 외화거래금액 
	FcurrDps: float # 외화예수금 
	FcurrDpsBfbalAmt: float # 외화예수금전잔금액 
	OppAcntNm: str # 상대계좌명 
	OppAcntNo: str # 상대계좌번호 
	LoanRfundAmt: int # 대출상환금액 
	LoanIntrstAmt: int # 대출이자금액 
	AskpsnNm: str # 의뢰인명 
	OrdDt: str # 주문일자 
	TrdXchrat: float # 거래환율 
	RdctCmsn: float # 감면수수료 
	FcurrStmpTx: float # 외화인지세 
	FcurrElecfnTrtax: float # 외화전자금융거래세 
	FcstckTrtax: float # 외화증권거래세 	

class CDPCQ04700OUTBLOCK4(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	PnlSumAmt: int # 손익합계금액 
	CtrctAsm: int # 약정누계 
	CmsnAmtSumAmt: int # 수수료합계금액 

class CDPCQ04700OUTBLOCK5(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	MnyinAmt: int # 입금금액 
	SecinAmt: int # 입고금액 
	MnyoutAmt: int # 출금금액 
	SecoutAmt: int # 출고금액 
	DiffAmt: int # 차이금액 
	DiffAmt0: int # 차이금액0 
	SellQty: int # 매도수량 
	SellAmt: int # 매도금액 
	SellCmsn: int # 매도수수료 
	EvrTax: int # 제세금 
	FcurrSellAdjstAmt: float # 외화매도정산금액 
	BuyQty: int # 매수수량 
	BuyAmt: int # 매수금액 
	BuyCmsn: int # 매수수수료 
	ExecTax: int # 체결세금 
	FcurrBuyAdjstAmt: float # 외화매수정산금액 

class CDPCQ04700_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	CDPCQ04700OutBlock1: Optional[CDPCQ04700OUTBLOCK1] = None
	CDPCQ04700OutBlock2: Optional[CDPCQ04700OUTBLOCK2] = None
	CDPCQ04700OutBlock3: Optional[List[CDPCQ04700OUTBLOCK3]] = None  # 리스트로 변경
	CDPCQ04700OutBlock4: Optional[CDPCQ04700OUTBLOCK4] = None
	CDPCQ04700OutBlock5: Optional[CDPCQ04700OUTBLOCK5] = None
