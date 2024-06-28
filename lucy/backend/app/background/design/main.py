from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from managers.client_ws_manager import ClientWsManager
from managers.stock_ws_manager import StockWsManager

app = FastAPI()

client_ws_manager = ClientWsManager()
stock_ws_manager = StockWsManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await client_ws_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await client_ws_manager.send_personal_message(f"Message text was: {data}", user_id)
    except WebSocketDisconnect:
        client_ws_manager.disconnect(user_id)

@app.get("/start/{user_id}/{stk_company_abbr}")
async def start_stock_ws(user_id: str, stk_company_abbr: str):
    if not stock_ws_manager.is_connected(user_id, stk_company_abbr):
        await stock_ws_manager.connect(user_id, stk_company_abbr)
    return {"message": f"Started WebSocket for {stk_company_abbr} and user {user_id}"}

@app.get("/stop/{user_id}/{stk_company_abbr}")
async def stop_stock_ws(user_id: str, stk_company_abbr: str):
    await stock_ws_manager.disconnect(user_id, stk_company_abbr)
    return {"message": f"Stopped WebSocket for {stk_company_abbr} and user {user_id}"}
