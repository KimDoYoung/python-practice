# Asset-Api

## url 구상

- api.kfs.co.kr/asset-erp/v1/get-auth

## table

- localhost, kdy987/kalpa987! 로 접속 테스트

```sql
DROP TABLE IF EXISTS ifi01_company;
CREATE TABLE IF NOT EXISTS ifi01_company  (
    company_id BIGINT NOT NULL,               -- 회사 ID (예: 회사 이름 또는 고유 식별자)
    service_nm VARCHAR(100) NOT NULL,              -- 서비스 명칭 (예: 서비스 이름 또는 고유 식별자)
    start_ymd VARCHAR(8) NOT NULL,                 -- 서비스 시작 일자
    end_ymd VARCHAR(8) NOT NULL DEFAULT '99991231', -- 서비스 종료 일자
    app_key VARCHAR(64) NOT NULL,                  -- 랜덤으로 생성된 appKey (회사에 제공한 고유 키)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 레코드 생성 일자
    PRIMARY KEY(company_id, service_nm)
);

-- 회사 ID, 서비스 ID, 시작일자를 기반으로 고유한 조합을 만들어주는 인덱스 추가 (선택 사항)
-- CREATE UNIQUE INDEX idx_company_service_unique ON company_service (company_id, service_id, start_date);
```

## app_key, app_secret_key 2가지 발급

- KFS가 제공하는 openapi 서비스에 등록한 회사는 app_key를 발급받는다.
- 이하 **서비스에 등록한 회사**는 **미래에셋**으로 기술한다.
- app_key는 랜덤한 알파벳숫자로 길이 64이다.
- app_key는 db에 저장된다.
- app_secret_key는 app_key + company_id + service_nm + start_ymd 를 aes암호화하여 생성한다.
- 이때 암호화에 사용되는 키는 env.profile에 저장되어 있다. (예 : 'kfs-restful-zaq1@WSX)
- 생성된 app_secret_key는 db에 저장되지 않는다.
- 미래에셋은 app_key와  app_secret_key를 제공받는다.
- 미래에셋은 url /auth 에 접속한다. 이때 header에 제공받은 app_key와 app_secret_key를 함께 보낸다.
- 검증 및 token발급로직에서 app_key로 db에서 검색한다.
- 검색 후 app_key+ company_id + service_nm + start_ymd 를 소스에 존재하는 암호화키로  aes암호화한다.
- 그 결과와 header에서 보내 온 app_secret_key를 비교하여 검증한다.
- 검증완료된 후 jwt key를 발급환다.
- jwt key는 24시간 유효하다.

### API Key 발급 및 검증 문서

1. 개요
KFS가 제공하는 OpenAPI 서비스에 등록한 회사는 **app_key**와 **app_secret_key**를 발급받아야 합니다.
이 문서에서는 미래에셋을 예시로 설명합니다.

1. app_key 및 app_secret_key 발급
**app_key**는 랜덤한 64자 길이의 알파벳 및 숫자 조합으로 생성됩니다.
**app_key**는 KFS의 데이터베이스(DB)에 저장되며, 각 회사에 고유한 키로 사용됩니다.
**app_secret_key**는 **company_id + service_nm + start_ymd**를 AES 암호화하여 생성됩니다.
이때 암호화 키는 소스 코드에 포함된 고정 키를 사용합니다. (예: 'kfs-restful-zaq1@WSX')
**app_secret_key**는 DB에 저장되지 않습니다.
미래에셋은 API 사용을 위해 발급받은 **app_key**와 **app_secret_key**를 제공받습니다.

1. 인증 요청 절차
미래에셋은 /auth URL로 접속하여 **app_key**와 **app_secret_key**를 HTTP 헤더에 포함해 요청을 보냅니다.
헤더에는 다음과 같은 정보가 포함됩니다:
app_key: 발급받은 64자리 랜덤 키
app_secret_key: 발급받은 AES 암호화된 키

1. 검증 및 토큰 발급 로직
KFS 서버는 요청이 들어오면, **app_key**를 기반으로 DB에서 해당 회사 정보를 조회합니다.
조회한 company_id, service_nm, start_ymd 정보를 소스 코드에 저장된 암호화 키(예: 'kfs-restful-zaq1@WSX')를 사용해 AES 암호화하여 동적으로 app_secret_key를 생성합니다.
생성된 app_secret_key와 **헤더로 전달된 app_secret_key**를 비교하여 일치하는지 검증합니다.
검증이 성공하면, JWT(JSON Web Token) 기반의 Access Token을 발급하여 응답합니다.

## 폴더구조

```shell
mkdir -p backend/app/api/v1/endpoints
mkdir -p backend/app/core
mkdir -p backend/app/domain
mkdir -p backend/app/utils
touch backend/main.py
mkdir -p doc
mkdir -p frontend/public
mkdir -p frontend/views/common
mkdir -p frontend/views/template
```
