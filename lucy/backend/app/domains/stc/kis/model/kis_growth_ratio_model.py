# kis_growth_ratio_model.py
"""
모듈 설명: 
    - 성장성 모델

작성자: 김도영
작성일: 2024-09-11
버전: 1.0
"""

from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class GrowthRatio_Request(StockApiBaseModel):
    fid_input_iscd: str # 입력 종목코드 ex : 000660
    fid_div_cls_code: str = '1' # 분류 구분 코드 0: 년, 1: 분기
    fid_cond_mrkt_div_code: str = 'J' # 조건 시장 분류 코드 시장구분코드 (주식 J)

class GrowthRatioItem(StockApiBaseModel):
    stac_yymm: Optional[str] = None  # 결산 년월
    grs: Optional[str] = None  # 매출액 증가율
    bsop_prfi_inrt: Optional[str] = None  # 영업 이익 증가율
    equt_inrt: Optional[str] = None  # 자기자본 증가율
    totl_aset_inrt: Optional[str] = None  # 총자산 증가율

class GrowthRatio_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: List[GrowthRatioItem]