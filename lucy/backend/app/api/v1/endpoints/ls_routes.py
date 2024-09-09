# ls_routes.py
"""
모듈 설명: 
    - LS증권 API를 사용하는 API를 정의한다.
주요 기능:
    - /notice/start: websocket으로 Notice 연결 시작
    - /notice/stop: websocket으로 Notice 연결 종료
    - /current-cost/{stk_code}: 현재가
    - /order: 현물주문
    - /modify-order: 현물정정주문
    - /cancel-order: 현물주문취소
    - /acct-history: 계좌 주문내역
    - /fulfill-list: 체결/미체결내역
    - /fulfill-api-list: 현물계좌 주문체결내역 조회(API)
    - /master-api: [주식] 시세-주식마스터조회API용
    - /multi-current-cost: [주식] 시세-API용주식멀티현재가조회
    - /jango2: [주식] 계좌-주식잔고2
    - /bep_danga: [주식] 계좌-BEP단가조회
    - /rank/range: [주식] 상위종목 : 등락률
    - /rank/volumn: [주식] 상위종목-거래량상위
    - /rank/rapidup: [주식] 상위종목-전일동시간대비거래급증
    - /rank/timeout-range: [주식] 상위종목-시간외등락율상위
    - /rank/timeout-volume: [주식] 상위종목-시간외거래량상위
    - /rank/expect-fulfill: [주식] 상위종목-예상체결량상위조회
    - /rank/expect-danilga-range: [주식] 상위종목-단일가예상등락율
    - /rank/purchase-cost: [주식] 상위종목-거래대금상위
    

작성자: 김도영
작성일: 2024-07-19
버전: 1.0
"""
import asyncio
from fastapi import APIRouter
from backend.app.domains.stc.ls.model.cdpcq04700_model import CDPCQ04700_Response
from backend.app.domains.stc.ls.model.cspaq12300_model import CSPAQ12300_Request, CSPAQ12300_Response, CSPAQ12300InBlock1
from backend.app.domains.stc.ls.model.cspaq13700_model import CSPAQ13700_Response
from backend.app.domains.stc.ls.model.cspaq22200_model import CSPAQ22200_Request, CSPAQ22200_Response, CSPAQ22200InBlock1
from backend.app.domains.stc.ls.model.cspat00601_model import CSPAT00601_Response
from backend.app.domains.stc.ls.model.cspat00701_model import CSPAT00701_Response
from backend.app.domains.stc.ls.model.cspat00801_model import CSPAT00801_Response
from backend.app.domains.stc.ls.model.t0424_model import T0424INBLOCK, T0424_Request, T0424_Response
from backend.app.domains.stc.ls.model.t0425_model import T0425_Response
from backend.app.domains.stc.ls.model.t1102_model import T1102_Request, T1102_Response
from backend.app.domains.stc.ls.model.t1441_model import T1441_Response
from backend.app.domains.stc.ls.model.t1452_model import T1452_Response
from backend.app.domains.stc.ls.model.t1463_model import T1463_Response
from backend.app.domains.stc.ls.model.t1466_model import T1466_Response
from backend.app.domains.stc.ls.model.t1481_model import T1481_Response
from backend.app.domains.stc.ls.model.t1482_model import T1482_Response
from backend.app.domains.stc.ls.model.t1489_model import T1489_Response
from backend.app.domains.stc.ls.model.t1492_model import T1492_Response
from backend.app.domains.stc.ls.model.t8407_model import ArrayStkCodes, T8407_Request, T8407_Response, T8407InBLOCK
from backend.app.domains.stc.ls.model.t9945_model import T9945_Response
from backend.app.domains.stc.ls_interface_model import AcctHistory_Request, CancelOrder_Request, Fulfill_Api_Request, Fulfill_Request, HighItem_Request, ModifyOrder_Request, Order_Request

