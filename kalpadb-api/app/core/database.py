from databases import Database
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.settings import config

# 비동기 데이터베이스 연결
database = Database(config.DATABASE_URL)
metadata = MetaData()

# 비동기 SQLAlchemy 엔진 생성
# 데이터베이스 URL을 비동기 형식에 맞게 변경 (mysql+aiomysql)
engine = create_async_engine(config.DATABASE_URL, echo=True)

# 세션 생성기 (비동기)
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# 비동기 데이터베이스 세션 제공
async def get_session():
    async with async_session() as session:
        yield session
