import pytest
from datetime import datetime
from fastapi import FastAPI
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from backend.app.domains.logs.logs_model import Logs, LogQueryParams
from backend.app.domains.logs.logs_service import LogsService
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

# FastAPI 앱 생성
app = FastAPI()

# MongoDB 설정
mongodb_url = "mongodb://root:root@test.kfs.co.kr:27017/"
db_name = "test_db"


# MongoDB 초기화
async def init_db():
    client = AsyncIOMotorClient(mongodb_url)
    await init_beanie(database=client[db_name], document_models=[Logs])

@app.on_event("startup")
async def on_startup():
    await init_db()

# LogsService 인스턴스 생성
logs_service = LogsService()

# Lifespan 이벤트 핸들러 추가
@app.on_event("lifespan")
async def lifespan(app: FastAPI):
    await init_db()
    yield
    # Shutdown actions if any
    # e.g., close MongoDB connection


# 테스트 클라이언트 설정
client = TestClient(app)

# LogsService 인스턴스 생성
logs_service = LogsService()

# 테스트 데이터 생성
@pytest.fixture
async def test_log_data():
    log_data = {
        "at_time": datetime.now(),
        "user_id": "test_user",
        "stk_abbr": "TEST",
        "acct_no": True,
        "message": "This is a test log"
    }
    return log_data

# LogsService 테스트
@pytest.mark.asyncio
async def test_create_log(test_log_data):
    # 로그 생성
    created_log = await logs_service.create(await test_log_data)
    
    assert created_log is not None
    assert created_log.user_id == test_log_data["user_id"]
    assert created_log.message == test_log_data["message"]

@pytest.mark.asyncio
async def test_get_all_logs(test_log_data):
    # 로그 생성
    await logs_service.create(await test_log_data)
    
    # 모든 로그 조회
    query_params = LogQueryParams()
    logs = await logs_service.get_all(query_params)
    
    assert len(logs) > 0

@pytest.mark.asyncio
async def test_get_logs_with_filters(test_log_data):
    # 로그 생성
    await logs_service.create(await test_log_data)
    
    # 필터를 사용하여 로그 조회
    query_params = LogQueryParams(user_id="test_user", acct_no=True)
    logs = await logs_service.get_all(query_params)
    
    assert len(logs) > 0
    assert logs[0].user_id == "test_user"
    assert logs[0].acct_no == True

@pytest.mark.asyncio
async def test_count_logs(test_log_data):
    # 로그 생성
    await logs_service.create(await test_log_data)
    
    # 로그 개수 조회
    count = await logs_service.count()
    
    assert count > 0

