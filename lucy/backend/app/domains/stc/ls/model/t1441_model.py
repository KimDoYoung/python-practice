# t1441_model.py
"""
모듈 설명: 
    - 상위종목 : 등락률

작성자: 김도영
작성일: 2024-07-16
버전: 1.0
"""
from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class T1441INBLOCK(StockApiBaseModel):
	gubun1 : str # 구분 0:전체 1:코스피 2:코스닥
	gubun2 : str # 상승하락 0: 상승률 1: 하락률 2: 보합
	gubun3 : str # 당일전일 0: 당일 1: 전일
	jc_num : int = 0x00400000 | 0x00800000 | 0x00200000 | 0x00000080 |0x00000100 | 0x00000200 | 0x00004000 | 0x04000000 | 0x01000000 | 0x80000000
	# 대상제외 대상제외값 증거금50 : 0x00400000 증거금100 : 0x00800000 증거금50/100 : 0x00200000 관리종목 : 0x00000080 시장경보 : 0x00000100 거래정지 : 0x00000200 우선주 : 0x00004000 투자유의 : 0x04000000 정리매매 : 0x01000000 불성실공시 : 0x80000000
	sprice : int = 0 # 시작가격 현재가 >= sprice
	eprice : int = 0 # 종료가격 현재가 <= eprice
	volume : int = 0 # 거래량 거래량 >= volume
	idx : int  = 0# IDX 처음 조회시는 Space 연속 조회시에 이전 조회한 OutBlock의 idx 값으로 설정
	jc_num2 : int = 0 # 대상제외2 기본 => 000000000000 상장지수펀드 => 000000000001 선박투자회사 => 000000000002 스펙 => 000000000004 ETN => 000000000008(0x00000008) 투자주의 => 000000000016(0x00000010) 투자위험 => 000000000032(0x00000020) 위험예고 => 000000000064(0x00000040) 담보불가 => 000000000128(0x00000080) 두개 이상 제외시 해당 값을 합산한다.
	

class T1441_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	t1441InBlock : T1441INBLOCK

class T1441OUTBLOCK(StockApiBaseModel):
	idx: int # IDX 

class T1441OUTBLOCK1(StockApiBaseModel):
    hname: Optional[str] = None # 한글명 
    price: Optional[int] = None # 현재가 
    sign: Optional[str] = None # 전일대비구분 1:상한/2:상승/3:보합/4:하한/5:하락/6:기세상한/7:기세상승/8:기세하한/9:기세하락	
    change: Optional[int] = None # 전일대비 
    diff: Optional[float] = None # 등락율 
    volume: Optional[int] = None # 누적거래량 
    offerrem1: Optional[int] = None # 매도잔량 
    offerho1: Optional[int] = None # 매도호가 
    bidho1: Optional[int] = None # 매수호가 
    bidrem1: Optional[int] = None # 매수잔량 
    updaycnt: Optional[int] = None # 연속 
    jnildiff: Optional[float] = None # 전일등락율 
    shcode: Optional[str] = None # 종목코드 
    open: Optional[int] = None # 시가 
    high: Optional[int] = None # 고가 
    low: Optional[int] = None # 저가 
    voldiff: Optional[float] = None # 거래량대비율 
    value: Optional[int] = None # 거래대금 
    total: Optional[int] = None # 시가총액

class T1441_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	t1441OutBlock: T1441OUTBLOCK
	t1441OutBlock1: List[T1441OUTBLOCK1]