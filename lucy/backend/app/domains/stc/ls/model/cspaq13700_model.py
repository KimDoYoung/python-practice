# cspaq13700_model.py
"""
모듈 설명: 
    - 계좌-현물계좌 주문체결내역 조회(API) 모델
    - tr_cd : CSPAQ13700
작성자: 김도영
작성일: 2024-07-09
버전: 1.0
"""
from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class CSPAQ13700InBlock1_Item(StockApiBaseModel):
	OrdMktCode : str = "00" # 주문시장코드 00.전체 10.거래소 20.코스닥 30.프리보드
	BnsTpCode : str ="0" # 매매구분 0@전체 1@매도 2@매수
	IsuNo : str  # 종목번호 주식 : A+종목코드 ELW : J+종목코드
	ExecYn : str = "0" # 체결여부 0.전체 1.체결 3.미체결
	OrdDt : str # 주문일 
	SrtOrdNo2 : int = 0 # 시작주문번호2 역순구분이 순 : 000000000 역순구분이 역순 : 999999999
	BkseqTpCode : str = "0" # 역순구분 0.역순 1.정순
	OrdPtnCode : str = "00" # 주문유형코드 00.전체 98.매도전체 99.매수전체 01.현금매도 02.현금매수 05.저축매도 06.저축매수 09.상품매도 10.상품매수 03.융자매도 04.융자매수 07.대주매도 08.대주매수 11.선물대용매도 13.현금매도(프) 14.현금매수(프) 17.대출 18.대출상환
	
class CSPAQ13700_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	CSPAQ13700InBlock1 : CSPAQ13700InBlock1_Item


class CSPAQ13700OUTBLOCK1(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	AcntNo: str # 계좌번호 
	InptPwd: str # 입력비밀번호 
	OrdMktCode: str # 주문시장코드 
	BnsTpCode: str # 매매구분 
	IsuNo: str # 종목번호 
	ExecYn: str # 체결여부 
	OrdDt: str # 주문일 
	SrtOrdNo2: int # 시작주문번호2 
	BkseqTpCode: str # 역순구분 
	OrdPtnCode: str # 주문유형코드 

class CSPAQ13700OUTBLOCK2(StockApiBaseModel):
	RecCnt: int # 레코드갯수 
	SellExecAmt: int # 매도체결금액 
	BuyExecAmt: int # 매수체결금액 
	SellExecQty: int # 매도체결수량 
	BuyExecQty: int # 매수체결수량 
	SellOrdQty: int # 매도주문수량 
	BuyOrdQty: int # 매수주문수량 

class CSPAQ13700OUTBLOCK3(StockApiBaseModel):
	OrdDt: str # 주문일 
	MgmtBrnNo: str # 관리지점번호 
	OrdMktCode: str # 주문시장코드 
	OrdNo: int # 주문번호 
	OrgOrdNo: int # 원주문번호 
	IsuNo: str # 종목번호 
	IsuNm: str # 종목명 
	BnsTpCode: str # 매매구분 
	BnsTpNm: str # 매매구분 
	OrdPtnCode: str # 주문유형코드 
	OrdPtnNm: str # 주문유형명 
	OrdTrxPtnCode: int # 주문처리유형코드 
	OrdTrxPtnNm: str # 주문처리유형명 
	MrcTpCode: str # 정정취소구분 
	MrcTpNm: str # 정정취소구분명 
	MrcQty: int # 정정취소수량 
	MrcAbleQty: int # 정정취소가능수량 
	OrdQty: int # 주문수량 
	OrdPrc: float # 주문가격 
	ExecQty: int # 체결수량 
	ExecPrc: float # 체결가 
	ExecTrxTime: str # 체결처리시각 
	LastExecTime: str # 최종체결시각 
	OrdprcPtnCode: str # 호가유형코드 
	OrdprcPtnNm: str # 호가유형명 
	OrdCndiTpCode: str # 주문조건구분 
	AllExecQty: int # 전체체결수량 
	RegCommdaCode: str # 통신매체코드 
	CommdaNm: str # 통신매체명 
	MbrNo: str # 회원번호 
	RsvOrdYn: str # 예약주문여부 
	LoanDt: str # 대출일 
	OrdTime: str # 주문시각 
	OpDrtnNo: str # 운용지시번호 
	OdrrId: str # 주문자ID 

class CSPAQ13700_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	CSPAQ13700OutBlock1: Optional[CSPAQ13700OUTBLOCK1] = None
	CSPAQ13700OutBlock2: Optional[CSPAQ13700OUTBLOCK2] = None
	CSPAQ13700OutBlock3: Optional[List[CSPAQ13700OUTBLOCK3]] = None