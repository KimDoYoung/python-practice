# 프로젝트명 lucy - 공모주청약(개인용)

공모주 청약과 관련한 정보를 제공한다. 개인용으로 작성됨

* 1단계 개발
    1. 공모주 청약일정
    2. 예상체결가 산정
    3. 38커뮤니티 등에서 데이터를 가져온다.(배치)
   
* 2단계 개발
  1. 계좌관리
  2. 수익금관리 

## 기술스택

* backend
1. python, fastapi, uvicorn
2. mongodb
   1. db : stockdb
   2. collections : users, ipo, ipo_scrap_38, configs
   
3. async db : use beanie
4. pytest 
5. jwt 인증


* frontend
1. jquery 사용, ajax는 pure javascript의 fetch사용
2. handlebar-template사용
3. bootstrap5 사용



## 주요기능

1. batch(scheduler)로 site [38커뮤니케이션](https://www.38.co.kr/html/fund/index.htm?o=k)에서 데이터를 가져와서 mongodb의 collection을 채운다
2. 공공openapi [공휴일정보](http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo)를 가져와서 collection days에 채운다
3. 가져온 데이터로 일정을 달력에 보여준다.
4. 가져온 데이터로 예상체결가를 산정해 본다.


## history

2024-05-21 : 프로젝트 시작

