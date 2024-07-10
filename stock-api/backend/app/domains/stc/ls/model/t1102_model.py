# t1102_model.py
"""
모듈 설명: 
    - LS 현재가 모델

작성자: 김도영
작성일: 2024-07-08
버전: 1.0
"""

from typing import Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel


class T1102OUTBLOCK(StockApiBaseModel):
	hname: str # 한글명 
	price: int # 현재가 
	sign: str # 전일대비구분 
	change: int # 전일대비 
	diff: float # 등락율 
	volume: int # 누적거래량 
	recprice: int # 기준가(평가가격) 
	avg: int # 가중평균 
	uplmtprice: int # 상한가(최고호가가격) 
	dnlmtprice: int # 하한가(최저호가가격) 
	jnilvolume: int # 전일거래량 
	volumediff: int # 거래량차 
	open: int # 시가 
	opentime: str # 시가시간 
	high: int # 고가 
	hightime: str # 고가시간 
	low: int # 저가 
	lowtime: str # 저가시간 
	high52w: int # 52최고가 
	high52wdate: str # 52최고가일 
	low52w: int # 52최저가 
	low52wdate: str # 52최저가일 
	exhratio: float # 소진율 
	per: float # PER 
	pbrx: float # PBRX 
	listing: int # 상장주식수(천) 
	jkrate: int # 증거금율 
	memedan: str # 수량단위 
	offernocd1: str # 매도증권사코드1 
	bidnocd1: str # 매수증권사코드1 
	offerno1: str # 매도증권사명1 
	bidno1: str # 매수증권사명1 
	dvol1: int # 총매도수량1 
	svol1: int # 총매수수량1 
	dcha1: int # 매도증감1 
	scha1: int # 매수증감1 
	ddiff1: float # 매도비율1 
	sdiff1: float # 매수비율1 
	offernocd2: str # 매도증권사코드2 
	bidnocd2: str # 매수증권사코드2 
	offerno2: str # 매도증권사명2 
	bidno2: str # 매수증권사명2 
	dvol2: int # 총매도수량2 
	svol2: int # 총매수수량2 
	dcha2: int # 매도증감2 
	scha2: int # 매수증감2 
	ddiff2: float # 매도비율2 
	sdiff2: float # 매수비율2 
	offernocd3: str # 매도증권사코드3 
	bidnocd3: str # 매수증권사코드3 
	offerno3: str # 매도증권사명3 
	bidno3: str # 매수증권사명3 
	dvol3: int # 총매도수량3 
	svol3: int # 총매수수량3 
	dcha3: int # 매도증감3 
	scha3: int # 매수증감3 
	ddiff3: float # 매도비율3 
	sdiff3: float # 매수비율3 
	offernocd4: str # 매도증권사코드4 
	bidnocd4: str # 매수증권사코드4 
	offerno4: str # 매도증권사명4 
	bidno4: str # 매수증권사명4 
	dvol4: int # 총매도수량4 
	svol4: int # 총매수수량4 
	dcha4: int # 매도증감4 
	scha4: int # 매수증감4 
	ddiff4: float # 매도비율4 
	sdiff4: float # 매수비율4 
	offernocd5: str # 매도증권사코드5 
	bidnocd5: str # 매수증권사코드5 
	offerno5: str # 매도증권사명5 
	bidno5: str # 매수증권사명5 
	dvol5: int # 총매도수량5 
	svol5: int # 총매수수량5 
	dcha5: int # 매도증감5 
	scha5: int # 매수증감5 
	ddiff5: float # 매도비율5 
	sdiff5: float # 매수비율5 
	fwdvl: int # 외국계매도합계수량 
	ftradmdcha: int # 외국계매도직전대비 
	ftradmddiff: float # 외국계매도비율 
	fwsvl: int # 외국계매수합계수량 
	ftradmscha: int # 외국계매수직전대비 
	ftradmsdiff: float # 외국계매수비율 
	vol: float # 회전율 
	shcode: str # 단축코드 
	value: int # 누적거래대금 
	jvolume: int # 전일동시간거래량 
	highyear: int # 연중최고가 
	highyeardate: str # 연중최고일자 
	lowyear: int # 연중최저가 
	lowyeardate: str # 연중최저일자 
	target: int # 목표가 
	capital: int # 자본금 
	abscnt: int # 유동주식수 
	parprice: int # 액면가 
	gsmm: str # 결산월 
	subprice: int # 대용가 
	total: int # 시가총액 
	listdate: str # 상장일 
	name: str # 전분기명 
	bfsales: int # 전분기매출액 
	bfoperatingincome: int # 전분기영업이익 
	bfordinaryincome: int # 전분기경상이익 
	bfnetincome: int # 전분기순이익 
	bfeps: float # 전분기EPS 
	name2: str # 전전분기명 
	bfsales2: int # 전전분기매출액 
	bfoperatingincome2: int # 전전분기영업이익 
	bfordinaryincome2: int # 전전분기경상이익 
	bfnetincome2: int # 전전분기순이익 
	bfeps2: float # 전전분기EPS 
	salert: float # 전년대비매출액 
	opert: float # 전년대비영업이익 
	ordrt: float # 전년대비경상이익 
	netrt: float # 전년대비순이익 
	epsrt: float # 전년대비EPS 
	info1: str # 락구분 
	info2: str # 관리/급등구분 
	info3: str # 정지/연장구분 
	info4: str # 투자/불성실구분 
	janginfo: str # 장구분 
	t_per: float # T.PER 
	tonghwa: str # 통화ISO코드 
	dval1: int # 총매도대금1 
	sval1: int # 총매수대금1 
	dval2: int # 총매도대금2 
	sval2: int # 총매수대금2 
	dval3: int # 총매도대금3 
	sval3: int # 총매수대금3 
	dval4: int # 총매도대금4 
	sval4: int # 총매수대금4 
	dval5: int # 총매도대금5 
	sval5: int # 총매수대금5 
	davg1: int # 총매도평단가1 
	savg1: int # 총매수평단가1 
	davg2: int # 총매도평단가2 
	savg2: int # 총매수평단가2 
	davg3: int # 총매도평단가3 
	savg3: int # 총매수평단가3 
	davg4: int # 총매도평단가4 
	savg4: int # 총매수평단가4 
	davg5: int # 총매도평단가5 
	savg5: int # 총매수평단가5 
	ftradmdval: int # 외국계매도대금 
	ftradmsval: int # 외국계매수대금 
	ftradmdvag: int # 외국계매도평단가 
	ftradmsvag: int # 외국계매수평단가 
	info5: str # 투자주의환기 
	spac_gubun: str # 기업인수목적회사여부 
	issueprice: int # 발행가격 
	alloc_gubun: str # 배분적용구분코드(1:배분발생2:배분해제그외:미발생) 
	alloc_text: str # 배분적용구분 
	shterm_text: str # 단기과열/VI발동 
	svi_uplmtprice: int # 정적VI상한가 
	svi_dnlmtprice: int # 정적VI하한가 
	low_lqdt_gu: str # 저유동성종목여부 
	abnormal_rise_gu: str # 이상급등종목여부 
	lend_text: str # 대차불가표시 
	ty_text: str # ETF/ETN투자유의 


class T1102_Response(StockApiBaseModel):
	''' t1102: 현재가 결과'''
	rsp_cd: str
	rsp_msg: str
	t1102OutBlock: Optional[T1102OUTBLOCK] = None


class T1102_Request(StockApiBaseModel):
	''' t1102: 현재가 요청'''
	stk_code: str
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''