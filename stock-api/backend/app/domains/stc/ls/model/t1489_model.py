# t1489_model.py
"""
모듈 설명: 
    -  상위종목-예상체결량상위조회

작성자: 김도영
작성일: 2024-07-16
버전: 1.0
"""
from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel
#요청모델 데이터
class T1489INBLOCK(StockApiBaseModel):
	gubun : str # 거래소구분 0:전체 1:코스피 2:코스닥
	jgubun : str # 장구분 0:장전 1:장후
	jongchk : str # 종목체크 대상제외값(설정시 저장됨) 증거금50 : 0x00400000 증거금100 : 0x00800000 증거금50/100 : 0x00200000 관리종목 : 0x00000080 시장경보 : 0x00000100 거래정지 : 0x00000200 우선주 : 0x00004000 투자유의 : 0x04000000 정리매매 : 0x01000000 불성실공시 : 0x80000000
	idx : int # IDX 다음 조회시 사용 첫 조회시 Space
	yesprice : int # 예상체결시작가격 yesprice <= 예상체결가 인 종목
	yeeprice : int # 예상체결종료가격 예상체결가 <= yeeprice 인 종목
	yevolume : int # 예상체결량 예상체결량 >= yevolume 인 종목

class T1489_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'Y'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	t1489InBlock : T1489INBLOCK

class T1489OUTBLOCK(StockApiBaseModel):
	idx: int # IDX 

class T1489OUTBLOCK1(StockApiBaseModel):
	hname: str # 한글명 
	price: int # 현재가 
	sign: str # 전일대비구분 
	change: int # 전일대비 
	diff: float # 등락율 
	volume: int # 예상거래량 
	offerho: int # 매도호가 
	bidho: int # 매수호가 
	shcode: str # 종목코드 
	jnilvolume: int # 전일거래량 

class T1489_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	t1489OutBlock: T1489OUTBLOCK
	t1489OutBlock1: List[T1489OUTBLOCK1] = []
