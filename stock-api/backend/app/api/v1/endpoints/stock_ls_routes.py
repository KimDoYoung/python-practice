# stock_ls_routes.py
"""
모듈 설명: 
    - LS등 증권사의 API
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 04
버전: 1.0
"""
from fastapi import APIRouter, Depends
from backend.app.core.dependency import get_user_service
from backend.app.domains.stc.interface_model import AcctHistory_Request, CancelOrder_Request, Fulfill_Request, ModifyOrder_Request, Order_Request
from backend.app.domains.stc.ls.model.cdpcq04700_model import CDPCQ04700_Response
from backend.app.domains.stc.ls.model.cspat00601_model import CSPAT00601_Response
from backend.app.domains.stc.ls.model.cspat00701_model import CSPAT00701_Response
from backend.app.domains.stc.ls.model.cspat00801_model import CSPAT00801_Response
from backend.app.domains.stc.ls.model.t1102_model import T1102_Request, T1102_Response
from backend.app.domains.user.user_service import UserService
from backend.app.managers.stock_api_manager import StockApiManager
from backend.app.core.logger import get_logger
from backend.app.utils.model_util import acct_history_to_CDPCQ04700_Request, cancel_order_to_cspat00801_Request, order_to_cspat00601_Request, modify_order_to_cspat00701_Request

logger = get_logger(__name__)

# APIRouter 인스턴스 생성
router = APIRouter()

@router.get("/current-cost/{user_id}/{acctno}/{stk_code}",response_model=T1102_Response)
async def current_cost(user_id:str, acctno:str, stk_code:str, user_service:UserService = Depends(get_user_service) ):
    ''' 현재가 '''
    logger.info(f"current_cost: {user_id}, {acctno}, {stk_code}")
    api_manager = StockApiManager(user_service)
    ls_api = await api_manager.stock_api(user_id, acctno,'LS')
    
    req = T1102_Request(stk_code=stk_code)

    t1102_response = await ls_api.current_cost(req)
    logger.info(f"current_cost: {t1102_response}")
    return t1102_response

@router.post("/order/{user_id}/{acctno}",response_model=CSPAT00601_Response)
async def order_cash(user_id:str, acctno:str, req:Order_Request, user_service:UserService = Depends(get_user_service) ):
    ''' 현물주문 '''
    
    api_manager = StockApiManager(user_service)
    ls_api = await api_manager.stock_api(user_id, acctno,'LS')

    cspat00601_Request = order_to_cspat00601_Request(req)

    response = await ls_api.order(cspat00601_Request)
    return response

@router.post("/modify-order/{user_id}/{acctno}",response_model=CSPAT00701_Response)
async def modify_order(user_id:str, acctno:str, req:ModifyOrder_Request, user_service:UserService = Depends(get_user_service) ):
    ''' 현물정정주문 '''
    api_manager = StockApiManager(user_service)
    ls_api = await api_manager.stock_api(user_id, acctno,'LS')
    capat00701_req = modify_order_to_cspat00701_Request(req)
    response = await ls_api.modify_cash(capat00701_req)
    logger.debug(f"modify_order 응답: [{response.to_str()}]")
    return response

@router.post("/cancel-order/{user_id}/{acctno}",response_model=CSPAT00801_Response)
async def cancel_order(user_id:str, acctno:str, req:CancelOrder_Request, user_service:UserService = Depends(get_user_service) ):
    ''' 현물주문취소 '''
    api_manager = StockApiManager(user_service)
    ls_api = await api_manager.stock_api(user_id, acctno,'LS')
    capat00801_req = cancel_order_to_cspat00801_Request(req)
    response = await ls_api.cancel_cash(capat00801_req)
    logger.debug(f"cancel_order 응답: [{response.to_str()}]")
    return response

@router.post("/acct-history/{user_id}/{acctno}",response_model=CDPCQ04700_Response)
async def acct_history(user_id:str, acctno:str, req:AcctHistory_Request, user_service:UserService = Depends(get_user_service) ):
    ''' 계좌 주문내역 '''
    api_manager = StockApiManager(user_service)
    ls_api = await api_manager.stock_api(user_id, acctno,'LS')
    
    CDPCQ04700_Req = acct_history_to_CDPCQ04700_Request(req)
    
    response = await ls_api.acct_history(CDPCQ04700_Req)

    logger.debug(f"acct_history 응답: [{response.to_str()}]")
    return response    

@router.post("/fulfill-list/{user_id}/{acctno}",response_model=T0425_Response)
async def fulfill_list(user_id:str, acctno:str, req:Fulfill_Request, user_service:UserService = Depends(get_user_service) ):
    ''' 체결/미체결내역 '''
    api_manager = StockApiManager(user_service)
    ls_api = await api_manager.stock_api(user_id, acctno,'LS')
    
    t042_Req = fulfill_to_t0425_Request(req)
    
    response = await ls_api.fulfill_list(t042_Req)

    logger.debug(f"acct_history 응답: [{response.to_str()}]")
    return response    