from backend.app.core.logger import get_logger
from backend.app.managers.client_ws_manager import ClientWsManager
from backend.app.managers.stock_api_manager import StockApiManager
from backend.app.managers.stock_ws_manager import StockWsManager
from backend.app.utils.ls_model_util import acct_history_to_CDPCQ04700_Request, cancel_order_to_cspat00801_Request, fulfill_api_to_cspaq13700_Request, fulfill_to_t0425_Request, high_item_to_T1441_Request, high_item_to_T1452_Request, high_item_to_T1463_Request, high_item_to_T1466_Request, high_item_to_T1481_Request, high_item_to_T1482_Request, high_item_to_T1489_Request, high_item_to_T1492_Request, modify_order_to_cspat00701_Request, order_to_cspat00601_Request
from backend.app.core.dependency import get_stkinfo_service
from backend.app.utils.naver_util import get_name_by_code

logger = get_logger(__name__)

# APIRouter 인스턴스 생성
router = APIRouter()

@router.get("/notice/start")
async def news_start(user_id:str, acctno:str):
    ''' websocket으로 Notice 연결 시작 '''
    client_ws_manager = ClientWsManager()

    stock_ws_manager = StockWsManager(client_ws_manager)
    if stock_ws_manager.is_connected(user_id, acctno):
        return {"code":"01", "detail": f"{user_id}, {acctno} 이미 연결되어 있습니다."}
    
    result = await stock_ws_manager.connect(user_id, acctno)
    return result

@router.get("/notice/stop")
async def news_stop(user_id:str, acctno:str):
    ''' websocket으로 Notice 연결 종료 '''
    client_ws_manager = ClientWsManager()
    stock_ws_manager = StockWsManager(client_ws_manager)
    if stock_ws_manager.is_connected(user_id, acctno):
        result = await stock_ws_manager.disconnect(user_id, acctno)
    else:
        result = {"code":"01", "detail": f"{user_id}, {acctno} 연결되어 있지 않습니다."}
    return result

@router.get("/current-cost/{stk_code}",response_model=T1102_Response)
async def current_cost(stk_code:str ):
    ''' 현재가 '''
    logger.info(f"current_cost 요청:  {stk_code}")
    ls_api = await StockApiManager().stock_api('LS')
    
    req = T1102_Request(stk_code=stk_code)

    t1102_response = await ls_api.current_cost(req)
    logger.info(f"current_cost: {t1102_response}")
    return t1102_response

@router.post("/order",response_model=CSPAT00601_Response)
async def order_cash(req:Order_Request):
    ''' 현물주문 '''
    
    cspat00601_Request = order_to_cspat00601_Request(req)
    
    ls_api = await StockApiManager().stock_api('LS')
    response = await ls_api.order(cspat00601_Request)

    return response

@router.post("/modify-order",response_model=CSPAT00701_Response)
async def modify_order(req:ModifyOrder_Request):
    ''' 현물정정주문 '''
    ls_api = await StockApiManager().stock_api('LS')
    capat00701_req = modify_order_to_cspat00701_Request(req)
    response = await ls_api.modify_cash(capat00701_req)
    logger.debug(f"modify_order 응답: [{response.to_str()}]")
    return response

@router.post("/cancel-order",response_model=CSPAT00801_Response)
async def cancel_order(req:CancelOrder_Request):
    ''' 현물주문취소 '''
    ls_api = await StockApiManager().stock_api('LS')
    capat00801_req = cancel_order_to_cspat00801_Request(req)
    response = await ls_api.cancel_cash(capat00801_req)
    logger.debug(f"cancel_order 응답: [{response.to_str()}]")
    return response

@router.post("/acct-history",response_model=CDPCQ04700_Response)
async def acct_history(req:AcctHistory_Request):
    ''' 계좌 주문내역 '''
    ls_api = await StockApiManager().stock_api('LS')
    
    CDPCQ04700_Req = acct_history_to_CDPCQ04700_Request(req)
    
    response = await ls_api.acct_history(CDPCQ04700_Req)

    logger.debug(f"acct_history 응답: [{response.to_str()}]")
    return response    

