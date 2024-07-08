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
from backend.app.domains.stc.ls.model.cspat00601_model import CSPAT00601_Request, CSPAT00601_Response
from backend.app.domains.stc.ls.model.cspat00701_model import CSPAT00701_Request, CSPAT00701_Response
from backend.app.domains.stc.ls.model.cspat00801_model import CSPAT00801_Request, CSPAT00801_Response
from backend.app.domains.stc.ls.model.t1102_model import T1102_Request, T1102_Response
from backend.app.domains.user.user_service import UserService
from backend.app.managers.stock_api_manager import StockApiManager
from backend.app.core.logger import get_logger

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

@router.get("/order-cash/{user_id}/{acctno}",response_model=CSPAT00601_Response)
async def order_cash(user_id:str, acctno:str, req:CSPAT00601_Request, user_service:UserService = Depends(get_user_service) ):
    ''' 현물주문 '''
    
    api_manager = StockApiManager(user_service)
    ls_api = await api_manager.stock_api(user_id, acctno,'LS')

    response = await ls_api.order_cash(req)
    return response

@router.get("/modify-cash/{user_id}/{acctno}",response_model=CSPAT00701_Response)
async def modify_cash(user_id:str, acctno:str, req:CSPAT00701_Request, user_service:UserService = Depends(get_user_service) ):
    ''' 현물정정주문 '''
    api_manager = StockApiManager(user_service)
    ls_api = await api_manager.stock_api(user_id, acctno,'LS')
    
    

    response = await ls_api.modify_cash(req)
    return response

@router.get("/modify-cash/{user_id}/{acctno}",response_model=CSPAT00801_Response)
async def cancel_cash(user_id:str, acctno:str, req:CSPAT00801_Request, user_service:UserService = Depends(get_user_service) ):
    ''' 현물정정주문 '''
    api_manager = StockApiManager(user_service)
    ls_api = await api_manager.stock_api(user_id, acctno,'LS')
    
    req = CSPAT00801_Request(stk_code=stk_code)

    response = await ls_api.cancel_cash(req)
    return response