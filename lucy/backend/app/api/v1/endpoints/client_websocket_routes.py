# client_websocket_routes.py
"""
모듈 설명: 
    - client(browser)와 서버간의 웹소켓 통신을 위한 라우터
주요 기능:
    - 

작성자: 김도영
작성일: 12
버전: 1.0
"""

from fastapi import APIRouter, WebSocket
from typing import List

router = APIRouter()
clients: List[WebSocket] = []

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await broadcast_message("서버로부터의 메세지:" + data)
    except Exception as e:
        print(f"Client disconnected: {e}")
    finally:
        clients.remove(websocket)

async def broadcast_message(message: str):
    for client in clients:
        await client.send_text(message)

# TODO : 증권사와 연결 후
# async def connect_to_broker():
#     uri = "wss://broker-websocket-url"  # 증권사 WebSocket URL을 여기에 입력
#     async with websockets.connect(uri) as websocket:
#         while True:
#             data = await websocket.recv()
#             print(f"Received data from broker: {data}")
#             # 모든 클라이언트에 데이터 전송
#             await broadcast_message(data)

# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(connect_to_broker())