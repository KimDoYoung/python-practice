# kalpadb-api

- 기존에 있던 kalpadb(mysql) 에 대한 restful api
- frontend는 만들지 않는다.
- 짝으로 된 client는 svelte로 만들기로 한다.
- fastapi
- mysql async
- fastapi로 restful api 서버를 만들려고 함.
- mysql로 된 데이터베이스명 kalpadb가 존재함.
- localhost나 알려진 IP로 접속시에만 서비스를 제공함

# 실행

```shell
pip install -r requirements.txt
export Kalpadb_api_mode=local
uvicorn app.main:app --reload
```
