import asyncio
from datetime import datetime
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest
from app.core.mongodb import MongoDb
from app.domain.users.user_service import UserService
from app.main import app  # 여러분의 FastAPI 앱 인스턴스 경로
from unittest.mock import AsyncMock, patch
from app.main import app

# client = TestClient(app)

# async def execute_startup():
#     # FastAPI 앱의 'startup' 이벤트를 수동으로 실행
#     await app.router.startup()

# async def execute_shutdown():
#     # FastAPI 앱의 'startup' 이벤트를 수동으로 실행
#     await app.router.shutdown()


@pytest.mark.asyncio
async def test_get_all_users():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        MongoDb.initialize('mongodb://root:root@test.kfs.co.kr:27017')
        try:
            app.state.user_service =  await UserService.create_instance(db_client=MongoDb.get_client())
            print("User service created successfully")
        except Exception as e:
            print("----> user_service 실패:" , e)    
        
        with patch('app.core.dependency.get_user_service') as mock_get_user_service:
            data = [{
                'user_id': '1', 
                'user_name': 'Test User',
                "email": "kdy987@gmail.com",
                "password": "1234",
                "kind": "P",  # 이 필드는 선택적이며 기본값 'P'를 사용합니다.
                "created_at": datetime.utcnow().isoformat(),  # ISO 포맷 날짜
                "additional_attributes": []  # 빈 리스트 또는 유효한 속성 목록
            }]            

            mock_service = AsyncMock()
            mock_service.get_all_users.return_value = data
            mock_get_user_service.return_value = mock_service
            
            response = await ac.get("/api/v1/users")
            assert response.status_code == 200
            #assert response.json() == data
        del app.state.user_service    

# @pytest.mark.asyncio
# async def test_get_all_users():
#     MongoDb.initialize('mongodb://root:root@test.kfs.co.kr:27017')
#     try:
#         app.state.user_service =  await UserService.create_instance(db_client=MongoDb.get_client())
#         print("User service created successfully")
#     except Exception as e:
#         print("----> user_service 실패:" , e)    
    
#     with patch('app.core.dependency.get_user_service') as mock_get_user_service:
#         mock_service = AsyncMock()
#         mock_service.get_all_users.return_value = [{'user_id': '1', 'name': 'Test User'}]
#         mock_get_user_service.return_value = mock_service
        
#         response = client.get("/api/v1/users")
#         assert response.status_code == 200
#         assert response.json() == [{'user_id': '1', 'name': 'Test User'}]
#     del app.state.user_service    

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