@router.post("/fulfill-list",response_model=T0425_Response)
async def fulfill_list(req:Fulfill_Request):
    ''' 체결/미체결내역 '''
    ls_api = await StockApiManager().stock_api('LS')
    
    t042_Req = fulfill_to_t0425_Request(req)
    
    response = await ls_api.fulfill_list(t042_Req)
    
    if response.t0425OutBlock1 is  None:
        return response
    
    list = response.t0425OutBlock1
    # hname 종목명을 채운다.
    stk_info_service = get_stkinfo_service()
    for item in list:
        stkinfo =  await stk_info_service.get_by_stk_code(item.expcode)
        item.hname = ""
        if stkinfo is not None:
            item.hname = stkinfo.stk_name
        else:
            item.hname = get_name_by_code(item.expcode)

    logger.debug(f"fulfill-list 응답: [{response.to_str()}]")
    return response    

@router.post("/fulfill-api-list",response_model=CSPAQ13700_Response)
async def fulfill_api_list(req:Fulfill_Api_Request,):
    ''' 현물계좌 주문체결내역 조회(API) '''
    ls_api = await StockApiManager().stock_api('LS')
    
    cspaq13700_req = fulfill_api_to_cspaq13700_Request(req)
    logger.debug(f"fulfill-api-list 요청: [{cspaq13700_req.to_str()}]")
    response = await ls_api.fulfill_api_list(cspaq13700_req)

    logger.debug(f"fulfill-api-list 응답: [{response.to_str()}]")
    return response

@router.get("/master-api",response_model=T9945_Response)
async def master_api():
    ''' [주식] 시세-주식마스터조회API용 '''
    ls_api = await StockApiManager().stock_api('LS')
    
    response = await ls_api.master_api("1") # 1 코스피, 2 코스닥

    logger.debug(f"master_api 응답: [{response.to_str()}]")
    return response

@router.post("/multi-current-cost",response_model=T8407_Response)
async def multi_current_cost(array_stk_codes: ArrayStkCodes):
    ''' [주식] 시세-API용주식멀티현재가조회 '''
    ls_api = await StockApiManager().stock_api('LS')
    length =  len(array_stk_codes.stk_codes)
    stk_code_str = ''.join(array_stk_codes.stk_codes)
    inBlock = T8407InBLOCK(nrec=length, shcode=stk_code_str)
    req_data = T8407_Request(t8407InBlock=inBlock) 
    response = await ls_api.multi_current_cost(req_data)

    logger.debug(f"multi-current-cost 응답: [{response.to_str()}]")
    return response

@router.get("/jango2",response_model=T0424_Response)
async def jango2():
    ''' [주식] 계좌-주식잔고2 '''
    ls_api = await StockApiManager().stock_api('LS')
    req = T0424_Request(t0424InBlock=T0424INBLOCK())
    response = await ls_api.jango2(req)

    logger.debug(f"jango2 응답: [{response.to_str()}]")
    return response

@router.get("/bep_danga",response_model=CSPAQ12300_Response)
async def bep_danga(user_id:str, acctno:str):
    '''[주식] 계좌-BEP단가조회'''
    ls_api = await StockApiManager().stock_api('LS')
    req = CSPAQ12300_Request(CSPAQ12300InBlock1=CSPAQ12300InBlock1())
    response = await ls_api.bep_danga(req)

    logger.debug(f"bep_danga 응답: [{response.to_str()}]")
    return response

@router.get("/order-possible-money",response_model=CSPAQ22200_Response)
async def order_possible_money():
    '''[주식] 계좌-현물계좌예수금 주문가능금액 총평가2 '''
    ls_api = await StockApiManager().stock_api('LS')
    req = CSPAQ22200_Request(CSPAQ22200InBlock1=CSPAQ22200InBlock1())
    response = await ls_api.order_possible_money(req)

    logger.debug(f"bep_danga 응답: [{response.to_str()}]")
    return response


