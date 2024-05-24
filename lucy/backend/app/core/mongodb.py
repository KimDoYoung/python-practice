from motor.motor_asyncio import AsyncIOMotorClient

class MongoDb:
    _client: AsyncIOMotorClient = None

    @classmethod
    async def initialize(cls, uri: str):
        if cls._client is None:
            cls._client = AsyncIOMotorClient(uri)

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
