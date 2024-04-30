
from fastapi import Depends
from app.core.mongodb import MongoDb
from app.domain.users.user_model import User
from app.domain.users.user_service import UserService
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

# 데이터베이스 클라이언트를 앱 전역에서 접근 가능하도록 저장
db_client: AsyncIOMotorClient = None

async def get_database(db_url: str= 'mongodb://root:root@test.kfs.co.kr:27017/', db_name: str='stockdb') -> AsyncIOMotorClient:
    global db_client
    if db_client is None:
        db_client = AsyncIOMotorClient(db_url)
    return db_client[db_name]

async def initialize_beanie(db):
    await init_beanie(database=db, document_models=[User])

def get_user_service(db=Depends(get_database)):
    return UserService(db)

# def get_user_service() -> UserService:
#     from ..main import app
#     return app.state.user_service
