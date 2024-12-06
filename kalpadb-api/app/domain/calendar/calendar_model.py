from sqlalchemy import Column, Integer, String, CHAR, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Calendar(Base):
    __tablename__ = 'calendar'
    id = Column(Integer, primary_key=True, autoincrement=True, comment="id")
    gubun = Column(CHAR(1), nullable=False, comment="종류")
    sorl = Column(CHAR(1), nullable=False, default='S', comment="S: Sun, L: Lunar")
    ymd = Column(String(8), nullable=True, comment="날짜")
    content = Column(String(100), nullable=False, comment="내용")
    modify_dt = Column(DateTime, nullable=False, default=func.current_timestamp(), comment="수정일시")
