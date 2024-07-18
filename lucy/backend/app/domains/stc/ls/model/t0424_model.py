# t0424_model.py
"""
모듈 설명: 
    - [주식] 계좌-주식잔고2 
    - tr_cd : t0424
작성자: 김도영
작성일: 2024-07-11
버전: 1.0
"""
from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel


class T0424INBLOCK(StockApiBaseModel):	
    prcgb : str = "" # 단가구분 
    chegb : str = "" # 체결구분 
    dangb : str = "" # 단일가구분 
    charge : str = ""  # 제비용포함여부 
    cts_expcode : str = "" # CTS_종목번호 연속조회시 OutBlock의 동일필드 입력

class T0424_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	t0424InBlock : T0424INBLOCK


class T0424OUTBLOCK(StockApiBaseModel):
	sunamt: int # 추정순자산 
	dtsunik: int # 실현손익 
	mamt: int # 매입금액 
	sunamt1: int # 추정D2예수금 
	cts_expcode: str # CTS_종목번호 
	tappamt: int # 평가금액 
	tdtsunik: int # 평가손익 


class T0424OUTBLOCK1(StockApiBaseModel):
	expcode: str # 종목번호 
	jangb: str # 잔고구분 
	janqty: int # 잔고수량 
	mdposqt: int # 매도가능수량 
	pamt: int # 평균단가 
	mamt: int # 매입금액 
	sinamt: int # 대출금액 
	lastdt: str # 만기일자 
	msat: int # 당일매수금액 
	mpms: int # 당일매수단가 
	mdat: int # 당일매도금액 
	mpmd: int # 당일매도단가 
	jsat: int # 전일매수금액 
	jpms: int # 전일매수단가 
	jdat: int # 전일매도금액 
	jpmd: int # 전일매도단가 
	sysprocseq: int # 처리순번 
	loandt: str # 대출일자 
	hname: str # 종목명 
	marketgb: str # 시장구분 
	jonggb: str # 종목구분 
	janrt: float # 보유비중 
	price: int # 현재가 
	appamt: int # 평가금액 
	dtsunik: int # 평가손익 
	sunikrt: float # 수익율 
	fee: int # 수수료 
	tax: int # 제세금 
	sininter: int # 신용이자 

class T0424_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	t0424OutBlock: T0424OUTBLOCK
	t0424OutBlock1: List[T0424OUTBLOCK1]