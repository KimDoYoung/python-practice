import asyncio
from fastapi.testclient import TestClient
import pytest
from app.main import app  # 여러분의 FastAPI 앱 인스턴스 경로
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)

async def execute_startup():
    # FastAPI 앱의 'startup' 이벤트를 수동으로 실행
    await app.router.startup()

async def execute_shutdown():
    # FastAPI 앱의 'startup' 이벤트를 수동으로 실행
    await app.router.shutdown()

def test_get_all_users():
    asyncio.run(execute_startup())  # startup 이벤트를 실행
    with patch('app.core.dependency.get_user_service') as mock_get_user_service:
        mock_service = AsyncMock()
        mock_service.get_all_users.return_value = [{'user_id': '1', 'name': 'Test User'}]
        mock_get_user_service.return_value = mock_service
        
        response = client.get("/api/v1/users")
        assert response.status_code == 200
        assert response.json() == [{'user_id': '1', 'name': 'Test User'}]
    asyncio.run(execute_shutdown())  # startup 이벤트를 실행

# def test_get_user():
#     with patch('app.core.dependency.get_user_service') as mock_get_user_service:
#         mock_service = AsyncMock()
#         mock_service.get_user.return_value = {'user_id': '1', 'name': 'Test User'}
#         mock_get_user_service.return_value = mock_service
        
#         response = client.get("/api/v1/user/1")
#         assert response.status_code == 200
#         assert response.json() == {'user_id': '1', 'name': 'Test User'}

# def test_create_user():
#     user_data = {'name': 'New User', 'email': 'new@user.com'}
#     with patch('app.core.dependency.get_user_service') as mock_get_user_service:
#         mock_service = AsyncMock()
#         mock_service.create_user.return_value = {**user_data, 'user_id': '2'}
#         mock_get_user_service.return_value = mock_service
        
#         response = client.post("/user", json=user_data)
#         assert response.status_code == 200
#         assert response.json() == {**user_data, 'user_id': '2'}

# def test_update_user():
#     update_data = {'name': 'Updated User'}
#     with patch('app.core.dependency.get_user_service') as mock_get_user_service:
#         mock_service = AsyncMock()
#         mock_service.update_user.return_value = {'user_id': '1', **update_data}
#         mock_get_user_service.return_value = mock_service
        
#         response = client.put("/user/1", json=update_data)
#         assert response.status_code == 200
#         assert response.json() == {'user_id': '1', **update_data}

# def test_delete_user():
#     with patch('app.core.dependency.get_user_service') as mock_get_user_service:
#         mock_service = AsyncMock()
#         mock_service.delete_user.return_value = None
#         mock_get_user_service.return_value = mock_service
        
#         response = client.delete("/user/1")
#         assert response.status_code == 200
#         assert response.json() == {'msg': 'User 1 deleted successfully'}
