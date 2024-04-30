import asyncio
from httpx import AsyncClient
import pytest
from app.core.dependency import get_database, initialize_beanie
from app.core.mongodb import MongoDb
from app.domain.users.user_service import UserService
from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def startup_event():
    db_url = 'mongodb://root:root@test.kfs.co.kr:27017/'
    db_name = 'stockdb'
    db = await get_database(db_url, db_name)
    await initialize_beanie(db)

@pytest.mark.asyncio
async def test_get_all_users(event_loop):
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/api/v1/users")
        assert response.status_code == 200
        # 데이터 형식에 따라 추가적인 내용 확인이 필요할 수 있습니다.
        assert isinstance(response.json(), list)  # 응답이 리스트 형태인지 확인

# @pytest.mark.asyncio
# async def test_get_all_users(event_loop ):
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
#         MongoDb.initialize('mongodb://root:root@test.kfs.co.kr:27017')
#         app.state.user_service =  await UserService.create_instance(db_client= MongoDb.get_client())
#         response = await ac.get("/api/v1/users")
#         assert response.status_code == 200
#         del app.state.user_service
#         # MongoDb.close()

# @pytest.mark.asyncio
# async def test_get_1(event_loop):
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
#         MongoDb.initialize('mongodb://root:root@test.kfs.co.kr:27017')
#         app.state.user_service =  await UserService.create_instance(db_client=MongoDb.get_client())
#         response = await ac.get("/api/v1/user/kdy987")
#         assert response.status_code == 200
#         del app.state.user_service
#         #MongoDb.close()


# @pytest.mark.asyncio
# async def test_create_update_delete_user(event_loop):
#     '''
#     insert -> update -> delete 테스트 
#     '''
#     user_data = {'user_id': 'aaa', 'user_name':'123', 'password':'123', 'email': 'new@user.com'}
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:           
#         MongoDb.initialize('mongodb://root:root@test.kfs.co.kr:27017')
#         app.state.user_service =  await UserService.create_instance(db_client=MongoDb.get_client())
       
#         # insert
#         response = await async_client.post("/api/v1/user", json=user_data)
#         assert response.status_code == 200
#         user = await app.state.user_service.get_user('aaa')
#         assert user.user_name == '123'
        
#         # update
#         response = await async_client.put("/api/v1/user/aaa", json={'user_name':'456'})
#         user = await app.state.user_service.get_user('aaa')
#         assert user.user_name == '456'
#         count = await app.state.user_service.count()
       
#         # delete
#         response = await async_client.delete("/api/v1/user/aaa")
#         assert response.status_code == 200
#         assert response.json() == {'msg': 'User aaa deleted successfully'}
#         count_1 = await app.state.user_service.count()
#         assert count == count_1 + 1
        
#         del app.state.user_service 


# @pytest.fixture(scope="module")
# async def async_client() -> AsyncGenerator[AsyncClient,None]:
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
#         yield ac

# @pytest.fixture(scope="module")
# async def user_service():
#     print("Initializing MongoDB")
#     MongoDb.initialize('mongodb://root:root@test.kfs.co.kr:27017')
#     app.state.user_service = await UserService.create_instance(db_client=MongoDb.get_client())
#     print(f"UserService set in app.state: {app.state.user_service}")
#     yield app.state.user_service
#     del app.state.user_service
#     MongoDb.close()
#     print("MongoDB closed and UserService removed from app.state")

# @pytest.fixture(scope="module")
# async def user_service():
#     MongoDb.initialize('mongodb://root:root@test.kfs.co.kr:27017')
#     app.state.user_service = await UserService.create_instance(db_client=MongoDb.get_client())
#     yield  # 이 위치에 객체를 반환할 필요는 없습니다.
#     del app.state.user_service
#     MongoDb.close()
# @pytest.fixture
# async def user_service():
#     MongoDb.initialize('mongodb://root:root@test.kfs.co.kr:27017')
#     try:
#         app.state.user_service = await UserService.create_instance(db_client=MongoDb.get_client())
#         yield app.state.user_service
#     finally:
#         del app.state.user_service
#         MongoDb.close()  # Assuming you have a close method to cleanup DB connection

# @pytest.mark.asyncio
# async def test_get_all_users1111(async_client, user_service):
#     # # 사용자 서비스가 상태에 설정되었는지 확인
#     assert 'user_service' in app.state._state, "User service is not set in the app state"
    
#     response = await async_client.get("/api/v1/users")
#     assert response.status_code == 200




# @pytest.mark.asyncio
# async def test_get_all_users():
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
#         MongoDb.initialize('mongodb://root:root@test.kfs.co.kr:27017')
#         try:
#             app.state.user_service =  await UserService.create_instance(db_client=MongoDb.get_client())
#             print("User service created successfully")
#             response = await ac.get("/api/v1/users")
#             assert response.status_code == 200

#         except Exception as e:
#             print("----> user_service 실패:" , e)    
#         del app.state.user_service    
        

# @pytest.mark.asyncio
# async def test_get_all_users():
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
#         response = await ac.get("/api/v1/users")
#         assert response.status_code == 200



# @pytest.fixture
# async def client():
#     # MongoDB 초기화
#     MongoDb.initialize('mongodb://root:root@test.kfs.co.kr:27017')
#     # UserService 인스턴스 생성
#     app.state.user_service = await UserService.create_instance(db_client=MongoDb.get_client())

#     # AsyncClient 인스턴스 생성 및 관리
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
#         yield ac

#     # 자원 정리
#     del app.state.user_service


# @pytest.mark.asyncio
# async def test_get_all_users(client):
#     response = await client.get("/api/v1/users")
#     assert response.status_code == 200



# @pytest.mark.asyncio
# async def test_get_all_users():
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
#         MongoDb.initialize('mongodb://root:root@test.kfs.co.kr:27017')
#         try:
#             app.state.user_service =  await UserService.create_instance(db_client=MongoDb.get_client())
#             print("User service created successfully")
#         except Exception as e:
#             print("----> user_service 실패:" , e)    
        
#         with patch('app.core.dependency.get_user_service') as mock_get_user_service:
#             data = [{
#                 'user_id': '1', 
#                 'user_name': 'Test User',
#                 "email": "kdy987@gmail.com",
#                 "password": "1234",
#                 "kind": "P",  # 이 필드는 선택적이며 기본값 'P'를 사용합니다.
#                 "created_at": datetime.utcnow().isoformat(),  # ISO 포맷 날짜
#                 "additional_attributes": []  # 빈 리스트 또는 유효한 속성 목록
#             }]            

#             mock_service = AsyncMock()
#             mock_service.get_all_users.return_value = data
#             mock_get_user_service.return_value = mock_service
            
#             response = await ac.get("/api/v1/users")
#             assert response.status_code == 200
#             #assert response.json() == data
#         del app.state.user_service    

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
