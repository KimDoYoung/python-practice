# kist_financial_ratio_model.py
"""
모듈 설명: 
    - 재무비율 모델

작성자: 김도영
작성일: 2024-09-11
버전: 1.0
"""
from typing import List
from backend.app.domains.stock_api_base_model import StockApiBaseModel
class FinancialRatio_Request(StockApiBaseModel):
    FID_DIV_CLS_CODE: str = '1' # 분류 구분 코드 0: 년, 1: 분기
    fid_cond_mrkt_div_code: str = 'J' # 조건 시장 분류 코드 J
    fid_input_iscd: str # 입력 종목코드 000660 : 종목코드

class FinancialRatioItem(StockApiBaseModel):
    stac_yymm: str # 결산 년월 
    grs: str # 매출액 증가율 
    bsop_prfi_inrt: str # 영업 이익 증가율 적자지속, 흑자전환, 적자전환인 경우 0으로 표시
    ntin_inrt: str # 순이익 증가율 
    roe_val: str # ROE 값 
    eps: str # EPS 
    sps: str # 주당매출액 
    bps: str # BPS 
    rsrv_rate: str # 유보 비율 
    lblt_rate: str # 부채 비율 

class FinancialRatio_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: List[FinancialRatioItem]