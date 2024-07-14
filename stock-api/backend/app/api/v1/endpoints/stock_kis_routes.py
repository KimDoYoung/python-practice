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

from backend.app.domains.stc.kis.model.kis_inquire_balance_model import KisInquireBalance_Response
from backend.app.domains.stc.kis.model.kis_inquire_price import InquirePrice_Response
from backend.app.domains.stc.kis.model.kis_order_cash_model import OrderCash_Request, KisOrderCash_Response
from backend.app.domains.stc.kis.model.kis_psearch_result_model import PsearchResult_Response
from backend.app.domains.stc.kis.model.kis_psearch_title_model import PsearchTitle_Result
from backend.app.domains.stc.kis.model.kis_search_stock_info_model import SearchStockInfo_Response
from backend.app.domains.stc.kis_interface_model import DailyCcld_Request
from backend.app.domains.user.user_service import UserService
from backend.app.managers.client_ws_manager import ClientWsManager
from backend.app.managers.stock_api_manager import StockApiManager
from backend.app.core.dependency import get_user_service
from backend.app.managers.stock_ws_manager import StockWsManager
from backend.app.core.logger import get_logger
from backend.app.utils.kis_model_util import daily_ccld_to_inquire_daily_ccld

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
    kis_api = await api_manager.stock_api(user_id, acctno, 'KIS')
    response = kis_api.current_cost(stk_code)
    logger.info(f"current_cost 응답: {response}")
    return response

@router.post("/order/{user_id}/{acctno}",response_model=KisOrderCash_Response)
async def order(user_id:str, acctno:str, order_request: OrderCash_Request):
    ''' 매도/매수 현금주문'''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno,'KIS')
    
    order_cash_response = kis_api.order(order_request)
    return order_cash_response

@router.get("/stock-info/{user_id}/{acctno}/{stk_code}",response_model=SearchStockInfo_Response)
async def search_stock_info(user_id:str, acctno:str, stk_code:str):
    ''' 상품정보 '''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno,'KIS')
    
    response = kis_api.search_stock_info(stk_code)
    return response

@router.get("/inquire-balance/{user_id}/{acctno}",response_model=KisInquireBalance_Response)
async def inquire_balance(user_id:str, acctno:str):
    ''' 주식 잔고 조회 '''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno,'KIS')
    
    response = kis_api.inquire_balance()
    return response

@router.get("/psearch-title/{user_id}/{acctno}",response_model=PsearchTitle_Result)
async def psearch_title(user_id:str, acctno:str):
    ''' 조건식 목록 조회 '''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno,'KIS')
    
    response = kis_api.psearch_title()
    return response

@router.get("/psearch-result/{user_id}/{acctno}/{seq}",response_model=PsearchResult_Response)
async def psearch_reulst(user_id:str, acctno:str, seq:str):
    ''' 조건식 결과 리스트 '''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno,'KIS')
    
    response = kis_api.psearch_result(seq)
    return response

@router.post("/inquire-daily-ccld/{user_id}/{acctno}",response_model=InquireDailyCcld_Response)
async def inquire_daily_ccld(user_id:str, acctno:str, daily_ccld: DailyCcld_Request ):
    '''주식일별주문체결조회 '''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno, 'KIS')
    inquire_daily_ccld_req = daily_ccld_to_inquire_daily_ccld(daily_ccld)
    response = kis_api.inquire_daily_ccld(inquire_daily_ccld_req)
    return response