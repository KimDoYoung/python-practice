from typing import AsyncGenerator
from fastapi import Depends
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from backend.app.domains.user.appkey_model import AppKey
from backend.app.domains.user.appkey_service import AppKeyService
from backend.app.core.exceptions.business_exceptions import BusinessException

TEST_DB_HOST =  '172.20.100.120'
TEST_DB_USER =  'kdy987'
TEST_DB_PASSWORD = 'kalpa987!'

# @pytest.fixture(scope="module")
# async def get_db()-> AsyncGenerator[AsyncSession, None]:
#     DB_URL= f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}/stock"
#     engine = create_async_engine(DB_URL, echo=True, future=True)
#     AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

#     session = AsyncSessionLocal()
#     try:
#         yield session
#     finally:
#         await session.close()

@pytest.fixture(scope="module")
async def get_db():
    DB_URL = f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}/stock"
    engine = create_async_engine(DB_URL, echo=True, future=True)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        yield session

@pytest.fixture()
def get_service():
    service = AppKeyService()
    return service


@pytest.mark.asyncio
async def test_insert_app_key(get_service, get_db):
    service = get_service
    app_key = AppKey(user_id="test_user", key_name="test_key", key_value="12345")
    result = await service.insert(app_key, get_db)
    assert result.created_at is not None
    assert result.use_yn == "Y"
    assert result.key_name == "test_key"

# @pytest.mark.asyncio
# async def test_insert_app_key(get_service, get_db):
#     service = get_service
#     session = await get_db
#     app_key = AppKey(user_id="test_user", key_name="test_key", key_value="12345")
#     result = await service.insert(app_key, session)
#     assert result.created_at is not None
#     assert result.use_yn == "Y"
#     assert result.key_name == "test_key"

# @pytest.mark.asyncio
# async def test_insert_app_key(get_service , get_db  : AsyncSession):
#     service =  get_service
#     session =  get_db
#     app_key = AppKey(user_id="test_user", key_name="test_key", key_value="12345")
#     result = await service.insert(app_key, session)  # session을 올바르게 사용
#     assert result.created_at is not None
#     assert result.use_yn == "Y"
#     assert result.key_name == "test_key"

# 1. 임의의 데이터로 insert 수행
# @pytest.mark.asyncio
# async def test_insert_app_key(get_service, get_db):
#     service = get_service
#     session = get_db
#     app_key = AppKey(user_id="test_user", key_name="test_key", key_value="12345")
#     result = await service.insert(app_key, session)
#     assert result.created_at is not None
#     assert result.use_yn == "Y"
#     assert result.key_name == "test_key"



# 2. 같은 데이터로 insert 시 예외 발생 확인
# @pytest.mark.asyncio
# async def test_insert_duplicate_app_key(app_key_service, async_session):
#     service = await app_key_service
#     app_key = AppKey(user_id="test_user", key_name="test_key", key_value="12345")
#     with pytest.raises(BusinessException) as excinfo:
#         await service.insert(app_key, async_session)
#     assert 'already exists' in str(excinfo.value)

# 3. 데이터 조회
# @pytest.mark.asyncio
# async def test_get_app_key(app_key_service, async_session):
#     service = await app_key_service
#     app_key_base = AppKey(user_id="test_user", key_name="test_key")
#     result = await service.get(app_key_base, async_session)
#     assert result.user_id == "test_user"