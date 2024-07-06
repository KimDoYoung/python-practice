import asyncio
from fastapi import FastAPI, status
import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager

app = FastAPI()

async def startup():
    print("Startup")

async def shutdown():    
    print("Shutdown")

app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://localhost:8000") as test_client:
            yield test_client

@app.get("/")
async def hello_world():
    return {"hello": "world"}


@pytest.mark.asyncio
async def test_hello_world(test_client: httpx.AsyncClient):
    response = await test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json == {"hello": "world"}