# mongodb-test

- 몽고 db 연결 및 python에서의 사용 테스트
- fastapi

1. async로 연결가능
2. docker로 mongodb만들기
3. fastapi 로 user CRUD

## 설치

1. pymongo설치 : pip install pymongo
2. test.kfs.co.kr 에 docker로 mongodb설치

## api

post /api/user
get /api/user/{id}
get /api/user
put /api/user
delete /api/user/{id}

## Run application

- run.py 사용
- python run.py
  
## pytest

```bash
export PYTHONPATH=/c/Users/deHong/Documents/kdy/python-practice/mongodb-test && pytest -p no:warnings ./tests
export PYTHONPATH=/c/Users/deHong/Documents/kdy/python-practice/mongodb-test && pytest ./tests
```

### 주의 할 점

1. AsyncClient를 사용해야한다.
2. @pytest.mark.asyncio를 사용해야한다.
3. 여러개를 할때 event loop 에러가 난다
4. fixture로 db연결을 하는 것 실패

```python
@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

async def db_init():
    await MongoDb.initialize("mongodb://root:root@test.kfs.co.kr:27017/")
    db = MongoDb.get_client()["stockdb"]
    await init_beanie(database=db, document_models=[User])

@pytest.mark.asyncio
async def test_get_all_users(event_loop):

    await db_init()
    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        response = await async_client.get("/api/v1/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)  # 응답이 리스트 형태인지 확인

```
