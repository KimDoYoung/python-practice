# client_websocket_routes.py
"""
모듈 설명: 
    - client(browser)와 서버간의 웹소켓 통신을 위한 라우터
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 18
버전: 1.0
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.app.managers.client_ws_manager import ClientWsManager
from backend.app.core.config import config
from backend.app.core.logger import get_logger
from backend.app.managers.stock_ws_manager import StockWsManager
from backend.app.core.dependency import get_user_service
logger = get_logger(__name__)

router = APIRouter()
#clients: List[WebSocket] = []

# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     clients.append(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await broadcast_message("서버로부터의 메세지:" + data)
#     except Exception as e:
#         print(f"Client disconnected: {e}")
#     finally:
#         clients.remove(websocket)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):        
    client_ws_manager = ClientWsManager()
    user_id = config.DEFAULT_USER_ID
    await client_ws_manager.connect(websocket, user_id)
    logger.debug(f"User {user_id} client 웹소켓 연결됨")
    
    # KIS 증권사에 연결한다
    user_service = get_user_service()
    user_id = config.DEFAULT_USER_ID
    user = await user_service.get_1(user_id)
    
    #KIS  WebSocket 연결
    account = user.find_account_by_abbr('KIS')
    kis_acctno = account.account_no
    client_ws_manager = ClientWsManager()
    stock_ws_manager = StockWsManager(client_ws_manager)
    # if not stock_ws_manager.is_connected(user_id, kis_acctno):   
    result = await stock_ws_manager.connect(user_id, kis_acctno)
    client_ws_manager.broadcast(str(result))
    logger.info(f"User {user_id} KIS 웹소켓 연결됨")

    #LS  WebSocket 연결
    account = user.find_account_by_abbr('LS')
    ls_acctno = account.account_no
    client_ws_manager = ClientWsManager()
    stock_ws_manager = StockWsManager(client_ws_manager)
    # if not stock_ws_manager.is_connected(user_id, ls_acctno):
    result = await stock_ws_manager.connect(user_id, ls_acctno)
    client_ws_manager.broadcast(str(result))
    logger.info(f"User {user_id} LS 웹소켓 연결됨")

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received data from user {user_id}: {data}")
            await client_ws_manager.send_to_client(f"Message text was: {data}", user_id)
    except WebSocketDisconnect:
        client_ws_manager.disconnect(user_id)
        logger.info(f"User {user_id} client 웹소켓 종료됨")        

# @router.websocket("/ws/kis/call/{stk_code}")
# async def kis_call(websocket: WebSocket, stk_code: str):
#     ''' KIS 증권사에 주식호가 요청 '''   
#     user_id = config.DEFAULT_USER_ID
#     user_service = get_user_service()
#     user = await user_service.get_1(user_id)
#     account = user.find_account_by_abbr('KIS')
#     kis_acctno = account.account_no

#     client_ws_manager = ClientWsManager()
#     stock_ws_manager = StockWsManager(client_ws_manager)    
#     task = stock_ws_manager.get_task(user_id, kis_acctno)
    
#     if task is None:
#         await websocket.send_json({"code": "01", "detail": f"{kis_acctno} 계좌에 대한 WebSocket 작업이 없습니다."})
#     else: 
#         task.subscribe(KIS_WSReq.BID_ASK, stk_code)
#         await websocket.send_json({"code": "00", "detail": f"{stk_code} 호가 요청 성공"})
    

# @router.websocket("/ws/kis")
# async def websocket_endpoint(websocket: WebSocket):            
#     # KIS 증권사에 연결한다
#     user_service = get_user_service()
#     user_id = config.DEFAULT_USER_ID
#     user = await user_service.get_1(user_id)
#     account = user.find_account_by_abbr('KIS')
#     kis_acctno = account.account_no
#     client_ws_manager = ClientWsManager()
#     stock_ws_manager = StockWsManager(client_ws_manager)
#     if not stock_ws_manager.is_connected(user_id, kis_acctno):   
#         result = await stock_ws_manager.connect(user_id, kis_acctno)
#         logger.info(f"User {user_id} KIS 웹소켓 연결됨")
        
#     return result

# @router.websocket("/ws/ls")
# async def websocket_endpoint(websocket: WebSocket):            
#     # 증권사에 연결한다
#     user_service = get_user_service()
#     user_id = config.DEFAULT_USER_ID
#     user = await user_service.get_1(user_id)
#     account = user.find_account_by_abbr('LS')
#     ls_acctno = account.account_no
#     client_ws_manager = ClientWsManager()
#     stock_ws_manager = StockWsManager(client_ws_manager)
#     if stock_ws_manager.is_connected(user_id, ls_acctno):
#         return {"code":"01", "detail": f"{user_id}, {ls_acctno} 이미 연결되어 있습니다."}
    
#     result = await stock_ws_manager.connect(user_id, ls_acctno)
#     return result

