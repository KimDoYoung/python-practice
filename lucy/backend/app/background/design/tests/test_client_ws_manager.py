import pytest
from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
from backend.app.background.design.managers.client_ws_manager import ClientWsManager
import asyncio

app = FastAPI()

client_ws_manager = ClientWsManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await client_ws_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await client_ws_manager.send_to_client(f"Message text was: {data}", user_id)
    except WebSocketDisconnect:
        client_ws_manager.disconnect(user_id, websocket)

@app.get("/reset")
async def reset():
    client_ws_manager.reset()
    return {"message": "All connections have been reset"}

@app.get("/reset_user/{user_id}")
async def reset_user(user_id: str):
    client_ws_manager.reset_user(user_id)
    return {"message": f"All connections for user {user_id} have been reset"}

client = TestClient(app)

@pytest.mark.asyncio
async def test_websocket_connection():
    user_id = "test_user"
    with client.websocket_connect(f"/ws?user_id={user_id}") as websocket:
        websocket.send_text("Hello")
        data = websocket.receive_text()
        assert data == "Message text was: Hello"

@pytest.mark.asyncio
async def test_send_personal_message():
    user_id = "test_user"
    with client.websocket_connect(f"/ws?user_id={user_id}") as websocket:
        await client_ws_manager.send_to_client("Test Message", user_id)
        data = websocket.receive_text()
        assert data == "Test Message"

@pytest.mark.asyncio
async def test_reset_user():
    user_id = "test_user"
    with client.websocket_connect(f"/ws?user_id={user_id}") as websocket:
        websocket.send_text("Hello")
        data = websocket.receive_text()
        assert data == "Message text was: Hello"
        response = client.get(f"/reset_user/{user_id}")
        assert response.json() == {"message": f"All connections for user {user_id} have been reset"}
        websocket.close()
        assert user_id not in client_ws_manager.active_connections

@pytest.mark.asyncio
async def test_reset():
    user_id_1 = "user1"
    user_id_2 = "user2"
    with client.websocket_connect(f"/ws?user_id={user_id_1}") as websocket1:
        with client.websocket_connect(f"/ws?user_id={user_id_2}") as websocket2:
            websocket1.send_text("Hello user1")
            data1 = websocket1.receive_text()
            assert data1 == "Message text was: Hello user1"
            
            websocket2.send_text("Hello user2")
            data2 = websocket2.receive_text()
            assert data2 == "Message text was: Hello user2"
            
            response = client.get("/reset")
            assert response.json() == {"message": "All connections have been reset"}
            websocket1.close()
            websocket2.close()
            assert not client_ws_manager.active_connections
