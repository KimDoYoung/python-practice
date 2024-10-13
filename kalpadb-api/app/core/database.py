from databases import Database
from sqlalchemy import create_engine, MetaData
from app.core.settings import config

# 비동기 데이터베이스 연결
database = Database(config.DATABASE_URL)
metadata = MetaData()

# 데이터베이스 엔진 생성 (비동기 데이터베이스를 위한 엔진)
engine = create_engine(config.DATABASE_URL)

# 비동기 데이터베이스 연결을 위한 세션 제공
async def get_session():
    async with database.transaction():
        yield database
