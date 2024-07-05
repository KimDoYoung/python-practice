# websocket_routes.py
"""
모듈 설명: 
    - 
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 05
버전: 1.0
"""
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from backend.app.core.logger import get_logger
from backend.app.managers.client_ws_manager import ClientWsManager

logger = get_logger(__name__)
router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: str = Query(...)):
    client_ws_manager = ClientWsManager()
    await client_ws_manager.connect(websocket, user_id)
    logger.debug(f"User {user_id} client 웹소켓 연결됨")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received data from user {user_id}: {data}")
            await client_ws_manager.send_to_client(f"Message text was: {data}", user_id)
    except WebSocketDisconnect:
        client_ws_manager.disconnect(user_id)
        logger.info(f"User {user_id} client 웹소켓 종료됨")
