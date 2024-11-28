from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Jangbi(Base):
    __tablename__ = "jangbi"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="id")
    ymd = Column(String(8), nullable=False, comment="구입일")
    item = Column(String(100), nullable=False, comment="품목")
    location = Column(String(200), nullable=True, comment="위치")
    cost = Column(Integer, nullable=True, comment="가격")
    spec = Column(Text, nullable=True, comment="스펙(특징)")
    lvl = Column(String(1), nullable=False, default="2", comment="등급")
    modify_dt = Column(DateTime, nullable=False, default=func.now(), comment="수정일시")
