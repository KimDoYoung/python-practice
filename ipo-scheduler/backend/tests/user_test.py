import pytest
from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field

# MongoDB URL을 직접 코드에 정의
MONGODB_URL = "mongodb://root:root@test.kfs.co.kr:27017/ipo-scheduler"

# 1. User 모델 정의 (pydantic 기반)
class User(Document):
    user_id: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)

    class Settings:
        collection = "User"  # 사용할 MongoDB 컬렉션 설정

# 2. Beanie 초기화 및 MongoDB 연결 설정
async def init_db():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database()
    await init_beanie(database=db, document_models=[User])

# 3. 테스트 함수 작성 (insert와 find_one 수행)
@pytest.mark.asyncio
async def test_insert_and_find():
    # DB 초기화
    await init_db()

    # 동일한 User 데이터 정의
    user_data = {"user_id": "test_user", "password": "1111", "email": "test_user@example.com"}

    # Insert 실행
    user = User(**user_data)
    await user.insert()
    print(f"Inserted User: {user}")

    # Find One 실행
    found_user = await User.find_one(User.emauser_idil == "test_user")
    assert found_user is not None, "No user found with the given email"
    assert found_user.email == "test_user@example.com"
    print(f"Found User: {found_user}")
