# Asset-Api

## url 구상

- api.kfs.co.kr/asset-erp/v1/get-auth

## 프롬프트

### 프로젝트의 시작

```text
1. 새로운 프로젝트 asset-api를 만들고 함.
2. 프로젝트의 개요
    2.1 사용자들에게 접속키를 발급함.
    2.2.접속키를 발급한 사용자는 restful방식으로 데이터를 제공받음.
3. 기술stack
    1. backend와 frontend로 나눔
    2. backend는 api url을 제공, 사용자들에게 restful방식으로 데이터를 제공함.
    3. frontend는 사용자들 리스트, 키발급과 같은 관련 화면 제공
    4. 세부 기술
        - backend
            1. python, fastapi, uvicorn
            2. postgresql
            3. async db 
            4. pytest

        - frontend
            1. jquery 사용, ajax는 pure javascript의 fetch사용
            2. handlebar-template사용
            3. bootstrap5 사용
        

asset-api 프로젝트 구상에 대한 의견은?
```

### 개발방법

swagger-ui를 이용한 문서가 아니고 사용자들에게 아래 정보와 같은 것을 보여주는 웹페이지를 만들어서 서비스를 하는게 좋을 것 같은데,
Asset-api 프로젝트를 해 감에 있어서 먼저 문서를 만들고 그것을 바탕으로 소스코드를 만들어 가는 것이 좋지 않을까 싶어        
```
기본정보
MethodPOST
실전 Domainhttps://openapi.koreainvestment.com:9443
모의 Domainhttps://openapivts.koreainvestment.com:29443
URL/oauth2/Approval
FormatJSON
Content-Type 
개요
실시간 (웹소켓) 접속키 발급받으실 수 있는 API 입니다.
웹소켓 이용 시 해당 키를 appkey와 appsecret 대신 헤더에 넣어 API를 호출합니다.

접속키의 유효기간은 24시간이지만, 접속키는 세션 연결 시 초기 1회만 사용하기 때문에 접속키 인증 후에는 세션종료되지 않는 이상 접속키 신규 발급받지 않으셔도 365일 내내 웹소켓 데이터 수신하실 수 있습니다.
LAYOUT
Request
 Header
Element	한글명	Type	Required	Length	Description
content-type	컨텐츠타입	String	N	20	application/json; utf-8
 Body
Element	한글명	Type	Required	Length	Description
grant_type	권한부여타입	String	Y	18	"client_credentials"
appkey	앱키	String	Y	36	한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.)
secretkey	시크릿키	String	Y	180	한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.)
Response
 Body
Element	한글명	Type	Required	Length	Description
approval_key	웹소켓 접속키	String	Y	286	웹소켓 이용 시 발급받은 웹소켓 접속키를 appkey와 appsecret 대신 헤더에 넣어 API 호출합니다.
Example
 Request
{
"grant_type": "client_credentials",
"appkey": "PSg5dctL9dKPo727J13Ur405OSXXXXXXXXXX",
"secretkey": "yo2t8zS68zpdjGuWvFyM9VikjXE0i0CbgPEamnqPA00G0bIfrdfQb2RUD1xP7SqatQXr1cD1fGUNsb78MMXoq6o4lAYt9YTtHAjbMoFy+c72kbq5owQY1Pvp39/x6ejpJlXCj7gE3yVOB/h25Hvl+URmYeBTfrQeOqIAOYc/OIXXXXXXXXXX"
}
 Response
{
    "approval_key": "a2585daf-8c09-4587-9fce-8ab893XXXXX"
}

```