import asyncio
import json
from typing import List
from beanie import init_beanie
import websockets
from fastapi import BackgroundTasks, FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from backend.app.core.logger import get_logger
from backend.app.domains.stc.kis.model.kis_websocket_model import KisWsResponse
from backend.app.domains.user.user_model import User
from backend.app.utils.kis_ws_util import KIS_WSReq, get_ws_approval_key, is_real_data, kis_ws_real_data_parsing, new_kis_ws_request
from backend.app.core.config import config
from backend.app.core.mongodb import MongoDb
from backend.app.core.dependency import get_user_service
import os

logger = get_logger(__name__)

app = FastAPI()

is_websocket_running = False
websocket_task = None
clients: List[WebSocket] = []
korea_investment_websocket = None


@app.get("/")
async def get():
    html_path = os.path.join(os.getcwd(), "main_ws1.html")

    with open(html_path, "r", encoding="utf-8") as file:
        html = file.read()
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(client_websocket: WebSocket):
    clients.append(client_websocket)
    logger.debug("client로부터 웹소켓 연결되었습니다.")
    await client_websocket.accept()
    try:
        while True:
            data = await client_websocket.receive_text()
            await client_websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")

async def broadcast_log(message: str):
    disconnected_clients = []
    for client in clients:
        try:
            msg = {"CODE": "SYS", "MSG": message}
            await client.send_text(json.dumps(msg))
            #await client.send_text(msg)
            logger.debug("웹소켓으로 메세지 전송: " + message)
        except WebSocketDisconnect:
            disconnected_clients.append(client)
    
    for client in disconnected_clients:
        clients.remove(client)


async def broadcast_message(message: str):
    disconnected_clients = []
    for client in clients:
        try:
            await client.send_text(message)
            logger.debug("웹소켓으로 메세지 전송: " + message)
        except WebSocketDisconnect:
            disconnected_clients.append(client)
    
    for client in disconnected_clients:
        clients.remove(client)

async def create_kis_ws_request(user: User, tr_id, tr_type, tr_key):
    ws_approval_key = user.get_value_by_key("KIS_WS_APPROVAL_KEY")
    KIS_APP_SECRET = user.get_value_by_key("KIS_APP_SECRET")
    req = new_kis_ws_request()
    req.header.approval_key = ws_approval_key
    req.header.personalseckey = KIS_APP_SECRET
    req.header.tr_type = tr_type
    req.body.input.tr_id = tr_id
    req.body.input.tr_key = tr_key
    senddata = req.model_dump_json()
    logger.debug(f"senddata : [{senddata}]")
    return senddata

async def subscribe(user: User, tr_id, stock_code):
    if tr_id in [KIS_WSReq.BID_ASK, KIS_WSReq.CONTRACT]:
        return await create_kis_ws_request(user, tr_id, '1', stock_code)
    elif tr_id == KIS_WSReq.NOTICE:
        KIS_HTS_USER_ID = user.get_value_by_key("KIS_HTS_USER_ID")
        return await create_kis_ws_request(user, tr_id, '1', KIS_HTS_USER_ID)

async def unsubscribe(user: User, tr_id, stock_code):
    if tr_id in [KIS_WSReq.BID_ASK, KIS_WSReq.CONTRACT]:
        return await create_kis_ws_request(user, tr_id, '2', stock_code)
    elif tr_id == KIS_WSReq.NOTICE:
        KIS_HTS_USER_ID = user.get_value_by_key("KIS_HTS_USER_ID")
        return await create_kis_ws_request(user, tr_id, '2', KIS_HTS_USER_ID)

async def on_open(user,websocket):
    logger.info("웹소켓 연결이 열렸습니다.")
    # user_service = get_user_service()
    # user = await user_service.get_1("kdy987")
    
    # KIS_APP_KEY = user.get_value_by_key("KIS_APP_KEY")
    # KIS_APP_SECRET = user.get_value_by_key("KIS_APP_SECRET")
    # KIS_HTS_USER_ID = user.get_value_by_key("KIS_HTS_USER_ID")
    # ws_approval_key = get_ws_approval_key(KIS_APP_KEY, KIS_APP_SECRET)    
    # user.set_value_by_key("KIS_WS_APPROVAL_KEY", ws_approval_key)

    # stocks = ('160190', '009520', '108380')
    # for stock in stocks:
    #     # 호가 등록
    #     senddata = await subscribe(user, KIS_WSReq.BID_ASK, stock)
    #     logger.debug(f"보낸데이터 : [{senddata}]")
    #     await websocket.send(senddata)
    #     await asyncio.sleep(0.5)
    #     # 체결가 등록
    #     senddata = await subscribe(user, KIS_WSReq.CONTRACT, stock)
    #     await websocket.send(senddata)
    #     await asyncio.sleep(0.5)

    # 고객체결발생통보 등록
    # senddata = await subscribe(user,  KIS_WSReq.NOTICE, None)
    # await websocket.send(senddata)
    # await asyncio.sleep(0.5)