#--------------------------------------------------------------------------------------
# 상위랭크 route
#--------------------------------------------------------------------------------------
@router.post("/rank/range",response_model=T1441_Response)
async def rank_range(user_req:HighItem_Request):
    '''[주식] 상위종목 : 등락률'''
    ls_api = await StockApiManager().stock_api('LS')
    t1441_req = high_item_to_T1441_Request(user_req)
    list = []
    for i in range(1):
        response = await ls_api.rank_range(t1441_req)
        await asyncio.sleep(1)
        list.extend(response.t1441OutBlock1)
        t1441_req.t1441InBlock.idx = response.t1441OutBlock.idx
    # 필터링과 정렬
    filtered_sorted_list = sorted(
        [item for item in list if item.diff is not None and item.diff > 3.0],
        key=lambda x: x.diff,
        reverse=True
    )    
    final_response = T1441_Response(rsp_cd="0000",
                                    rsp_msg="정상처리",
                                    t1441OutBlock=response.t1441OutBlock,
                                    t1441OutBlock1=filtered_sorted_list[0:30])
    logger.debug(f"rank 응답: [{list}]")
    return final_response

@router.post("/rank/volumn",response_model=T1452_Response)
async def rank_volumn(req:HighItem_Request):
    '''[주식] 상위종목-거래량상위'''
    ls_api = await StockApiManager().stock_api('LS')

    t1452_req = high_item_to_T1452_Request(req) 
    list = []
    for i in range(1):
        response = await ls_api.rank_volumn(t1452_req)
        list.extend(response.t1452OutBlock1)
        if t1452_req.t1452InBlock.idx == response.t1452OutBlock.idx:
            break
        t1452_req.t1452InBlock.idx = response.t1452OutBlock.idx
        await asyncio.sleep(1)
    #필터링과 정렬
    # filtered_sorted_list = sorted(
    #     [item for item in list if item.diff is not None and item.diff >= 0.0],
    #     key=lambda x: x.bef_diff,
    #     reverse=True
    # )

    final_response = T1452_Response(rsp_cd="0000",
                                    rsp_msg="정상처리",
                                    t1452OutBlock=response.t1452OutBlock,
                                    t1452OutBlock1=list)
    logger.debug(f"rank 응답: [{list}]")
    return final_response

@router.post("/rank/rapidup",response_model=T1466_Response)
async def rank_rapidup(req:HighItem_Request):
    '''[주식] 상위종목-전일동시간대비거래급증 '''
    ls_api = await StockApiManager().stock_api('LS')
    t1466_req = high_item_to_T1466_Request(req) 
    list = []
    for i in range(1):
        response = await ls_api.rank_rapidup(t1466_req)
        list.extend(response.t1466OutBlock1)
        if t1466_req.t1466InBlock.idx == response.t1466OutBlock.idx:
            break
        t1466_req.t1466InBlock.idx = response.t1466OutBlock.idx
        await asyncio.sleep(1)
    # 필터링과 정렬
    # filtered_sorted_list = sorted(
    #     [item for item in list if item.voldiff is not None and item.voldiff > 3.0],
    #     key=lambda x: x.volume,
    #     reverse=True)
    final_response = T1466_Response(rsp_cd="0000",
                                    rsp_msg="정상처리",
                                    t1466OutBlock=response.t1466OutBlock,
                                    t1466OutBlock1=list)
    return final_response

@router.post("/rank/timeout-range",response_model=T1481_Response)
async def rank_timeout_range(req:HighItem_Request):
    '''[주식] 상위종목-시간외등락율상위 '''
    ls_api = await StockApiManager().stock_api('LS')
    t1481_req = high_item_to_T1481_Request(req)
    list = []
    for i in range(1):
        response = await ls_api.rank_timeout_range(t1481_req)
        list.extend(response.t1481OutBlock1)
        t1481_req.t1481InBlock.idx = response.t1481OutBlock.idx
        await asyncio.sleep(1)
    # 필터링과 정렬
    # filtered_sorted_list = sorted(
    #     [item for item in list if item.diff is not None and item.diff > 3.0],
    #     key=lambda x: x.offerrem1,
    #     reverse=True
    # )
    final_response = T1481_Response(rsp_cd="0000",
                                    rsp_msg="정상처리",
                                    t1481OutBlock=response.t1481OutBlock,
                                    t1481OutBlock1=list)
    return final_response

