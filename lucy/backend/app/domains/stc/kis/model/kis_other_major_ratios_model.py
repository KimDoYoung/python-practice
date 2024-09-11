# kis_other_major_ratios_model.py
"""
모듈 설명: 
    - 수익성 모델

작성자: 김도영
작성일: 2024-09-11
버전: 1.0
"""
from typing import List
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class OtherMajorRatios_Request(StockApiBaseModel):
    fid_input_iscd: str # 입력 종목코드 000660 : 종목코드
    fid_div_cls_code: str = '1' # 분류 구분 코드 0: 년, 1: 분기
    fid_cond_mrkt_div_code: str = 'J' # 조건 시장 분류 코드 J
    
class OtherMajorRatiosItem(StockApiBaseModel):
    stac_yymm: str # 결산 년월 
    payout_rate: str # 배당 성향 비정상 출력되는 데이터로 무시
    eva: str # EVA 
    ebitda: str # EBITDA 
    ev_ebitda: str # EV_EBITDA 


class OtherMajorRatios_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: List[OtherMajorRatiosItem]