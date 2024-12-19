import asyncio
import threading
import time
import json
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import websocket

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
ws = None
ws_thread = None
should_run = False

# 웹소켓 이벤트 핸들러
def on_open(ws):
    logger.info("웹소켓 연결이 열렸습니다.")
    register_quote_info(ws, "005930")  # 주식종목 005930의 호가정보 등록

def on_message(ws, message):
    logger.info(f"웹소켓으로부터 받은 데이터: {message}")
    response = json.loads(message)
    if "header" in response and response["header"].get("tr_id") == "PINGPONG":
        logger.debug(f"PINGPONG 데이터 전송: {message}")

def on_error(ws, error):
    logger.error(f"웹소켓 에러 발생: {error}")

def on_close(ws):
    logger.info("웹소켓 연결이 닫혔습니다.")

# 호가 정보 등록 및 해제 함수
def register_quote_info(ws, stock_code):
    data = {
        "header": {
            "approval_key": "8f4e6614-6f98-4835-b03c-fb37608d5c58",
            "personalseckey": "5e408P+AfqziO/xdFuAQipkAIbQILbZAwlpMbXvbSFqywYzyyuzoCmqvzkq7lRyWeFx0YmO6sNtPIaYr76KW9PbX4Bwo8IIWfsgA82uVSw3vehZXHaQ0QlPGdghb5i5P3Fx2e2F1ThyDZf/rxnqKH1TLaKh7KBhNiThY4EeWLcDevJE2t/w=",
            "custtype": "P",
            "tr_type": "1",  # 호가 정보 등록
            "content_type": "utf-8"
        },
        "body": {
            "input": {
                "tr_id": "H0STASP0",
                "tr_key": stock_code
            }
        }
    }
    ws.send(json.dumps(data))
    logger.info(f"호가 정보 등록 데이터 보냄: {json.dumps(data)}")

def unregister_quote_info(ws, stock_code):
    data = {
        "header": {
            "approval_key": "8f4e6614-6f98-4835-b03c-fb37608d5c58",
            "personalseckey": "5e408P+AfqziO/xdFuAQipkAIbQILbZAwlpMbXvbSFqywYzyyuzoCmqvzkq7lRyWeFx0YmO6sNtPIaYr76KW9PbX4Bwo8IIWfsgA82uVSw3vehZXHaQ0QlPGdghb5i5P3Fx2e2F1ThyDZf/rxnqKH1TLaKh7KBhNiThY4EeWLcDevJE2t/w=",
            "custtype": "P",
            "tr_type": "2",  # 호가 정보 해제
            "content_type": "utf-8"
        },
        "body": {
            "input": {
                "tr_id": "H0STASP0",
                "tr_key": stock_code
            }
        }
    }
    ws.send(json.dumps(data))
    logger.info(f"호가 정보 해제 데이터 보냄: {json.dumps(data)}")

# 웹소켓 연결 함수
def run_websocket():
    global ws
    ws = websocket.WebSocketApp("ws://ops.koreainvestment.com:21000/tryitout",
                                on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    while should_run:
        ws.run_forever()
        time.sleep(5)  # 재연결 시도 전 대기 시간

# 웹소켓 시작 엔드포인트
@app.get("/start-ws")
async def start_ws():
    global should_run, ws_thread
    if ws_thread is None or not ws_thread.is_alive():
        should_run = True
        ws_thread = threading.Thread(target=run_websocket)
        ws_thread.start()
        return {"message": "웹소켓 연결 시작됨"}
    else:
        raise HTTPException(status_code=400, detail="웹소켓이 이미 실행 중입니다.")

# 웹소켓 정지 엔드포인트
@app.get("/stop-ws")
async def stop_ws():
    global should_run, ws
    if ws_thread and ws_thread.is_alive():
        should_run = False
        if ws:
            unregister_quote_info(ws, "005930")  # 주식종목 005930의 호가정보 해제
            ws.close()
        ws_thread.join()
        return {"message": "웹소켓 연결 종료됨"}
    else:
        raise HTTPException(status_code=400, detail="웹소켓이 실행 중이 아닙니다.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
