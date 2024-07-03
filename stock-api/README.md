# Stock-Api

## 개요

1. KIS, LS 등 Restful api를 지원하는 증권사를 대상
2. 사용자는 운용사이다
3. 사용자는 KIS에 n개 이상의 계좌를 가지고 있다.
4. backend와 frontend를 동시에 가지고 있다.
5. 사용자는 restful방식으로 주식관련 작업수행
6. Websocket으로 체결통보만을 받는다. (호가, 체결가 websocket서비스는 개발안함)
7. client는 AssetErp가 됨
8. security는 없슴. 단 ip 체크로  client가  AssetErp인지만을 체크

## 기술스택

- backend
  - fastapi
  - mongodb (beanie)
  - jinja2
  
- frontend
  - boostrap5
  - handlebar

## 실행

```shell
export STOCK_API_MODE=local
python backend/main.py
```

## database

1. 데이터베이스명 :  StockApiDb
2. collection : Users, Logs

## 고려할 점

1. mongo db->postgresql로 변경 될 수 있슴
