# t1466_model.py
"""
모듈 설명: 
    -  상위종목-전일동시간대비거래급증

작성자: 김도영
작성일: 2024-07-16
버전: 1.0
"""
from typing import Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

#요청모델 데이터
class T1466INBLOCK(StockApiBaseModel):
	gubun : str # 구분 0 : 전체 1 : 코스피 2 : 코스닥
	type1 : str # 전일거래량 0@1주 이상 1@1만주 이상 2@5만주 이상 3@10만주 이상 4@20만주 이상 5@50만주 이상 6@100만주 이상
	type2 : str # 거래급등율 0@전체 1@2000%이하 2@1500%이하 3@1000%이하 4@500%이하 5@100%이하 6@50%이하
	jc_num : int # 대상제외 대상제외값 (0x00000080)관리종목 => 000000000128 (0x00000100)시장경보 => 000000000256 (0x00000200)거래정지 => 000000000512 (0x00004000)우선주 => 000000016384 (0x00200000)증거금50 => 000008388608 (0x01000000)정리매매 => 000016777216 (0x04000000)투자유의 => 000067108864 (0x80000000)불성실공시 => -02147483648 두개 이상 제외시 해당 값을 합산한다 예)관리종목 + 시장경보 = 000000000128 + 000000000256 = 000000000384
	sprice : int # 시작가격 현재가 >= sprice
	eprice : int # 종료가격 현재가 <= eprice
	volume : int # 거래량 거래량 >= volume
	idx : int # IDX 처음 조회시는 Space 연속 조회시에 이전 조회한 OutBlock의 idx 값으로 설정
	jc_num2 : int # 대상제외2 기본 => 000000000000 상장지수펀드 => 000000000001 선박투자회사 => 000000000002 스펙 => 000000000004 ETN => 000000000008(0x00000008) 투자주의 => 000000000016(0x00000010) 투자위험 => 000000000032(0x00000020) 위험예고 => 000000000064(0x00000040) 담보불가 => 000000000128(0x00000080) 두개 이상 제외시 해당 값을 합산한다.

class T1466_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	t1466InBlock :  T1466INBLOCK 

class T1466OUTBLOCK(StockApiBaseModel):
	hhmm: str # 현재시분 
	idx: int # IDX 

class T1466OUTBLOCK1(StockApiBaseModel):
	shcode: str # 종목코드 
	hname: str # 종목명 
	price: int # 현재가 
	sign: str # 전일대비구분 
	change: int # 전일대비 
	diff: float # 등락율 
	stdvolume: int # 전일거래량 
	volume: int # 당일거래량 
	voldiff: float # 거래급등율 
	open: int # 시가 
	high: int # 고가 
	low: int # 저가 

class T1466_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	t1466OutBlock: T1466OUTBLOCK
	t1466OutBlock1: T1466OUTBLOCK1