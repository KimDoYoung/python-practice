import os
from beanie import init_beanie
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from backend.app.domains.stc.kis.model.kis_order_cash_model import OrderCashRequest
from backend.app.domains.user.user_model import User
from backend.app.core.dependency import get_user_service
from managers.client_ws_manager import ClientWsManager
from managers.stock_ws_manager import StockWsManager
from backend.app.core.config import config
from backend.app.core.mongodb import MongoDb
from managers.stock_api_manager import StockApiManager


app = FastAPI()

client_ws_manager = None
stock_ws_manager = None
api_manager = None

async def init_db():
    ''' Lucy가 사용하는 stockdb 초기화 '''
    mongodb_url = config.DB_URL 
    db_name = config.DB_NAME
    await MongoDb.initialize(mongodb_url)
    
    db = MongoDb.get_client()[db_name]
    await init_beanie(database=db, document_models=[User])

@app.on_event("startup")
async def startup_event():
    global client_ws_manager, stock_ws_manager, api_manager
    await init_db()
    client_ws_manager = ClientWsManager()
    stock_ws_manager = StockWsManager(client_ws_manager)
    api_manager = StockApiManager()
    api_manager.set_user_service(get_user_service())


@app.get("/", response_class=HTMLResponse)
async def get():
    html_path = os.path.join(os.getcwd(), "main_ws1.html")

    with open(html_path, "r", encoding="utf-8") as file:
        html = file.read()
    return HTMLResponse(html)

#
# WebSocket
#
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await client_ws_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await client_ws_manager.send_to_client(f"Message text was: {data}", user_id)
    except WebSocketDisconnect:
        client_ws_manager.disconnect(user_id)

@app.get("/start-realdata/{user_id}/{acctno}")
async def start_stock_ws(user_id: str, acctno: str):
    ''' 사용자의 acctno에 대해서 연결을 시작한다'''
    #stock_accounts = user.stock_accounts
    if stock_ws_manager.is_connected(user_id, acctno):
        return {"code":"01", "detail": f"{user_id}, {acctno} 이미 연결되어 있습니다."}
    result = await stock_ws_manager.connect(user_id, acctno)
    return result

@app.get("/stop-realdata/{user_id}/{acctno}")
async def stop_stock_ws(user_id: str, acctno: str):
    ''' 사용자의 acctno에 대해서 실시간 연결을 중단한다 '''
    if stock_ws_manager.is_connected(user_id, acctno):
        await stock_ws_manager.disconnect(user_id, acctno)
    return {"message": f"Stopped WebSocket for user {user_id}"}
    
@app.get("/status-realdata")
async def stop_stock_ws():
    return stock_ws_manager.status()
#
# Restful API
# 
@app.post("/order-cash/{user_id}/{acctno}")
async def order_cash(user_id:str, acctno:str, order_cash_request: OrderCashRequest):
    ''' 매도/매수 주문'''
    stk_abbr = order_cash_request.stk_abbr
    # user_service = get_user_service()
    # user = user_service.get_user(user_id)
    stock_api =  await api_manager.stock_api(user_id, acctno, stk_abbr)
    
    order_cash_result = stock_api.order_cash(order_cash_request)

    return order_cash_result




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
