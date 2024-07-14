# kis_model_util.py
"""
모듈 설명: 
    - KIS interface model -> api model로 변경하는 유틸리티
주요 기능:

작성자: 김도영
작성일: 2024-07-14
버전: 1.0
"""

from backend.app.domains.stc.kis.model.kis_inquire_daily_ccld_model import InquireDailyCcld_Request
from backend.app.domains.stc.kis_interface_model import DailyCcld_Request


def daily_ccld_to_inquire_daily_ccld(daily_ccld: DailyCcld_Request ) -> InquireDailyCcld_Request :
    ''' 주식일별주문체결조회 DailyCcld_Request -> InquireDailyCcld_Request '''
    req = InquireDailyCcld_Request(start_ymd=daily_ccld.start_ymd, end_ymd=daily_ccld.end_ymd)
    return req