# async def on_message(websocket, message):
#     logger.info(f"웹소켓으로부터 받은 데이터: {message}")



async def on_error(websocket, error):
    await broadcast_log("Kis Websocket 통신 중 에러발생..." + error)
    logger.error(f"웹소켓 에러 발생: {error}")

async def on_close(websocket):
    await broadcast_log("Kis Websocket이 중지되었습니다.")
    logger.info("웹소켓 연결이 닫혔습니다.")

async def connect_to_korea_investment():
    global korea_investment_websocket
    uri = "ws://ops.koreainvestment.com:21000"
    try:
        user_service = get_user_service()
        user = await user_service.get_1("kdy987")
        KIS_APP_KEY = user.get_value_by_key("KIS_APP_KEY")
        KIS_APP_SECRET = user.get_value_by_key("KIS_APP_SECRET")

        ws_approval_key = get_ws_approval_key(KIS_APP_KEY, KIS_APP_SECRET)    
        user.set_value_by_key("KIS_WS_APPROVAL_KEY", ws_approval_key)

        async with websockets.connect(uri, ping_interval=60) as websocket:
            await on_open(user,websocket)
            korea_investment_websocket = websocket
            if korea_investment_websocket is None:
                raise Exception("korea_investment_websocket 웹소켓 연결이 안됨")
            # aes_key = None
            # aes_iv = None

            while True:
                received_text = await websocket.recv()  
                logger.info("웹소켓(KIS로부터 받은데이터) : [" + received_text + "]")
                if is_real_data(received_text): # 실시간 데이터인 경우
                    aes_key = user.get_value_by_key("KIS_WS_AES_KEY")
                    aes_iv = user.get_value_by_key("KIS_WS_AES_IV")
                    header, real_model = kis_ws_real_data_parsing(received_text, aes_key, aes_iv)
                    logger.info(f"header: {header}")
                    logger.info(f"real_model: {real_model}")
                    #model_str = real_model.to_str()
                    real_data_dict = real_model.data_for_client_ws()
                    message_str = json.dumps(real_data_dict)
                    await broadcast_message(message_str)
                    await asyncio.sleep(0.5)
                else: # 실시간 데이터가 아닌 경우
                    try:
                        kis_response = KisWsResponse.from_json_str(received_text)
                        if kis_response.is_pingpong(): # PINGPONG 데이터인 경우
                            await websocket.pong(received_text)  # 웹소켓 클라이언트에서 pong을 보냄
                            logger.debug(f"PINGPONG 데이터 전송: [{received_text}]")
                        elif kis_response.is_error():
                            logger.warning(f"Kis Websocket Response 에러발생: {kis_response.get_error_message()}")
                        else: 
                            iv = kis_response.get_iv()
                            key = kis_response.get_key()
                            user.set_value_by_key("KIS_WS_AES_IV", iv)
                            user.set_value_by_key("KIS_WS_AES_KEY", key)
                            event_log = kis_response.get_event_log()
                            logger.debug(f"event_log: {event_log}")
                            await broadcast_log(event_log)
                    except json.JSONDecodeError as e:
                            logger.error(f"JSON decoding error: {e}")
                    except websockets.ConnectionClosed as e:
                            logger.error(f"WebSocket connection closed: {e}")
                            break
                    except Exception as e:
                            logger.error(f"Unexpected error: {e}")
    except websockets.exceptions.ConnectionClosed as e:
        await on_close(korea_investment_websocket)
        logger.error(f"웹소켓 연결이 닫혔습니다: {e}")
    except Exception as e:
        await on_error(korea_investment_websocket, e)
        logger.error(f"웹소켓 연결 중 에러 발생: {e}")
    finally:
        logger.debug(f"finally.....")
        korea_investment_websocket = None

async def kis_ws_start():
    global is_websocket_running, websocket_task
    if not is_websocket_running:
        websocket_task = asyncio.create_task(connect_to_korea_investment())
        is_websocket_running = True

