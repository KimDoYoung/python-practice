import asyncio
from beanie import init_beanie
from httpx import AsyncClient
import pytest
from app.core.dependency import get_user_service
from app.core.mongodb import MongoDb
from app.domain.users.user_model import User
from app.main import app

base_url = "http://localhost:8000"

@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

async def db_init():
    await MongoDb.initialize("mongodb://root:root@test.kfs.co.kr:27017/")
    db = MongoDb.get_client()["stockdb"]
    await init_beanie(database=db, document_models=[User])

@pytest.mark.asyncio
async def test_get_all_users(event_loop):

    await db_init()
    async with AsyncClient(app=app, base_url=base_url) as async_client:
        response = await async_client.get("/api/v1/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)  # 응답이 리스트 형태인지 확인


@pytest.mark.asyncio
async def test_get_1(event_loop):
    await db_init()
    async with AsyncClient(app=app, base_url=base_url) as async_client:
        response = await async_client.get("/api/v1/user/kdy987")
        print(response.json())
        assert response.status_code == 200
        user_service = get_user_service()
        assert user_service is not None

@pytest.mark.asyncio
async def test_create_update_delete_user(event_loop):
    '''
    insert -> update -> delete 테스트 
    '''
    await db_init()
    user_data = {'user_id': 'aaa', 'user_name':'123', 'password':'123', 'email': 'new@user.com'}
    async with AsyncClient(app=app, base_url=base_url) as async_client:           
        # delete
        response = await async_client.delete("/api/v1/user/aaa")
        assert response.status_code == 200
        # insert
        user_service = get_user_service()
        response = await async_client.post("/api/v1/user", json=user_data)
        assert response.status_code == 200
        user = await user_service.get_user('aaa')
        assert user.user_name == '123'
        
        # update
        response = await async_client.put("/api/v1/user/aaa", json={'user_name':'456'})
        user = await user_service.get_user('aaa')
        assert  user.user_name == '456'
        count = await user_service.count()
       
        # delete
        response = await async_client.delete("/api/v1/user/aaa")
        assert response.status_code == 200
        assert response.json() == {'msg': 'User aaa deleted successfully'}
        count_1 = await user_service.count()
        assert count == count_1 + 1
        
