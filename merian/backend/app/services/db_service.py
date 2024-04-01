from contextlib import asynccontextmanager
from typing import AsyncIterator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from backend.app.core.configs import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession


# 비동기 엔진 생성
async_engine = create_async_engine(DATABASE_URL, echo=True)

# 비동기 세션 팩토리 생성
AsyncSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=async_engine, 
    class_=AsyncSession
)

Base = declarative_base()

@asynccontextmanager
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session

@asynccontextmanager
async def db_session():
    """비동기 컨텍스트 매니저는 스크립트나 배치 작업에서 SQLAlchemy 비동기 세션을 사용할 때 유용합니다."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"An error occurred: {e}")
            raise
