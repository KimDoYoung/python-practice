# kis_routes.py
"""
모듈 설명: 
    -  KIS 한국투자증권 API를 사용하는 API를 정의한다.
주요 기능:
    - token : KIS_ACCESS_TOKEN_EXPIRE_EXCECPTION이 발생하면 새로 token을 발급받아서 User DB에 저장한다.
    - / : 주식잔고조회, 보유주식을 mystock에 등록
    - /order-cash : 주식매수, 주식매도 주문
    - /order-cancel : 주식매수, 주식매도 취소
    - /stock-info/{stk_code} : 주식정보 조회
    - /psearch/title : 조건식 타이틀 조회
    - /psearch/result/{seq} : 조건식 결과 조회
    - /inquire-daily-ccld : 주식일별주문체결조회

작성자: 김도영
작성일: 2024-06-16
버전: 1.0
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from backend.app.core.dependency import get_mystock_service, get_user_service
# from backend.app.domains.stc.kis.kis_api import KoreaInvestmentApi
from backend.app.domains.stc.kis.model.kis_after_hour_balance_model import AfterHourBalance_Response
from backend.app.domains.stc.kis.model.kis_inquire_daily_ccld_model import InquireDailyCcld_Request
from backend.app.domains.stc.kis.model.kis_order_cash_model import KisOrderCancel_Request, OrderCash_Request
from backend.app.domains.stc.kis.model.kis_quote_balance_model import QuoteBalance_Response
from backend.app.domains.stc.kis_interface_model import Rank_Request
from backend.app.domains.system.mystock_model import MyStockDto
from backend.app.domains.user.user_service import UserService

from backend.app.core.logger import get_logger
from backend.app.core.security import get_current_user
from backend.app.managers.stock_api_manager import StockApiManager
from backend.app.utils.kis_model_util import rank_to_after_hour_balance_request, rank_to_quote_balance_request

logger = get_logger(__name__)

# APIRouter 인스턴스 생성
router = APIRouter()

async def validate_user(request: Request, user_service: UserService):
    current_user = await get_current_user(request)
    logger.debug(f"current_user : {current_user}")
    user_id = current_user.get('user_id')
    user = await user_service.get_1(user_id)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token-사용자 정보가 없습니다")
    
    return user

# async def get_kis_api(request: Request, user_service: UserService) -> KoreaInvestmentApi:
#     ''' 
#         토큰이 유효한지 체크해서 유효하지 않으면 새로 발급받아서 User DB에 저장한다. 
#         그런 후 KoreaInvestmentApi 인스턴스를 반환한다.
#     '''
#     user = await validate_user(request, user_service)
#     kis_api = KoreaInvestmentApi(user)
    
#     try:
#         cost = kis_api.get_current_price("005930") # 삼성전자
#         logger.debug(f"현재 ACCESS_TOKEN OK, 삼성전자 현재가 : {cost}")
#         return  kis_api
#     except KisAccessTokenExpireException as e:
#         logger.warning(f"현재 ACCESS_TOKEN은  만료되었습니다.")
#         new_access_token=await kis_api.set_access_token_from_kis()
#         logger.debug(f"새로운 ACCESS_TOKEN을 발급받음: [{new_access_token}]")
#         return kis_api
#     except KisAccessTokenInvalidException as e:
#         logger.error(f"현재 ACCESS_TOKEN이 유효하지 않습니다.")
#         new_access_token=await kis_api.set_access_token_from_kis()
#         return kis_api

@router.get("/", response_class=JSONResponse, response_model=None)
async def info(request:Request, user_service :UserService=Depends(get_user_service)):
    '''1.주식잔고조회, 2. 보유주식을 mystock에 등록'''

    kis_api = await StockApiManager().kis_api()

    kis_inquire_balance =  kis_api.inquire_balance()
    mystock_service = get_mystock_service()
    output1 = kis_inquire_balance.output1
    for item in output1:
        stk_code = item.pdno
        stk_name = item.prdt_name
        if '스팩' in stk_name:
            continue
        stk_types = ['보유']
        mystock_dto = MyStockDto(stk_code=stk_code, stk_name=stk_name, stk_types=stk_types)
        await mystock_service.upsert(mystock_dto)

    logger.debug(f"주식잔고 조회 : {kis_inquire_balance}")
    return kis_inquire_balance


@router.get("/current-cost/{stk_cost}", response_class=JSONResponse)
async def current_cost(request:Request, stk_cost:str, user_service :UserService=Depends(get_user_service)):
    ''' 
        현재가 조회
    '''
    kis_api = await StockApiManager().kis_api()
    cost = kis_api.get_current_price(stk_cost) # 삼성전자
    logger.debug(f"{stk_cost} 현재가 : {cost}")
    return {"cost": cost}



@router.post("/order-cash", response_class=JSONResponse)
async def order_cash(request:Request, order_cash: OrderCash_Request, user_service :UserService=Depends(get_user_service)):
    '''주식매수, 주식매도 주문'''
    
    kis_api = await StockApiManager().kis_api()
    kis_order_cash =   kis_api.order(order_cash)
    if order_cash.buy_sell_gb == "매수":
        logger.debug(f"주식매수 : {kis_order_cash}")
    else:
        logger.debug(f"주식매도 : {kis_order_cash}")
    return kis_order_cash

@router.post("/order-cancel", response_class=JSONResponse)
async def order_cancel(request:Request, order_cancel: KisOrderCancel_Request, user_service :UserService=Depends(get_user_service)):
    '''주식매수, 주식매도 취소'''
    kis_api = await StockApiManager().kis_api()
    cancel_response =   kis_api.order_cancel(order_cancel)
    logger.debug(f"주식매수,매도 취소 : {cancel_response.to_str()}")
    return cancel_response

@router.get("/stock-info/{stk_code}", response_class=JSONResponse)
async def stock_info(request:Request, stk_code:str,  user_service :UserService=Depends(get_user_service)):
    '''주식정보 조회'''
    kis_api = await StockApiManager().kis_api()
    kis_stock_info = kis_api.search_stock_info(stk_code)
    return kis_stock_info

@router.get("/psearch/title", response_class=JSONResponse)
async def psearch_title(request:Request, user_service :UserService=Depends(get_user_service)):
    '''조건식 타이틀 조회'''    
    kis_api = await StockApiManager().kis_api()
    kis_psearch_title = kis_api.psearch_title()
    return kis_psearch_title

@router.get("/psearch/result/{seq}", response_class=JSONResponse)
async def psearch_result(request:Request,  seq:str, user_service :UserService=Depends(get_user_service)):
    '''seq에 해당하는 조건식 조회 '''
    kis_api = await StockApiManager().kis_api()
    kis_psearch_result = kis_api.psearch_result(seq)
    return kis_psearch_result


@router.post("/inquire-daily-ccld", response_class=JSONResponse)
async def inquire_daily_ccld(request:Request, ccld: InquireDailyCcld_Request, user_service :UserService=Depends(get_user_service)):
    '''주식일별주문체결조회 '''
    kis_api = await StockApiManager().kis_api()
    ccld_result = kis_api.inquire_daily_ccld(inquire_daily_ccld=ccld)
    logger.debug("주식일별주문체결조회:["+ccld_result.to_str()+"]")
    return ccld_result

@router.post("/rank/quote-balance",response_model=QuoteBalance_Response)
async def quote_balance(rank_req: Rank_Request):
    ''' 호가잔량순위 '''
    kis_api = await StockApiManager().kis_api()
    qb_req = rank_to_quote_balance_request(rank_req)
    response = kis_api.quote_balance(qb_req)
    return response

@router.post("/rank/after-hour-balance",response_model=AfterHourBalance_Response)
async def after_hour_balance(rank_req: Rank_Request):
    ''' 시간외호가잔량순위 '''
    kis_api = await StockApiManager().kis_api()
    ahb_req = rank_to_after_hour_balance_request(rank_req)
    response = kis_api.after_hour_balance(ahb_req)
    return response
