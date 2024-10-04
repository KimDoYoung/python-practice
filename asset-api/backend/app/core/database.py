from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.settings import config

DATABASE_URL = config.DB_URL

# Async SQLAlchemy 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)

# 세션 만들기
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    async with async_session() as session:
        yield session
