# kis_profit_ratio_model.py
"""
모듈 설명: 
    - 수익성 비율 모델

작성자: 김도영
작성일: 2024-09-11
버전: 1.0
"""
from typing import List
from backend.app.domains.stock_api_base_model import StockApiBaseModel


class ProfitRatio_Request(StockApiBaseModel):
    fid_input_iscd: str # 입력 종목코드 000660 : 종목코드
    FID_DIV_CLS_CODE: str = '1' # 분류 구분 코드 0: 년, 1: 분기
    fid_cond_mrkt_div_code: str = 'J' # 조건 시장 분류 코드 J

class ProfitRatioItem(StockApiBaseModel):
    stac_yymm: str # 결산 년월 
    cptl_ntin_rate: str # 총자본 순이익율 
    self_cptl_ntin_inrt: str # 자기자본 순이익율 
    sale_ntin_rate: str # 매출액 순이익율 
    sale_totl_rate: str # 매출액 총이익율 


class ProfitRatio_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: List[ProfitRatioItem]