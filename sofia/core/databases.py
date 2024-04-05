from databases import Database
from sqlalchemy import create_engine, text

class DatabaseConnection:
    def __init__(self, database_url):
        self.database = Database(database_url)


    async def connect(self):
        await self.database.connect()

    async def create_tables(self):
        # 이미지 파일 테이블 생성
        queries = ["""
        CREATE TABLE IF NOT EXISTS image_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            org_name TEXT NOT NULL,
            hash_code TEXT NOT NULL,
            seq INTEGER NOT NULL,
            folder_id INTEGER, 
            image_format TEXT NOT NULL,
            image_width INTEGER NOT NULL,
            image_height INTEGER NOT NULL,
            image_mode TEXT NOT NULL,
            color_palette TEXT,
            camera_manufacturer TEXT,
            camera_model TEXT,
            capture_date_time TEXT,
            shutter_speed REAL,
            aperture_value REAL,
            iso_speed INTEGER,
            focal_length REAL,
            gps_latitude REAL,
            gps_longitude REAL,
            image_orientation TEXT,
            FOREIGN KEY (folder_id) REFERENCES image_folders(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS image_folders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_name TEXT NOT NULL,
            last_load_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            note TEXT
        )
        """
        ]
        for query in queries:
            await self.database.execute(query=query)

    async def disconnect(self):
        # 데이터베이스 연결 해제 코드 (비동기 처리 필요시 여기 수정)
        await self.engine.dispose()
