# kis_stability_ratio_model.py
"""
모듈 설명: 
    - 안정성 비율 모델
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-09-11
버전: 1.0
"""
from typing import List
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class StabilityRatio_Request(StockApiBaseModel):
    fid_input_iscd: str # 입력 종목코드 000660 : 종목코드
    fid_div_cls_code: str # 분류 구분 코드 0: 년, 1: 분기
    fid_cond_mrkt_div_code: str # 조건 시장 분류 코드 J

class StabilityRatioItem(StockApiBaseModel):
    stac_yymm: str # 결산 년월 
    lblt_rate: str # 부채 비율 
    bram_depn: str # 차입금 의존도 
    crnt_rate: str # 유동 비율 
    quck_rate: str # 당좌 비율 


class StabilityRatio_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: List[StabilityRatioItem]