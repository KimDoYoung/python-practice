# t8407_model.py
"""
모듈 설명: 
    - [주식] 시세-API용주식멀티현재가조회
	- tr_cd : t8407

작성자: 김도영
작성일: 2024-07-10
버전: 1.0
"""

from typing import List, Optional

from pydantic import BaseModel
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class T8407InBLOCK(StockApiBaseModel):
	nrec : int # 건수 최대 50개까지
	shcode : str # 종목코드 구분자 없이 종목코드를 붙여서 입력 078020, 000660, 005930 을 전송시 '078020000660005930' 을 입력

class T8407_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	t8407InBlock : T8407InBLOCK
	
class T8407OUTBLOCK1(StockApiBaseModel):
	shcode: str # 종목코드 
	hname: str # 종목명 
	price: int # 현재가 
	sign: str # 전일대비구분 
	change: int # 전일대비 
	diff: float # 등락율 
	volume: int # 누적거래량 
	offerho: int # 매도호가 
	bidho: int # 매수호가 
	cvolume: int # 체결수량 
	chdegree: float # 체결강도 
	open: int # 시가 
	high: int # 고가 
	low: int # 저가 
	value: int # 거래대금(백만) 
	offerrem: int # 우선매도잔량 
	bidrem: int # 우선매수잔량 
	totofferrem: int # 총매도잔량 
	totbidrem: int # 총매수잔량 
	jnilclose: int # 전일종가 
	uplmtprice: int # 상한가 
	dnlmtprice: int # 하한가 

class T8407_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	t8407OutBlock1: List[T8407OUTBLOCK1]

class ArrayStkCodes(BaseModel):
    ''' router에서 받을 때 사용'''	
    stk_codes: List[str]    