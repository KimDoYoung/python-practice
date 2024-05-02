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
            raise ValueError("MongoDB client has not been initialized. Please call 'initialize' first.")
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client:
            cls._client.close()
            cls._client = None

# class MongoDb:
#     client: AsyncIOMotorClient = None

#     @classmethod
#     async def initialize(cls, uri: str):
#         cls.client = AsyncIOMotorClient(uri)


#     @classmethod
#     def get_client(cls):
#         return cls.client


#     @classmethod
#     def close(cls):
#         cls.client.close()