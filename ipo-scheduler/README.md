# IPO-scheduler

- ipo_scheduler에서 불필요한 것들 제거, ipo관련된 것들만 남김
- 포트를 8881로 변경함
- 데이타베이스명을 ipo-scheduer로 함.
- export IPO_SCHEDULER_MODE=real 로 서버에서 설정
- jskn의 몽고db는 docker로 실행됨
  ```shell
  docker run -d --name mongodb-container -p 27017:27017 -v /home/kdy987/fastapi/mongodb:/data/db mongo:4.4
  ```
## 빌드

### 고려할 점

1. 몽고DB의 데이터는 volume으로 정의되어서  DB가 유지되어야한다.
2. 몽코DB의 초기데이터들은 load되어야한다.
3. ipo_scheduler가 사용하는 데이터들은 volume으로 정의되어서 유지되어야한다.
4. ipo_scheduler로그는 tail -f로 모니터링되어야한다.
5. 서버시간과 container안의 fastapi서버의 시간은 동기화되어야한다.
   - scheduler가 제시간에 동작한다.
6. container안에 chrome driver가 설치되어야 judal을 가져올 수 있다.
7. 방화벽이 open되어야한다. 8000 서버, 27017 몽고는 보안상 오픈하지 않아야한다.
   - 단 초기에 모니터링하기 위해서 오픈한다.

- docker의 container로 실행한다.
- backend/Dockerfile
- docker-compose.yml
- .env.real
- mongo_collections.json들
  
```shell
cd python-practice/ipo_scheduler
docker-compose down     # 기존 컨테이너 종료
docker-compose build    # 새로 빌드
docker-compose up -d    # 백그라운드에서 다시 실행

docker-compose restart  # python만 변경된 경우
docker cp ./initial_data.json ipo_scheduler-mongo:/data/initial_data.json
- stockdb.Config.json
- stockdb.SchedulerJob.json
- stockdb.Users.json

- docker-compose build
- db설정
```

## jskn에 배포

- .env.real을 만들어야한다.
- 초기 몽고db를 위한 json을 만들어야한다.
- /root/fastapi-data/kdydata에 json파일3개, .env.real을 가져다 놓음
- 몽고db의 id/pw을 넣어야하지 않나?

- 방화벽열기

  ```shell
    # FastAPI 포트 8000 열기
    sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent

    # MongoDB 포트 27017 열기 (필요한 경우에만)
    sudo firewall-cmd --zone=public --add-port=27017/tcp --permanent

    # 방화벽 재시작
    sudo firewall-cmd --reload
  ```

- 공유기 포트포워드
  8000, 27017 포트를 foreward해야 함.

## 기술스택

- backend

1. python, fastapi, uvicorn
2. mongodb
   1. db : stockdb
   2. collections : users, ipo, ipo_scrap_38, configs, holiday

3. async db : use beanie
4. pytest
5. jwt 인증

- frontend

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
    export ipo_scheduler_MODE=local
    uvicorn backend.main:app --reload --port $PORT
```

### config.py

- ipo_scheduler_MODE=local 과 같이 설정된 파일로 .env.local 파일을 읽는다.

- DB설정값,로그파일
- config.DB_URL 과 같이 사용

## naming

### model

- Response -> Collection과 같은 명칭을 사용
- Request 를 붙인다.

```python
class DbConfigRequest(BaseModel):
    mode:str
...
class DbConfig(Document):
    ...
    class Settings:
            name = "Config" 
```

## scheduler

### 관련 모듈들

1. judal_scrap_1.py

   - judal 사이트에서 모든 데이터를 가져와서
   - config DATA폴더 하위의 judal 밑에 날짜시간으로 넣는다.

2. s38_2.py

    - ipo_scrap_38 collection을 모두 지운다.

        - history를 가져가지 않는다. 지난 간 것은 그냥 없는 것으로
        - scrapping 로직이 오류를 일으키면 버그인 것으로

    - 38커뮤니케이션에서 1,2 페이지를 가져와서
    - ipo_scrap_38 collection에 채운다.

3. f38_2.py
    - ipo collection을 모두 지운다.
    - ipo_scrap_38 collection에서 Ipo collection으로 데이터를 옮긴다.
    - 옮기면서 **판정정보**를 채운다.

### 호출

- /api/v1/scheduler/run/scrap_judal

## dependency.py

- 서비스 객체를 router 함수에서 주입시키기 위해서 사용

```text
functools.lru_cache 데코레이터를 사용할 수 있습니다. 이 데코레이터는 한 번 생성된 객체를 캐시하여 이후 호출 시 캐시된 객체를 반환합니다.
```

### logger.py

```python
from backend.app.core.logger import get_logger
logger = get_logger(__name__)

logger.debug(...) 

```

### login

- login.html에서 fetch로 username, password를 보낸다.

### calendar

- holiday, ipo, user

1. holiday->빨간색
2. ipdo event에서
   1. 6글짜이상...
   2. "일"자 빼기
   3. 청약일 파란색
   4. 납일일 회색
   5. 환불일 회색
   6. 상장일 빨간색
3. div click 각 event클릭
4. url과 종목코드 가져가기
5. 이번달이 아닌것은 이태리체로.

## history

2024-05-21 : 프로젝트 시작

## todo

1. calendar에 조회해서 공휴일과 일정넣기
2. div click
3. cron에 걸기
   - 공휴일
   - 38사이트
   - 주달
4. 현재 나의 계좌잔고
5. 현재 보유 주식
6. 매수
7. 매도
8. 약정매수
9. 약정매도
10. 회사규모, 경쟁률, 장외가격
11. docker로 말아보기
12.

## DantaService

1. 09:00에 시작한다.
2. 15:30에 종료한다.