@router.post("/rank/timeout-volume",response_model=T1482_Response)
async def rank_timeout_volume(req:HighItem_Request):
    '''[주식] 상위종목-시간외거래량상위 '''
    ls_api = await StockApiManager().stock_api('LS')
    t1482_req = high_item_to_T1482_Request(req)
    list = []
    for i in range(1):
        response = await ls_api.rank_timeout_volume(t1482_req)
        list.extend(response.t1482OutBlock1)
        t1482_req.t1482InBlock.idx = response.t1482OutBlock.idx
        await asyncio.sleep(1)
    # 필터링과 정렬
    # filtered_sorted_list = sorted(
    #     [item for item in list if item.diff is not None and item.diff > 3.0],
    #     key=lambda x: x.volume,
    #     reverse=True
    # )
    final_response = T1482_Response(rsp_cd="0000",
                                    rsp_msg="정상처리",
                                    t1482OutBlock=response.t1482OutBlock,
                                    t1482OutBlock1=list)
    return final_response

@router.post("/rank/expect-fulfill",response_model=T1489_Response)
async def rank_expect_filfull(req:HighItem_Request):
    '''[주식]  상위종목-예상체결량상위조회 '''
    ls_api = await StockApiManager().stock_api('LS')
    t1489_req = high_item_to_T1489_Request(req) 
    list = []
    for i in range(1):
        response = await ls_api.rank_expect_filfull(t1489_req)
        await asyncio.sleep(1)
        list.extend(response.t1489OutBlock1)
        t1489_req.t1489InBlock.idx = response.t1489OutBlock.idx
    # 필터링과 정렬
    # filtered_sorted_list = sorted(
    #     [item for item in list if item.diff is not None and item.diff > 3.0],
    #     key=lambda x: x.volume,
    #     reverse=True
    # )
    final_response = T1489_Response(rsp_cd="0000",
                                    rsp_msg="정상처리",
                                    t1489OutBlock=response.t1489OutBlock,
                                    t1489OutBlock1=list)
    return final_response

@router.post("/rank/expect-danilga-range",response_model=T1492_Response)
async def rank_expect_danilga_range(req:HighItem_Request):
    '''[주식]  상위종목-단일가예상등락율 '''
    ls_api = await StockApiManager().stock_api('LS')
    t1492_req = high_item_to_T1492_Request(req) 
    list = []
    for i in range(1):
        response = await ls_api.rank_expect_danilga_range(t1492_req)
        list.extend(response.t1492OutBlock1)
        t1492_req.t1492InBlock.idx = response.t1492OutBlock.idx
        await asyncio.sleep(1)
    # 필터링과 정렬
    filtered_sorted_list = sorted(
        [item for item in list if item.diff is not None and item.diff > 3.0],
        key=lambda x: x.change,
        reverse=True
    )
    response = await ls_api.rank_expect_danilga_range(t1492_req)
    final_response = T1492_Response(rsp_cd="0000",
                                    rsp_msg="정상처리",
                                    t1492OutBlock=response.t1492OutBlock,
                                    t1492OutBlock1=filtered_sorted_list[0:30])
    return final_response

@router.post("/rank/purchase-cost",response_model=T1463_Response)
async def rank_purchase_cost(req:HighItem_Request):
    '''[주식]  상위종목-거래대금상위 '''
    ls_api = await StockApiManager().stock_api('LS')
    t1463_req = high_item_to_T1463_Request(req) 
    list = []
    for i in range(1):
        response = await ls_api.rank_purchase_cost(t1463_req)
        await asyncio.sleep(1)
        list.extend(response.t1463OutBlock1)
        t1463_req.t1463InBlock.idx = response.t1463OutBlock.idx
    # 필터링과 정렬
    filtered_sorted_list = sorted(
        [item for item in list if item.diff is not None and item.diff > 3.0],
        key=lambda x: x.volume,
        reverse=True
    )
    final_response = T1463_Response(rsp_cd="0000",
                                    rsp_msg="정상처리",
                                    t1463OutBlock=response.t1463OutBlock,
                                    t1463OutBlock1=filtered_sorted_list[0:30])
    #logger.debug(f"rank 응답: [{list}]")
    return final_response