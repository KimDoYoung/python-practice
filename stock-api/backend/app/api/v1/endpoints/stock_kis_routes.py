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

from backend.app.domains.stc.kis.model.kis_after_hour_balance_model import AfterHourBalance_Request, AfterHourBalance_Response
from backend.app.domains.stc.kis.model.kis_chk_holiday_model import ChkWorkingDay_Response
from backend.app.domains.stc.kis.model.kis_inquire_balance_model import KisInquireBalance_Response
from backend.app.domains.stc.kis.model.kis_inquire_daily_ccld_model import InquireDailyCcld_Response
from backend.app.domains.stc.kis.model.kis_inquire_price import InquirePrice_Response
from backend.app.domains.stc.kis.model.kis_inquire_psbl_rvsecncl_model import InquirePsblRvsecncl_Response
from backend.app.domains.stc.kis.model.kis_inquire_psbl_sell_model import InquirePsblSell_Response
from backend.app.domains.stc.kis.model.kis_inquire_psble_order import InquirePsblOrder_Response
from backend.app.domains.stc.kis.model.kis_order_cash_model import KisOrderCancel_Response, OrderCash_Request, KisOrderCash_Response
from backend.app.domains.stc.kis.model.kis_psearch_result_model import PsearchResult_Response
from backend.app.domains.stc.kis.model.kis_psearch_title_model import PsearchTitle_Result
from backend.app.domains.stc.kis.model.kis_quote_balance_model import QuoteBalance_Request, QuoteBalance_Response
from backend.app.domains.stc.kis.model.kis_search_stock_info_model import SearchStockInfo_Response
from backend.app.domains.stc.kis_interface_model import Buy_Max_Request, DailyCcld_Request, Modify_Order_Request, Rank_Request
from backend.app.domains.user.user_service import UserService
from backend.app.managers.client_ws_manager import ClientWsManager
from backend.app.managers.stock_api_manager import StockApiManager
from backend.app.core.dependency import get_user_service
from backend.app.managers.stock_ws_manager import StockWsManager
from backend.app.core.logger import get_logger
from backend.app.utils.kis_model_util import buy_max_to_InquirePsblOrder_Request, daily_ccld_to_inquire_daily_ccld, modify_order_to_kisOrderRvsecncl_request, rank_to_after_hour_balance_request, rank_to_quote_balance_request
from backend.app.utils.misc_util import only_number

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

@router.get("/order-cancel/{user_id}/{acctno}/{org_ord_no}",response_model=KisOrderCancel_Response)
async def order_cancel(user_id:str, acctno:str, org_ord_no:str):
    ''' 주문 취소'''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno,'KIS')
    resp = kis_api.order_cancel(org_ord_no)
    return resp

@router.post("/order-modify/{user_id}/{acctno}/{org_ord_no}",response_model=KisOrderCancel_Response)
async def order_modify(user_id:str, acctno:str, org_ord_no:str, user_req: Modify_Order_Request):
    ''' 주문 정정'''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno,'KIS')
    req = modify_order_to_kisOrderRvsecncl_request(user_req)
    resp = kis_api.order_modify(req)
    return resp

@router.get("/order-modify-qty/{user_id}/{acctno}",response_model=InquirePsblRvsecncl_Response)
async def order_modify(user_id:str, acctno:str):
    ''' 주문 정정 가능수량 조회'''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno,'KIS')
    resp = kis_api.inquire_psbl_rvsecncl()
    return resp


@router.post("/buy-max-qty/{user_id}/{acctno}",response_model=InquirePsblOrder_Response)
async def buy_max_qty(user_id:str, acctno:str, user_req:Buy_Max_Request):
    ''' 매수가능수량 조회'''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno,'KIS')
    req = buy_max_to_InquirePsblOrder_Request(user_req)
    resp = kis_api.inquire_psbl_order(req)
    return resp

@router.get("/sell-max-qty/{user_id}/{acctno}/{stk_code}",response_model=InquirePsblSell_Response)
async def sell_max_qty(user_id:str, acctno:str, stk_code:str):
    ''' 매도가능수량 조회'''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno,'KIS')
    resp = kis_api.inquire_psbl_sell(stk_code)
    return resp

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
    # 모델변환
    inquire_daily_ccld_req = daily_ccld_to_inquire_daily_ccld(daily_ccld)
    response = kis_api.inquire_daily_ccld(inquire_daily_ccld_req)
    return response

@router.get("/chk-workingday/{user_id}/{acctno}/{ymd}",response_model=ChkWorkingDay_Response)
async def chk_workingday(user_id:str, acctno:str, ymd:str ):
    ''' 휴장일 '''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno, 'KIS')
    ymd = only_number(ymd)
    response = kis_api.chk_workingday(ymd)
    return response

@router.get("/quote-balance/{user_id}/{acctno}",response_model=QuoteBalance_Response)
async def quote_balance(user_id:str, acctno:str, rank_req: Rank_Request):
    ''' 호가잔량순위 '''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno, 'KIS')
    qb_req = rank_to_quote_balance_request(rank_req)
    response = kis_api.quote_balance(qb_req)
    return response

@router.get("/after-hour-balance/{user_id}/{acctno}",response_model=AfterHourBalance_Response)
async def after_hour_balance(user_id:str, acctno:str, rank_req: Rank_Request):
    ''' 시간외호가잔량순위 '''
    api_manager = StockApiManager()
    kis_api = await api_manager.stock_api(user_id, acctno, 'KIS')
    ahb_req = rank_to_after_hour_balance_request(rank_req)
    response = kis_api.after_hour_balance(ahb_req)
    return response