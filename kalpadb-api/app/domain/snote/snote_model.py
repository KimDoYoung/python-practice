from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SNote(Base):
    __tablename__ = "snote"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    title = Column(String(200), nullable=True, comment="제목")
    note = Column(Text, nullable=True, comment="노트")
    create_dt = Column(TIMESTAMP, nullable=False, default=func.now(), comment="생성일시")
