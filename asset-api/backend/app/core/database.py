"""
모듈 설명: 
    - 데이터베이스 연결 및 세션 관리 모듈
주요 기능:
    - get_session: 데이터베이스 세션 생성

작성자: 김도영
작성일: 2024-10-07
버전: 1.0
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from backend.app.core.settings import config

DATABASE_URL = config.DB_URL

# SQLAlchemy MetaData 객체 생성
metadata = MetaData()

# Async SQLAlchemy 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)

# 세션 만들기
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 세션 의존성 주입
# async def get_session():
#     async with async_session() as session:
#         yield session


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """비동기 세션을 생성하고 종료합니다."""
    async with async_session() as session:
        yield session