# kis_income_statement_model.py
"""
모듈 설명: 
    - 손익계산서 모델

작성자: 김도영
작성일: 2024-09-11
버전: 1.0
"""
from typing import List
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class IncomeStatement_Request(StockApiBaseModel):
    FID_DIV_CLS_CODE: str = '1' # 분류 구분 코드 0: 년, 1: 분기 ※ 분기데이터는 연단위 누적합산
    fid_cond_mrkt_div_code: str = 'J' # 조건 시장 분류 코드 J
    fid_input_iscd: str # 입력 종목코드 000660 : 종목코드

class IncomeStatementItem(StockApiBaseModel):
    stac_yymm: str # 결산 년월 
    sale_account: str # 매출액 
    sale_cost: str # 매출 원가 
    sale_totl_prfi: str # 매출 총 이익 
    depr_cost: str # 감가상각비 출력되지 않는 데이터(99.99 로 표시)
    sell_mang: str # 판매 및 관리비 출력되지 않는 데이터(99.99 로 표시)
    bsop_prti: str # 영업 이익 
    bsop_non_ernn: str # 영업 외 수익 출력되지 않는 데이터(99.99 로 표시)
    bsop_non_expn: str # 영업 외 비용 출력되지 않는 데이터(99.99 로 표시)
    op_prfi: str # 경상 이익 
    spec_prfi: str # 특별 이익 
    spec_loss: str # 특별 손실 
    thtr_ntin: str # 당기순이익 

class IncomeStatement_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: List[IncomeStatementItem]