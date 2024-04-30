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
export PYTHONPATH=/c/Users/deHong/Documents/kdy/python-practice/mongodb-test && pytest ./tests
```
### 주의 할 점
1. AsyncClient를 사용해야한다.
2. @pytest.mark.asyncio를 사용해야한다ㅣ
