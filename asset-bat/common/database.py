"""
모듈 설명: 
    - 데이터베이스 연결 및 세션 관리 모듈
주요 기능:
    - fetch: 비동기 데이터 조회
    - execute: 비동기 데이터 조작 (삽입, 업데이트 등)
    - execute_many: 여러 행의 데이터를 일괄로 실행

작성자: 김도영
작성일: 2024-10-07
버전: 1.1
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any, List
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from common.settings import config

# 데이터베이스 URL 설정
DATABASE_URL = config.DB_URL

# SQLAlchemy MetaData 객체 생성 (필요한 경우 사용)
metadata = MetaData()

# 비동기 SQLAlchemy 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)

# 비동기 세션 팩토리 생성
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """비동기 세션을 생성하고 종료합니다."""
    async with async_session() as session:
        yield session

# 비동기 데이터베이스 작업 클래스
class Database:
    def __init__(self):
        self.session_factory = async_session

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[AsyncSession, None]:
        """비동기 세션을 연결하고 종료하는 컨텍스트 매니저"""
        async with self.session_factory() as session:
            yield session

    async def fetch(self, query: str, *args: Any) -> List[Any]:
        """데이터 조회 쿼리 실행 (SELECT)"""
        async with self.get_connection() as connection:
            result = await connection.execute(query, *args)
            return result.fetchall()

    async def execute(self, query: str, *args: Any) -> None:
        """데이터 조작 쿼리 실행 (INSERT, UPDATE, DELETE)"""
        async with self.get_connection() as connection:
            await connection.execute(query, *args)
            await connection.commit()

    async def execute_many(self, query: str, values: List[Any]) -> None:
        """여러 행의 데이터를 일괄로 실행"""
        async with self.get_connection() as connection:
            await connection.executemany(query, values)
            await connection.commit()
