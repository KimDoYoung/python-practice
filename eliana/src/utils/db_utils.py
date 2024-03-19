#
# 데이데베이스
#
from contextlib import contextmanager
import hashlib
import json
from typing import Iterator
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Index, UniqueConstraint, create_engine
from sqlalchemy.orm import sessionmaker
# chart_history.py
from sqlalchemy import DateTime,  Column, Integer, String, Text,  func
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session as SQLAlchemySession

# from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite:///eliana.db"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

SessionLocal  = sessionmaker(autoflush=False, bind=engine)

class ChartHistory(Base):
    __tablename__ = 'chart_history'
    id = Column(Integer, primary_key=True, comment="자동증가")
    user_id = Column(String(50), nullable=False, default='ELIANA', comment="사용자id")
    chart_type = Column(String(20), nullable=False, comment="chart 종류")
    json_data = Column(Text, nullable=False, comment="입력 json")
    json_hash = Column(String(100), nullable=False, comment="json hashcode")
    url = Column(String(200), nullable=False, comment="생성된 url")
    created_on = Column(DateTime, nullable=False, default=func.now(), comment="생성일시")
    __table_args__ = (
        UniqueConstraint('json_hash', name='_json_uc'),
        Index('ix_json_hash', 'json_hash'),  # 인덱스 추가
    )

    def __init__(self, user_id, chart_type, json_data, json_hash, url):
        self.user_id = user_id
        self.chart_type = chart_type
        self.json_data = json_data
        self.json_hash = json_hash
        self.url = url

    def __repr__(self):
        return f"User ID: {self.user_id}, Chart Type: {self.chart_type}, JSON: {self.json_data}, JSON_HASH: {self.json_hash}, URL: {self.url}, Created On: {self.created_on}"

class ChartSample(Base):
    __tablename__ = 'chart_sample'
    id = Column(Integer, primary_key=True, comment="자동증가")
    chart_type = Column(String(20), nullable=False, comment="chart 종류")
    title = Column(String(100), nullable=False, comment="chart 제목")
    json_data = Column(Text, nullable=False, comment="입력 json")
    note = Column(String(1000), nullable=False, comment="chart 설명")
    created_on = Column(DateTime, nullable=False, default=func.now(), comment="생성일시")

    def __init__(self, chart_type, title, json_data, note):
        self.chart_type = chart_type
        self.title = title
        self.json_data = json_data
        self.note = note

    def __repr__(self):
        return f"Chart Type: {self.chart_type}, Title : {self.title}, JSON: {self.json_data}, Note: {self.note}, Created On: {self.created_on}"


def get_db() -> Iterator[SQLAlchemySession]:
    db = SessionLocal ()
    try:
        yield db
    finally:
        db.close()

# `get_db` 함수를 사용하여 데이터베이스 세션을 관리하는 컨텍스트 매니저를 정의합니다.
@contextmanager
def db_session():
    db = next(get_db())
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

def add_chart_history(chart_history):
    session = SessionLocal ()
    try:
        session.add(chart_history)
        session.commit()
    except IntegrityError:
        session.rollback()
    finally:
        session.close()

def calculate_request_hash(chart_request):
    # Pydantic 객체를 dict로 변환
    # request_dict = chart_request.dict()
    request_dict = chart_request
    # dict를 JSON 문자열로 변환. 키 정렬 옵션을 사용해 순서를 보장
    request_json = json.dumps(request_dict, sort_keys=True)
    # JSON 문자열의 SHA-256 해시를 계산
    hash_object = hashlib.sha256(request_json.encode())
    hex_dig = hash_object.hexdigest()
    
    return hex_dig


def get_chart_samples_by_type(chart_type: str,db: SQLAlchemySession = Depends(get_db) ):
    chart_samples = db.query(ChartSample)\
                    .filter(ChartSample.chart_type == chart_type)\
                    .order_by(ChartSample.created_on.desc())\
                    .all()
    return chart_samples

def delete_chart_histories(db: SQLAlchemySession, user_id: str = None, chart_type: str = None):
    try:
        query = db.query(ChartHistory)
        
        # `user_id`가 제공된 경우, 쿼리에 필터 추가
        if user_id:
            query = query.filter(ChartHistory.user_id == user_id)
        
        # `chart_type`이 제공된 경우, 쿼리에 필터 추가
        if chart_type:
            query = query.filter(ChartHistory.chart_type == chart_type)

        # 조건에 맞는 레코드를 삭제
        query.delete(synchronize_session=False)
        
        # 변경사항을 데이터베이스에 커밋
        db.commit()
    except Exception as e:
        # 에러가 발생한 경우, 롤백
        db.rollback()
        raise e


Base.metadata.create_all(engine)