from sqlalchemy import Column, String, Text
from app.core.database import metadata
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(metadata=metadata)

class Diary(Base):
    __tablename__ = 'dairy'
    
    ymd = Column(String(8), primary_key=True, comment='일자')  # varchar(8)
    content = Column(Text, nullable=True, comment='내용')  # text
    summary = Column(String(300), nullable=True, comment='요약')  # varchar(300)
