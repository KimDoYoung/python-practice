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

from backend.app.domains.stc.kis.model.kis_inquire_price import InquirePrice_Response
from backend.app.domains.stc.kis.model.kis_order_cash_model import KisOrderCashRequest, KisOrderCashResponse
from backend.app.domains.user.user_service import UserService
from backend.app.managers.client_ws_manager import ClientWsManager
from backend.app.managers.stock_api_manager import StockApiManager
from backend.app.core.dependency import get_user_service
from backend.app.managers.stock_ws_manager import StockWsManager
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

# APIRouter 인스턴스 생성
router = APIRouter()

@router.get("/notice/start/{user_id}/{acctno}")
async def notice_start(user_id:str, acctno:str, user_service:UserService = Depends(get_user_service) ):
    ''' KIS 체결통보 연결 시작-실시간으로 체결결과를 Websockect으로 통보요청'''
    client_ws_manager = ClientWsManager()

    stock_ws_manager = StockWsManager(client_ws_manager)
    if stock_ws_manager.is_connected(user_id, acctno):
        return {"code":"01", "detail": f"{user_id}, {acctno} 이미 연결되어 있습니다."}
    
    result = await stock_ws_manager.connect(user_id, acctno)
    return result

@router.get("/notice/stop/{user_id}/{acctno}")
async def notice_stop(user_id:str, acctno:str, user_service:UserService = Depends(get_user_service) ):
    ''' KIS 체결통보 연결 시작-실시간으로 체결결과를 Websockect으로 통보해제 '''
    client_ws_manager = ClientWsManager()
    stock_ws_manager = StockWsManager(client_ws_manager)

    if stock_ws_manager.is_connected(user_id, acctno):
        result = await stock_ws_manager.disconnect(user_id, acctno)
    else:
        result = {"code":"01", "detail": f"{user_id}, {acctno} 연결되어 있지 않습니다."}
    return result

@router.get("/current-cost/{user_id}/{acctno}/{stk_code}",response_model=InquirePrice_Response)
async def current_cost(user_id:str, acctno:str, stk_code:str):
    ''' 현재가 '''
    logger.info(f"current_cost 요청: {user_id}, {acctno}, {stk_code}")
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno,'KIS')
    response = kis_api.current_cost(stk_code)
    logger.info(f"current_cost 응답: {response}")
    return response

@router.post("/order-cash/{user_id}/{acctno}",response_model=KisOrderCashResponse)
async def order_cash(user_id:str, acctno:str, order_cash_request: KisOrderCashRequest):
    ''' 매도/매수 주문'''
    # raise StockApiException("이것은 잘못된 데이터입니다.")
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno,'KIS')
    # kis_api = StockApiManager(user_service).stock_api(user_id, acctno,'KIS')
    
    order_cash_response = kis_api.order(order_cash_request)
    return order_cash_response
