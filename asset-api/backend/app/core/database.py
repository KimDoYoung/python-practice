# database.py
"""
모듈 설명: 
    - 데이터베이스 연결 및 세션 관리 모듈
주요 기능:
    - get_session: 데이터베이스 세션 생성

작성자: 김도영
작성일: 2024-10-07
버전: 1.0
"""
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
