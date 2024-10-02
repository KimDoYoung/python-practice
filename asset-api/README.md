# Asset-Api

## url 구상

- api.kfs.co.kr/asset-erp/v1/get-auth

## table
```sql
DROP TABLE IF EXISTS ifi01_company;
CREATE TABLE IF NOT EXISTS ifi01_company  (
    company_id BIGINT NOT NULL,             		-- 회사 ID (예: 회사 이름 또는 고유 식별자)
    service_nm VARCHAR(100) NOT NULL,             	-- 서비스 명칭 (예: 서비스 이름 또는 고유 식별자)
    start_ymd VARCHAR(8) NOT NULL,                	-- 서비스 시작 일자
    end_ymd VARCHAR(8) NOT NULL DEFAULT '99991231', -- 서비스 종료 일자
    app_key VARCHAR(64) NOT NULL,                 	-- 랜덤으로 생성된 appKey (회사에 제공한 고유 키)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 레코드 생성 일자
    PRIMARY KEY(company_id, service_nm)
);


-- 회사 ID, 서비스 ID, 시작일자를 기반으로 고유한 조합을 만들어주는 인덱스 추가 (선택 사항)
-- CREATE UNIQUE INDEX idx_company_service_unique ON company_service (company_id, service_id, start_date);
```