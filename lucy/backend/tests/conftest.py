import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from backend.app.domains.system.eventdays_model import EventDays
from backend.app.core.config import config


# import pytest
# from motor.motor_asyncio import AsyncIOMotorClient
# from beanie import init_beanie
# from backend.app.domains.system.eventdays_model import EventDays

@pytest.fixture(scope="module")
async def db_client():

    url = 'mongodb://root:root@test.kfs.co.kr:27017/'
    client = AsyncIOMotorClient(url)
    await init_beanie(database=client.test_stockdb, document_models=[EventDays])
    yield client
    client.close()

@pytest.fixture(scope="function", autouse=True)
async def clear_database(db_client):
    yield
    await db_client.test_stockdb.eventdays.drop()
