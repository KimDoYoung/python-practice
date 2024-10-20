from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

class MongoDb:
    _client: AsyncIOMotorClient = None

    @classmethod
    async def initialize(cls, uri: str):
        if cls._client is None:
            cls._client = AsyncIOMotorClient(uri)

    @classmethod
    async def initialize(cls, uri: str):
        if cls._client is None:
            try:
                # MongoDB 클라이언트 초기화
                cls._client = AsyncIOMotorClient(uri)
                
                # 연결 확인 (ping 명령어)
                await cls._client.admin.command('ping')
                logger.info("MongoDB에 성공적으로 연결되었습니다.")
            except ConnectionFailure as e:
                logger.error(f"MongoDB 연결에 실패했습니다: {e}")            

    @classmethod
    def get_client(cls):
        if cls._client is None:
            raise ValueError("몽고DB가 아직 초기화되지 않음. 'initialize'를 호출하세요.")
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client:
            cls._client.close()
            cls._client = None
