# 프로젝트명 lucy - 공모주청약(개인용)

공모주 청약과 관련한 정보를 제공한다. 개인용으로 작성됨

* 1단계 개발
    1. 공모주 청약일정
    2. 예상체결가 산정
    3. 38커뮤니티 등에서 데이터를 가져온다.(배치)
    4. 정해진 일시에 자동으로 주식매매을 수행한다.
    5. cron기능을 가지고 있어서 정해진 시간에 특정사이트에서 scrapping을 한다.

* 2단계 개발
  1. 계좌관리
  2. 수익금관리

## 기술스택

* backend

1. python, fastapi, uvicorn
2. mongodb
   1. db : stockdb
   2. collections : users, ipo, ipo_scrap_38, configs, holiday

3. async db : use beanie
4. pytest
5. jwt 인증

* frontend

1. jquery 사용, ajax는 pure javascript의 fetch사용
2. handlebar-template사용
3. bootstrap5 사용

## 기술적 고찰

1. pytest로 async db test가 잘되지 않는다.
2. mongodb의 collection와 beanie의 클래스명을 일치시키자

## 주요기능

1. batch(scheduler)로 site [38커뮤니케이션](https://www.38.co.kr/html/fund/index.htm?o=k)에서 데이터를 가져와서 mongodb의 collection을 채운다
2. 공공openapi [공휴일정보](http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo)를 가져와서 collection days에 채운다
3. 가져온 데이터로 일정을 달력에 보여준다.
4. 가져온 데이터로 예상체결가를 산정해 본다.

## 프로그램 설명

## 실행환경

```bash
    export LUCY_MODE=local
    uvicorn backend.main:app --reload --port $PORT
```

### config.py

* LUCY_MODE=local 과 같이 설정된 파일로 .env.local 파일을 읽는다.

* DB설정값,로그파일
* config.DB_URL 과 같이 사용

### logger.py

```python
from backend.app.core.logger import get_logger
logger = get_logger(__name__)

logger.debug(...) 

```

### login

* login.html에서 fetch로 username, password를 보낸다.
* /login 에서

### calendar

* holiday, ipo, user

1. holiday->빨간색
2. ipdo event에서
   1. 6글짜이상...
   2. "일"자 빼기
   3. 청약일 파란색
   4. 납일일 회색
   5. 환불일 회색
   6. 상장일 빨간색

## history

2024-05-21 : 프로젝트 시작

## todo

1. calendar에 조회해서 공휴일과 일정넣기
2. cron에 걸기
   * 공휴일
   * 38사이트
   * 주달
3.
