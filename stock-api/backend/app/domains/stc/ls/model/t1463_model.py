# t1463_model.py
"""
모듈 설명: 
    - 거래대금상위

작성자: 김도영
작성일: 2024-07-17
버전: 1.0
"""
from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel
class T1463INBLOCK(StockApiBaseModel):
	gubun : str # 구분 0 : 전체 1 : 코스피 2 : 코스닥
	jnilgubun : str # 전일구분 0 : 당일 1 : 전일
	jc_num : int # 대상제외 대상제외값 (0x00000080)관리종목 => 000000000128 (0x00000100)시장경보 => 000000000256 (0x00000200)거래정지 => 000000000512 (0x00004000)우선주 => 000000016384 (0x00200000)증거금50 => 000008388608 (0x01000000)정리매매 => 000016777216 (0x04000000)투자유의 => 000067108864 (0x80000000)불성실공시 => -02147483648 두개 이상 제외시 해당 값을 합산한다 예)관리종목 + 시장경보 = 000000000128 + 000000000256 = 000000000384
	sprice : int # 시작가격 현재가 >= sprice
	eprice : int # 종료가격 현재가 <= eprice
	volume : int # 거래량 거래량 >= volume
	idx : int # IDX 처음 조회시는 Space 연속 조회시에 이전 조회한 OutBlock의 idx 값으로 설정
	jc_num2 : int # 대상제외2 기본 => 000000000000 상장지수펀드 => 000000000001 선박투자회사 => 000000000002 스펙 => 000000000004 ETN => 000000000008(0x00000008) 투자주의 => 000000000016(0x00000010) 투자위험 => 000000000032(0x00000020) 위험예고 => 000000000064(0x00000040) 담보불가 => 000000000128(0x00000080) 두개 이상 제외시 해당 값을 합산한다.
	
#요청모델 데이터
class T1463_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'Y'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	t1463InBlock : T1463INBLOCK

class T1463OUTBLOCK(StockApiBaseModel):
	idx: int # IDX 

class T1463OUTBLOCK1(StockApiBaseModel):
	hname: str # 한글명 
	price: int # 현재가 
	sign: str # 전일대비구분 
	change: int # 전일대비 
	diff: float # 등락율 
	volume: int # 누적거래량 
	value: int # 거래대금 
	jnilvalue: int # 전일거래대금 
	bef_diff: float # 전일비 
	shcode: str # 종목코드 
	filler: str # filler 
	jnilvolume: int # 전일거래량 

class T1463_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	t1463OutBlock: T1463OUTBLOCK
	t1463OutBlock1: List[T1463OUTBLOCK1]
