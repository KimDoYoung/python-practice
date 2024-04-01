# Merian

## 개요

1. 수집한 키보드  정보를 관리
    1. 키보드 정보를 테이블 keyboard를 통해서 관리
    2. 키보드와 관련된 이미지 파일을 관리
2. 최대한 chatGPT가 소스를 생성하게 한다
3. python으로 open api사용법을 정립

## 폴더구조

1. backend : Python 백엔드
2. frontend : 웹 프런트 엔드
3. js_test : javascript jest 테스트

## virtual 환경 설정

- make_merian_folders.sh : 폴더 구조를 생성하는 bash shell 프로그램
- python -m venv env
- source .env/Scripts/activate

## env 환경

- .env.local, .env.real 로 설정
- .gitignore에 설정
- main.py, constants.py에서만 사용, 기타 프로그램에서는 constants것을 사용

- .env.local

```text
# Database URL
DB_URL="postgresql+asyncpg://kdy987:kalpa987!@localhost:5432/fbhdb"

# PORT
PORT=8686
```

## 실행환경

```bash
    export MERIAN_MODE=local
    uvicorn backend.main:app --reload --port $PORT
```

## 디버깅

- launch.json

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "backend.main:app",
                "--reload",
                "--port",
                "8686"  // 원하는 포트 번호로 변경
            ],
            "jinja": true
        }
    ]
} 
```

## Table DDL & test data

```sql
-- collections 스키마에 키보드 정보를 저장하는 테이블 생성
DROP TABLE IF EXISTS collections.keyboard;
CREATE TABLE IF NOT EXISTS  collections.keyboard (
    product_name VARCHAR(100), -- 제품명
    manufacturer VARCHAR(100), -- 제조사
    purchase_date VARCHAR(8), -- 구입일 (YYYYMMDD 형식)
    purchase_amount BIGINT, -- 구입금액
    key_type VARCHAR(10), -- 키 타입 (예: 메카닉, 메모리스)
    switch_type VARCHAR(20), -- 스위치 타입 (예: Cherry MX, Topre)
    actuation_force VARCHAR(10), -- 작동 압력
    interface_type VARCHAR(30), -- 인터페이스 타입 (예: USB, 블루투스)
    overall_rating INT, -- 종합적 평가 (1~10)
    typing_feeling TEXT, -- 타이핑 감각
   create_on timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 create_by varchar(30) NULL

);

-- 테이블에 주석 추가
COMMENT ON TABLE collections.keyboard IS '키보드 정보를 저장하는 테이블';

-- 각 열에 주석 추가
COMMENT ON COLUMN collections.keyboard.product_name IS '제품명';
COMMENT ON COLUMN collections.keyboard.manufacturer IS '제조사';
COMMENT ON COLUMN collections.keyboard.purchase_date IS '구입일 (YYYYMMDD 형식)';
COMMENT ON COLUMN collections.keyboard.purchase_amount IS '구입금액';
COMMENT ON COLUMN collections.keyboard.key_type IS '키 타입 (예: 메카닉, 메모리스)';
COMMENT ON COLUMN collections.keyboard.switch_type IS '스위치 타입 (예: Cherry MX, Topre)';
COMMENT ON COLUMN collections.keyboard.actuation_force IS '작동 압력';
COMMENT ON COLUMN collections.keyboard.interface_type IS '인터페이스 타입 (예: USB, 블루투스)';
COMMENT ON COLUMN collections.keyboard.overall_rating IS '종합적 평가 (1~10)';
COMMENT ON COLUMN collections.keyboard.typing_feeling IS '타이핑 감각';
COMMENT ON COLUMN collections.keyboard.create_on IS '생성일';
COMMENT ON COLUMN collections.keyboard.create_by IS '생성자';

-- 
DROP TABLE IF EXISTS public.file_collection_match;
CREATE TABLE IF NOT EXISTS public.file_collection_match (
 category varchar(100) not NULL DEFAULT 'keyboard', --  'keyboard'
 id serial4 not null, -- keyboard id
 file_id serial4  not NULL, -- file_id
 PRIMARY KEY (category, id, file_id)
);

INSERT INTO public.edi_user (id,pw,nm,email,created_by)values('user1','$2b$12$C/MeW1GIhMe/W1nK45g7u.B.MrPzg4xQQDWFXZdCXYCfIA1xkClP2','김도영','kdy987@gmail.com','system');
```

## 테스트 시나리오

### CRUD

1. insert
   1. "한성1" 추가, 파일첨부 없음
   2. "한성1" 수정, 파일첨부 1개
   3. "한성1" 수정, 파일첨부 2개, 기존1개 삭제
   4. "한성1" 삭제
   5. 물리적 파일없어야함.
