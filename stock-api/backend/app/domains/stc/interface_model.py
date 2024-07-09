# common_model.py
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
from typing import Literal
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class Order_Request(StockApiBaseModel):
    ''' 주문 요청 '''
    buy_sell_gb: Literal['매수', '매도']
    user_id: str # 사용자 ID
    acctno: str # 계좌번호
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