# t1481_model.py
"""
모듈 설명: 
    - 상위종목-시간외등락율상위

작성자: 김도영
작성일: 2024-07-16
버전: 1.0
"""
#요청모델 데이터
from typing import Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class T1481INBLOCK(StockApiBaseModel):
	gubun1 : str # 구분 0:전체 1:코스피 2:코스닥
	gubun2 : str # 상승하락 0: 상승률 1: 하락률
	jongchk : str # 종목체크 0: 전체 1: 우선제외 2: 관리제외 3: 우선관리제외
	volume : str # 거래량 0: 전체거래량 1: 1천주 이상 2: 5천주 이상 3: 1만주 이상 4: 5만주 이상 5: 10만주 이상 6: 50만주 이상 7: 100만주 이상
	idx : int # IDX 연속조회시 OutBlock의 idx 입력

class T1481_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	t1481InBlock : T1481INBLOCK

class T1481OUTBLOCK(StockApiBaseModel):
	idx: int # IDX 

class T1481OUTBLOCK1(StockApiBaseModel):
	hname: str # 한글명 
	price: int # 현재가 
	sign: str # 전일대비구분 
	change: int # 전일대비 
	diff: float # 등락율 
	volume: int # 누적거래량 
	offerrem1: int # 매도잔량 
	bidrem1: int # 매수잔량 
	offerho1: int # 매도호가 
	bidho1: int # 매수호가 
	shcode: str # 종목코드 
	value: int # 누적거래대금 

class T1481_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	t1481OutBlock: T1481OUTBLOCK
	t1481OutBlock1: T1481OUTBLOCK1
