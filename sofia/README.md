### 기능

1. 폴더들의 목록을 db에 가지고 있다.
2. 폴더 속에 들어 있는 이미지파일들을 읽어들여서 목록을 가지고 있다.
3. 폴더를 선택하여 들어 있는 이미지 파일들을 thumb형태로 리스트한다.
4. 폴더를 선택하여 들어 있는 이미지 파일들을 1장씩 본다. next, prev버튼으로 앞, 뒤로 이동한다.
5. 이미지파일을 1장씩 볼 때 크기를 조정할 수 있게 한다.

### 기술스택

1. FastAPI 
2. sqlite db
3. async 기법 사용
4. jinja template사용
5. tailwindcss, vanilla javascript
6. 사용자 인증,인가 기능 필요없음

### 테이블들

```sql
CREATE TABLE image_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_name TEXT NOT NULL,
    hash_code TEXT NOT NULL,
    seq int not null, -- folder안에서의 순서
    folder_id integer , 
    image_format TEXT NOT NULL,
    image_width INTEGER NOT NULL,
    image_height INTEGER NOT NULL,
    image_mode TEXT NOT NULL,
    color_palette TEXT, -- 인덱싱된 이미지가 아닐 경우 NULL일 수 있음
    camera_manufacturer TEXT,
    camera_model TEXT,
    capture_date_time TEXT, -- 'YYYY-MM-DD HH:MM:SS' 형식을 추천함
    shutter_speed REAL, -- 분수 형태로 저장되기도 하므로 REAL 타입 사용
    aperture_value REAL,
    iso_speed INTEGER,
    focal_length REAL,
    gps_latitude REAL, -- 위도
    gps_longitude REAL, -- 경도
    image_orientation TEXT, -- 가로, 세로 등의 방향
    FOREIGN KEY (folder_id) REFERENCES image_folders(id)
);

CREATE TABLE image_folders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    folder_name TEXT NOT NULL,
    last_load_time DATETIME DEFAULT CURRENT_TIMESTAMP, -- 'YYYY-MM-DD HH:MM:SS' 형식을 추천함
    note TEXT
);
```

### URL 설계

| URL | method | param or form | 기능 |
| --- | --- | --- | --- |
| /folder/load | post | folder__name | 1. image_folder에 레코드 추가, 2. folder_name에 기술된 folder에서 이미지파일들을 읽어들여서 image_files에 레코드추가 |
| /folder/{folder_id} | get | thumb=true | folder에 포함된 이미지 리스트를 리턴 , thumb=true이며 thumb스타일로 보여준다. |
| /image/{image_id} | get |  | 이미지 파일을 읽어서 stream으로 write |
| /image/info/{image_id} | get |  | 이미지 파일의 속성 즉 image_file의 columns정보를 보여준다. |
- 주의) 위 url에  api를 앞에 붙인 것은 json형태로 같은 context를 리턴

### 폴더구조

root : main.py

root> db, services,static,templates,views, viewmodels 를 둔다.

db: sofia.sqlite 

services: db 생성, db연결, db조회등 모듈

static: css,js,font,image folder를 둔다.

templates : html파일들

viewmodels :  pydantic 모델들

controller : image_file.py, image_folder.py 를 둔다.

## 프로젝트의 시작

```
  python -m venv env
  pactive
  pip install fastapi uvicorn
```