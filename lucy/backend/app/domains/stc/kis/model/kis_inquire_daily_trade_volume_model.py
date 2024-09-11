# kis_inquire_daily_trade_volume_model.py
"""
모듈 설명: 
    - 종목별일별매수매도체결량

작성자: 김도영
작성일: 2024-09-11
버전: 1.0
"""
from typing import List
from backend.app.domains.stock_api_base_model import StockApiBaseModel
class InquireDailyTradeVolume_Request(StockApiBaseModel):
    FID_COND_MRKT_DIV_CODE: str = 'J' # FID 조건 시장 분류 코드 J
    FID_INPUT_ISCD: str # FID 입력 종목코드 005930
    FID_INPUT_DATE_1: str # FID 입력 날짜1 from
    FID_INPUT_DATE_2: str # FID 입력 날짜2 to
    FID_PERIOD_DIV_CODE: str = 'D' # FID 기간 분류 코드 D

class InquireDailyTradeVolume(StockApiBaseModel):
    shnu_cnqn_smtn: str # 매수 체결량 합계
    seln_cnqn_smtn: str # 매도 체결량 합계

class InquireDailyTradeVolumeItem(StockApiBaseModel):
    stck_bsop_date: str # 주식 영업 일자 
    total_seln_qty: str # 총 매도 수량 
    total_shnu_qty: str # 총 매수 수량 


class InquireDailyTradeVolume_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output1: InquireDailyTradeVolume
    output2: List[InquireDailyTradeVolumeItem]