# kis_interface_model.py
"""
모듈 설명: 
    -   설명을 넣으시오
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-07-14
버전: 1.0
"""

from backend.app.domains.stock_api_base_model import StockApiBaseModel


class DailyCcld_Request(StockApiBaseModel):
    ''' 주식일별주문체결 '''
    start_ymd: str
    end_ymd: str