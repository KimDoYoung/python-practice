# ls_interface_model.py
"""
모듈 설명: 
    - 여러 증권사(KIS,LS)에 공통으로 사용할 모델 
    - 주로 Request를 통일시키기 위한 목적의 모델들
주요 기능:
    - StockApiBaseModel을 상속받아서 사용한다.

작성자: 김도영
작성일: 2024-07-08
버전: 1.0
"""
from typing import Literal, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class Order_Request(StockApiBaseModel):
    ''' 주문 요청 '''
    buy_sell_gb: Literal['매수', '매도']
    user_id: Optional[str]='' # 사용자 ID
    acctno: Optional[str]='' # 계좌번호
    stk_code: str
    qty: int
    cost: int = 0 # cost가 0이면 시장가로 주문

class ModifyOrder_Request(StockApiBaseModel):
    ''' 주문 수정 요청 '''
    org_ord_no: int # 원주문번호
    stk_code: str
    qty: int
    cost: int = 0 # cost가 0이면 시장가로 주문

class CancelOrder_Request(StockApiBaseModel):
    ''' 주문 취소 요청 '''
    org_ord_no :str
    stk_code:str
    qty: int

class AcctHistory_Request(StockApiBaseModel):
    ''' 계좌별 거래내역 조회 요청 '''
    acctno: str
    from_ymd: str
    to_ymd: str
    stk_code: str = ''
    start_no: int = 0

class Fulfill_Request(StockApiBaseModel):
    ''' 체결/미체결 조회 요청 '''
    stk_code: str
    fullfill_type: Literal['전체', '체결', '미체결']
    buy_sell_gb: Literal['전체', '매수', '매도']

class Fulfill_Api_Request(StockApiBaseModel):
    '''현물계좌 주문체결내역 조회(API) 요청'''
    market_gb: Literal['전체', '거래소', '코스닥', '프리보드']
    buy_sell_gb: Literal['전체', '매수', '매도']
    stk_code: str
    fullfill_type: Literal['전체', '체결', '미체결']
    order_dt: str
    ord_ptn_code: Literal['전체', '매도전체', '매수전체', '현금매도', '현금매수'] #, '저축매도', '저축매수', '상품매도', '상품매수', '융자매도', '융자매수', '대주매도', '대주매수', '선물대용매도', '현금매도(프)', '현금매수(프)', '대출', '대출상환']


class HighItem_Request(StockApiBaseModel):
    ''' 상위종목 조회 요청 '''
    market_gb: Literal['전체', '코스피', '코스닥']
    updown_gb: Literal['상승', '하락', '보합']
    yester_or_today: Literal['전일', '금일']
    idx: int = 0
    