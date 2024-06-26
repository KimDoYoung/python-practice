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

logger = get_logger(__name__)

app = FastAPI()

is_websocket_running = False
websocket_task = None
clients: List[WebSocket] = []
korea_investment_websocket = None
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Real-Time Logs</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        #logs {
            height: 400px;
            overflow-y: scroll;
            border: 1px solid #ccc;
            padding: 10px;
        }
    </style>
</head>
<body>
    <h1>Real-Time Logs</h1>
    <button id="start">Start</button>
    <button id="stop">Stop</button>
    <div id="logs"></div>
    <script>
        var ws;

        function startWebSocket() {
            ws = new WebSocket("ws://localhost:8000/ws");

            ws.onmessage = function(event) {
                var logsDiv = $('#logs');
                var newLog = $('<div>').text(event.data);
                logsDiv.append(newLog);

                // 자동 스크롤
                logsDiv.scrollTop(logsDiv[0].scrollHeight);
            };

            ws.onerror = function(event) {
                console.error("WebSocket error observed:", event);
            };

            ws.onclose = function(event) {
                console.log("WebSocket connection closed:", event);
            };
        }

        function stopWebSocket() {
            if (ws) {
                ws.close();
            }
        }

        $(document).ready(function() {
            startWebSocket();
            $('#start').click(function() {
                $.post('/start');
                //startWebSocket();
            });

            $('#stop').click(function() {
                $.post('/stop');
                //stopWebSocket();
            });
        });
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
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

    stocks = ('458870', '009520', '108380')
    # stocks = ('458870')
    for stock in stocks:
        senddata = await subscribe(user, KIS_WSReq.BID_ASK, stock)
        logger.debug(f"보낸데이터 : [{senddata}]")
        await websocket.send(senddata)
        await asyncio.sleep(0.5)
    #    await subscribe(user, websocket, KIS_WSReq.CONTRACT, stock)
    #await subscribe(user, websocket, KIS_WSReq.NOTICE, None)


async def on_message(websocket, message):
    logger.info(f"웹소켓으로부터 받은 데이터: {message}")



async def on_error(websocket, error):
    logger.error(f"웹소켓 에러 발생: {error}")

async def on_close(websocket):
    logger.info("웹소켓 연결이 닫혔습니다.")

async def connect_to_korea_investment():
    uri = "ws://ops.koreainvestment.com:21000"
    try:
        user_service = get_user_service()
        user = await user_service.get_1("kdy987")
        KIS_APP_KEY = user.get_value_by_key("KIS_APP_KEY")
        KIS_APP_SECRET = user.get_value_by_key("KIS_APP_SECRET")

        ws_approval_key = get_ws_approval_key(KIS_APP_KEY, KIS_APP_SECRET)    
        user.set_value_by_key("KIS_WS_APPROVAL_KEY", ws_approval_key)

        async with websockets.connect(uri, ping_interval=60) as websocket:
            korea_investment_websocket = websocket
            await on_open(user,websocket)

            # aes_key = None
            # aes_iv = None

            while True:
                received_text = await websocket.recv()  
                logger.info("웹소켓(KIS로부터 받은데이터) : [" + received_text + "]")
                await broadcast_message(received_text)
                if is_real_data(received_text): # 실시간 데이터인 경우
                    aes_key = user.get_value_by_key("KIS_WS_AES_KEY")
                    aes_iv = user.get_value_by_key("KIS_WS_AES_IV")
                    header, real_model = kis_ws_real_data_parsing(received_text, aes_key, aes_iv)
                    logger.info(f"header: {header}")
                    logger.info(f"real_model: {real_model}")
                    model_str = real_model.to_str()
                    await broadcast_message(model_str)
                    await asyncio.sleep(1)
                else: # 실시간 데이터가 아닌 경우
                    try:
                        resp_json = json.loads(received_text)
                        if resp_json['header']['tr_id'] == 'PINGPONG': # PINGPONG 데이터인 경우
                            await websocket.pong(received_text)  # 웹소켓 클라이언트에서 pong을 보냄
                            logger.debug(f"PINGPONG 데이터 전송: [{received_text}]")
                        else:
                            kis_ws_model = KisWsResponse.from_json_str(received_text)
                            if kis_ws_model.body.output is not None and kis_ws_model.body.output.iv is not None and kis_ws_model.body.output.key is not None:
                                user.set_value_by_key("KIS_WS_AES_IV", kis_ws_model.body.output.iv)
                                user.set_value_by_key("KIS_WS_AES_KEY", kis_ws_model.body.output.key)
                                # aes_iv = kis_ws_model.body.output.iv
                                # aes_key =  kis_ws_model.body.output.key
                            logger.info(f"PINGPONG 아닌 것: [{received_text}]")
                            logger.debug(f"kis_ws_model: {json.dumps(kis_ws_model.model_dump(), ensure_ascii=False)}")
                    except ValueError as e:
                        logger.error(f"Error parsing response: {e}")        
    except websockets.exceptions.ConnectionClosed as e:
        await on_close(korea_investment_websocket)
        logger.error(f"웹소켓 연결이 닫혔습니다: {e}")
    except Exception as e:
        await on_error(korea_investment_websocket, e)
        logger.error(f"웹소켓 연결 중 에러 발생: {e}")
    finally:
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
    await broadcast_message("Kis Websocket이 시작되었습니다.")
    return {"message": "WebSocket connection is started"}

@app.post("/stop")
async def stop():
    logger.info("웹소켓 테스트 서버 중지")
    await kis_ws_stop()
    await broadcast_message("Kis Websocket이 중지되었습니다.")
    return {"message": "WebSocket connection is not running"}

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
