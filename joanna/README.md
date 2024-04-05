# 주식트레이딩 - joanna

## 개요

다음을 [참조로 시작](https://www.bluestones.biz/cms/pages?action=view&page=/HomePage/stock/stock_products.md)
**주식**거래만을 대상으로 한다.

## 기술스택

1. python
2. FastAPI
3. postgresql

## 기술개요

언어는 Python으로 작성하고 FastAPI를 이용해서 웹사이트를 만든다.
DB 는 postgresql을 사용한다.
각 증권사의 제공 api를 사용한다. 각 증권산의 제공 api는 REST방식도 있고, ocx(dll)을 사용하는 방식도 있다.

## 실행

```text
export JOANNA_MODE=local && uvicorn backend.main:app --reload
```

* test는 pytest를 사용하면 runtest.sh을 만들었음

> ./runtest.sh

* debugging mode로 실행
  * vscode에서 디버깅 모드로 실행  (F5)

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "backend.main:app",
                "--reload"
            ],
            "jinja": true,
        }
    ]
}
```

## 의문점

1. Access_token을 발급받아서 사용하는데 만료되었는지는 어떻게 알 수 있을까?

## 참고자료

1. [한국투자증권 API (REST)](https://apiportal.koreainvestment.com/intro)

## History

1. 2024-04-01 : 한국투자증권(REST), 키움증권(OCX)을 대상으로 관련 문서를 찾아보기 시작
