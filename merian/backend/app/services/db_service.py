from contextlib import contextmanager
from typing import Iterator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession
from sqlalchemy.ext.declarative import declarative_base
import os

# 환경 변수 또는 설정 파일에서 데이터베이스 연결 정보를 로드합니다.
# 예시로 직접 문자열을 입력했으나, 실제로는 보안을 위해 환경 변수에서 가져오는 것이 좋습니다.
DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(DATABASE_URL, echo=True)  # echo=True는 SQL 로그를 출력합니다. 개발 단계에서 유용할 수 있습니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Iterator[SQLAlchemySession]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def db_session():
    """이 컨텍스트 매니저는 스크립트나 배치 작업에서 SQLAlchemy 세션을 사용할 때 유용합니다."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
        raise
    finally:
        db.close()
