# t1482_model.py
"""
모듈 설명: 
    - 상위종목-시간외거래량상위

작성자: 김도영
작성일: 2024-07-16
버전: 1.0
"""
from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class T1482INBLOCK(StockApiBaseModel):
	gubun : str # 구분 0: 전체 1: 코스피 2: 코스닥
	jongchk : str # 거래량 0: 전체 1: 우선제외 2: 관리제외 3: 우선관리제외
	idx : int # IDX 연속조회시 OutBlock의 idx 입력


class T1482_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'Y'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	t1482InBlock : T1482INBLOCK

class T1482OUTBLOCK(StockApiBaseModel):
	idx: int # IDX 

class T1482OUTBLOCK1(StockApiBaseModel):
	hname: str # 종목명 
	price: int # 현재가 
	sign: str # 전일대비구분 
	change: int # 전일대비 
	diff: float # 등락율 
	volume: int # 누적거래량 
	vol: float # 회전율 
	shcode: str # 종목코드 
	value: int # 누적거래대금 

class T1482_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	t1482OutBlock: T1482OUTBLOCK
	t1482OutBlock1: List[T1482OUTBLOCK1] = []
