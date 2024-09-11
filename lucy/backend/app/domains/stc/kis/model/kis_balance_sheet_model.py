# kis_balance_sheet_model.py
"""
모듈 설명: 
    - 대차대조표 모델
작성자: 김도영
작성일: 2024-09-11
버전: 1.0
"""
from typing import List

from backend.app.domains.stock_api_base_model import StockApiBaseModel


class BalanceSheet_Request(StockApiBaseModel):
    FID_DIV_CLS_CODE: str = '1' # 분류 구분 코드 0: 년, 1: 분기
    fid_cond_mrkt_div_code: str = 'J' # 조건 시장 분류 코드 J
    fid_input_iscd: str # 입력 종목코드 000660 : 종목코드

class BalanceSheetItem(StockApiBaseModel):
    stac_yymm: str # 결산 년월 
    cras: str # 유동자산 
    fxas: str # 고정자산 
    total_aset: str # 자산총계 
    flow_lblt: str # 유동부채 
    fix_lblt: str # 고정부채 
    total_lblt: str # 부채총계 
    cpfn: str # 자본금 
    cfp_surp: str # 자본 잉여금 출력되지 않는 데이터(99.99 로 표시)
    prfi_surp: str # 이익 잉여금 출력되지 않는 데이터(99.99 로 표시)
    total_cptl: str # 자본총계 


class BalanceSheet_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: List[BalanceSheetItem]