async def kis_ws_stop():
    global is_websocket_running, websocket_task
    if is_websocket_running and websocket_task:
        websocket_task.cancel()
        is_websocket_running = False

@app.post("/start")
async def start(background_tasks: BackgroundTasks):
    logger.info("웹소켓 테스트 서버 시작")
    await kis_ws_start()
    await broadcast_log("Kis Websocket이 시작되었습니다.")
    return {"message": "WebSocket connection is started"}

@app.post("/stop")
async def stop():
    logger.info("웹소켓 테스트 서버 중지")
    await kis_ws_stop()
    await broadcast_log("Kis Websocket이 중지되었습니다.")
    return {"message": "WebSocket connection is not running"}

@app.get("/subscribe/bid-ask/{stock_code}")
async def subscribe_bid_ask(stock_code: str):
    global korea_investment_websocket
    if korea_investment_websocket is None:
        return {"message": "WebSocket connection is not established"}
    user_service = get_user_service()
    user = await user_service.get_1("kdy987")
    KIS_APP_KEY = user.get_value_by_key("KIS_APP_KEY")
    KIS_APP_SECRET = user.get_value_by_key("KIS_APP_SECRET")

    ws_approval_key = get_ws_approval_key(KIS_APP_KEY, KIS_APP_SECRET)    
    user.set_value_by_key("KIS_WS_APPROVAL_KEY", ws_approval_key)
    senddata = await subscribe(user, KIS_WSReq.BID_ASK, stock_code)
    await korea_investment_websocket.send(senddata)
    return {"message": "호가 등록"}

@app.get("/un-subscribe/bid-ask/{stock_code}")
async def un_subscribe_bid_ask(stock_code: str):
    global korea_investment_websocket
    if korea_investment_websocket is None:
        return {"message": "WebSocket connection is not established"}
    
    user_service = get_user_service()
    user = await user_service.get_1("kdy987")
    KIS_APP_KEY = user.get_value_by_key("KIS_APP_KEY")
    KIS_APP_SECRET = user.get_value_by_key("KIS_APP_SECRET")

    ws_approval_key = get_ws_approval_key(KIS_APP_KEY, KIS_APP_SECRET)    
    user.set_value_by_key("KIS_WS_APPROVAL_KEY", ws_approval_key)

    senddata = await unsubscribe(user, KIS_WSReq.BID_ASK, stock_code)
    await korea_investment_websocket.send(senddata)
    return {"message": "호가 취소"}

@app.get("/subscribe/contract/{stock_code}")
async def subscribe_contract(stock_code: str):
    global korea_investment_websocket
    if korea_investment_websocket is None:
        return {"message": "WebSocket connection is not established"}
    user_service = get_user_service()
    user = await user_service.get_1("kdy987")
    KIS_APP_KEY = user.get_value_by_key("KIS_APP_KEY")
    KIS_APP_SECRET = user.get_value_by_key("KIS_APP_SECRET")

    ws_approval_key = get_ws_approval_key(KIS_APP_KEY, KIS_APP_SECRET)    
    user.set_value_by_key("KIS_WS_APPROVAL_KEY", ws_approval_key)
    
    senddata = await subscribe(user, KIS_WSReq.CONTRACT, stock_code)
    await korea_investment_websocket.send(senddata)
    return {"message": "체결가 등록"}

@app.get("/un-subscribe/contract/{stock_code}")
async def un_subscribe_contract(stock_code: str):
    global korea_investment_websocket
    if korea_investment_websocket is None:
        return {"message": "WebSocket connection is not established"}
    user_service = get_user_service()
    user = await user_service.get_1("kdy987")
    KIS_APP_KEY = user.get_value_by_key("KIS_APP_KEY")
    KIS_APP_SECRET = user.get_value_by_key("KIS_APP_SECRET")

    ws_approval_key = get_ws_approval_key(KIS_APP_KEY, KIS_APP_SECRET)    
    user.set_value_by_key("KIS_WS_APPROVAL_KEY", ws_approval_key)
    senddata = await unsubscribe(user, KIS_WSReq.CONTRACT, stock_code)
    await korea_investment_websocket.send(senddata)
    return {"message": "체결가 취소"}


@app.post("/send")
async def send(request: Request):
    global korea_investment_websocket
    if korea_investment_websocket is None:
        return {"message": "WebSocket connection is not established"}

    data = await request.json()
    message = data.get("message")
    
    if message:
        await korea_investment_websocket.send(message)
        return {"message": "Message sent to WebSocket"}
    return {"message": "No message to send"}


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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
