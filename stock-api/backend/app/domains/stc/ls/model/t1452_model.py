# t1452_model.py
"""
모듈 설명: 
    - 상위종목: 거래량
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-07-16
버전: 1.0
"""
from typing import Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

#요청모델 데이터
class T1452INBLOCK(StockApiBaseModel):
	gubun : str # 구분 0:전체 1:코스피 2:코스닥
	jnilgubun : str # 전일구분 1:당일 2:전일
	sdiff : int # 시작등락율 현재등락율 >= sdiff
	ediff : int # 종료등락율 현재등락율 <= ediff
	jc_num : int # 대상제외 대상제외값 (0x00000080)관리종목 => 000000000128 (0x00000100)시장경보 => 000000000256 (0x00000200)거래정지 => 000000000512 (0x00004000)우선주 => 000000016384 (0x00200000)증거금50 => 000008388608 (0x01000000)정리매매 => 000016777216 (0x04000000)투자유의 => 000067108864 (0x80000000)불성실공시 => -02147483648 두개 이상 제외시 해당 값을 합산한다 예)관리종목 + 시장경보 = 000000000128 + 000000000256 = 000000000384
	sprice : int # 시작가격 현재가 >= sprice
	eprice : int # 종료가격 현재가 <= eprice
	volume : int # 거래량 거래량 >= volume
	idx : int # IDX 처음 조회시는 Space 연속 조회시에 이전 조회한 OutBlock의 idx 값으로 설정
	
class T1452_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	t1452InBlock : T1452INBLOCK 

class T1452OUTBLOCK(StockApiBaseModel):
	idx: int # IDX 

class T1452OUTBLOCK1(StockApiBaseModel):
	hname: str # 종목명 
	price: int # 현재가 
	sign: str # 전일대비구분 
	change: int # 전일대비 
	diff: float # 등락율 
	volume: int # 누적거래량 
	vol: float # 회전율 
	jnilvolume: int # 전일거래량 
	bef_diff: float # 전일비 
	shcode: str # 종목코드 

class T1452_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	t1452OutBlock: T1452OUTBLOCK
	t1452OutBlock1: T1452OUTBLOCK1
