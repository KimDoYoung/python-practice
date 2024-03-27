-- collections 스키마에 키보드 정보를 저장하는 테이블 생성
DROP TABLE IF EXISTS collections.keyboard;
CREATE TABLE IF NOT EXISTS  collections.keyboard (
    id serial4 PRIMARY KEY, -- 키보드 ID
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
COMMENT ON COLUMN collections.keyboard.id IS '자동생성키';
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


DROP TABLE IF EXISTS public.file_collection_match;
CREATE TABLE IF NOT EXISTS public.file_collection_match (
 category varchar(100) not NULL DEFAULT 'keyboard', 
 id serial4 not null, -- keyboard id
 file_id serial4  not NULL, -- file_id
 PRIMARY KEY (category, id, file_id)
);

delete from public.edi_user where id='user1';
INSERT INTO public.edi_user (id,pw,nm,email,created_by)values('user1','$2b$12$C/MeW1GIhMe/W1nK45g7u.B.MrPzg4xQQDWFXZdCXYCfIA1xkClP2','김도영','kdy987@gmail.com','system');


-- public.fb_file definition

-- Drop table

-- DROP TABLE public.fb_file;

CREATE TABLE public.fb_file (
	file_id serial4 NOT NULL,
	node_id int4 NOT NULL,
	phy_folder varchar(300) NOT NULL,
	phy_name varchar(300) NOT NULL,
	org_name varchar(300) NOT NULL,
	mime_type varchar(100) NULL,
	file_size int4 NULL,
	ext varchar(50) NULL,
	note varchar(1000) NULL,
	width int4 NULL,
	height int4 NULL,
	status bpchar(1) NOT NULL DEFAULT 'N'::bpchar,
	create_on timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	create_by varchar(30) NULL,
	CONSTRAINT pk_fb_file PRIMARY KEY (file_id)
);


-- public.fb_file foreign keys

ALTER TABLE public.fb_file ADD CONSTRAINT fk_node_id FOREIGN KEY (node_id) REFERENCES public.fb_node(node_id) ON DELETE RESTRICT;
