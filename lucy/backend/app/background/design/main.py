import os
from beanie import init_beanie
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from backend.app.domains.user.user_model import User
from managers.client_ws_manager import ClientWsManager
from managers.stock_ws_manager import StockWsManager
from backend.app.core.config import config
from backend.app.core.mongodb import MongoDb
from backend.app.core.dependency import get_user_service


app = FastAPI()

client_ws_manager = ClientWsManager()
stock_ws_manager = StockWsManager(client_ws_manager)

async def init_db():
    ''' Lucy가 사용하는 stockdb 초기화 '''
    mongodb_url = config.DB_URL 
    db_name = config.DB_NAME
    await MongoDb.initialize(mongodb_url)
    
    db = MongoDb.get_client()[db_name]
    await init_beanie(database=db, document_models=[User])

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/", response_class=HTMLResponse)
async def get():
    html_path = os.path.join(os.getcwd(), "main_ws1.html")

    with open(html_path, "r", encoding="utf-8") as file:
        html = file.read()
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await client_ws_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await client_ws_manager.send_personal_message(f"Message text was: {data}", user_id)
    except WebSocketDisconnect:
        client_ws_manager.disconnect(user_id)

@app.get("/start-realdata/{user_id}")
async def start_stock_ws(user_id: str):
    user_service = get_user_service()# 1. 사용자별로 증권사 계정을 다 가져온다.
    user = await user_service.get_1(user_id)
    
    #stock_accounts = user.stock_accounts
    stock_accounts = ['kis']
    for stk_company_abbr in stock_accounts:
        if not stock_ws_manager.is_connected(user_id, stk_company_abbr):
            await stock_ws_manager.connect(user_id, stk_company_abbr)
    return {"message": f"Started WebSocket for user {user_id}"}

@app.get("/stop-realdata/{user_id}")
async def stop_stock_ws(user_id: str):
    user_service = get_user_service()# 1. 사용자별로 증권사 계정을 다 가져온다.
    user = await user_service.get_1(user_id)
    
    #stock_accounts = user.stock_accounts
    stock_accounts = ['kis']
    for stk_company_abbr in stock_accounts:
        if stock_ws_manager.is_connected(user_id, stk_company_abbr):
            await stock_ws_manager.disconnect(user_id, stk_company_abbr=stk_company_abbr)
    return {"message": f"Stopped WebSocket for user {user_id}"}

@app.get("/status-realdata")
async def stop_stock_ws():
    return stock_ws_manager.status()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
