from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Essay(Base):
    __tablename__ = "essay"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="일련번호")
    title = Column(String(300), nullable=False, comment="제목")
    content = Column(Text, nullable=True, comment="내용")
    create_dt = Column(DateTime, default=func.now(), comment="최초생성일시")
    lastmodify_dt = Column(DateTime, nullable=True, comment="최종수정일시")
