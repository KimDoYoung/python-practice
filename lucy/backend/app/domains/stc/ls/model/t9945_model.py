# t9945_model.py
"""
모듈 설명: 
    - [주식] 시세-주식마스터조회API용
    - tr_cd : t9945
작성자: 김도영
작성일: 2024-07-10
버전: 1.0
"""
from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class T9945INBLOCK(StockApiBaseModel):
    gubun: str = '1' # 구분(KSP:1KSD:2)

class T9945_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	t9945InBlock: T9945INBLOCK

class T9945OUTBLOCK(StockApiBaseModel):
	hname: str # 종목명 
	shcode: str # 단축코드 
	expcode: str # 확장코드 
	etfchk: str # ETF구분 
	filler: str # filler 

class T9945_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	t9945OutBlock: List[T9945OUTBLOCK]