# stock_kis_routes.py
"""
모듈 설명: 
    - KIS 한국투자증권의 API
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 04
버전: 1.0
"""
from fastapi import APIRouter, Depends

from backend.app.domains.stc.kis.model.kis_order_cash_model import KisOrderCashRequest, KisOrderCashResponse
from backend.app.domains.user.user_service import UserService
from backend.app.managers.stock_api_manager import StockApiManager
from backend.app.core.dependency import get_user_service
#from backend.app.core.globals import api_manager

# APIRouter 인스턴스 생성
router = APIRouter()

@router.post("/order-cash/{user_id}/{acctno}",response_model=KisOrderCashResponse)
async def order_cash(user_id:str, acctno:str, order_cash_request: KisOrderCashRequest, user_service:UserService = Depends(get_user_service) ):
    ''' 매도/매수 주문'''
    raise ValueError("이것은 잘못된 데이터입니다.")
    api_manager = StockApiManager(user_service)
    kis_api = await api_manager.stock_api(user_id, acctno,'KIS')
    # kis_api = StockApiManager(user_service).stock_api(user_id, acctno,'KIS')
    
    order_cash_response = kis_api.order_cash(order_cash_request)
    return order_cash_response
