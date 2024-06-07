import pytest
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.domains.system.mystock_service import MyStockService
from backend.app.domains.system.mystock_model import MyStock, MyStockDto
from httpx import AsyncClient
from fastapi import FastAPI, Depends

# 가상 MongoDB 설정
@pytest.fixture(scope="module")
async def db():
    client = AsyncIOMotorClient("mongodb://root:root@test.kfs.co.kr:27017/")
    db = client["test_stockdb"]
    await init_beanie(database=db, document_models=[MyStock])
    yield db
    client.drop_database("test_stockdb")
    client.close()

# FastAPI 앱 설정
@pytest.fixture(scope="module")
def app():
    app = FastAPI()

    @app.post("/add")
    async def add_mystock(request: MyStockDto, mystock_service: MyStockService = Depends()):
        mystock = await mystock_service.upsert(request)
        return mystock

    @app.delete("/delete/{id}")
    async def delete_mystock(id: str, mystock_service: MyStockService = Depends()):
        success = await mystock_service.delete_by_id(id)
        return {"success": success}

    return app

# 테스트 클라이언트 설정
@pytest.fixture(scope="module")
async def client(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# MyStockService 인스턴스 설정
@pytest.fixture(scope="module")
async def mystock_service(db):
    return MyStockService()

# 테스트 함수
@pytest.mark.asyncio
async def test_create_mystock(client: AsyncClient, mystock_service: MyStockService):
    mystock_dto = MyStockDto(stk_code="123456", stk_name="Test Stock", stk_types=["보유"])
    response = await client.post("/add", json=mystock_dto.model_dump())
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["stk_code"] == "123456"
    assert response_data["stk_name"] == "Test Stock"
    assert response_data["stk_types"] == ["보유"]

@pytest.mark.asyncio
async def test_upsert_mystock(client: AsyncClient, mystock_service: MyStockService):
    mystock_dto = MyStockDto(stk_code="123456", stk_name="Upsert Test", stk_types=["관심"])
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await client.post("/add", json=mystock_dto.model_dump())
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["stk_code"] == "123456"
    assert response_data["stk_name"] == "Upsert Test"
    assert "관심" in response_data["stk_types"]

    # 업서트 테스트
    mystock_dto.stk_types.append("공모주")
    response = await client.post("/add", json=mystock_dto.model_dump())
    assert response.status_code == 200
    response_data = response.json()
    assert "공모주" in response_data["stk_types"]
