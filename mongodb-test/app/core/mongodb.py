from motor.motor_asyncio import AsyncIOMotorClient

class MongoDb:
    client: AsyncIOMotorClient = None

    @classmethod
    def initialize(cls, uri: str):
        cls.client = AsyncIOMotorClient(uri)


    @classmethod
    def get_client(cls):
        return cls.client


    @classmethod
    def close(cls):
        cls.client.close()