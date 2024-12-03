from sqlalchemy import Column, Integer, String, CHAR, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    content = Column(String(300), nullable=False, comment="내용")
    input_dt = Column(DateTime, default=func.now(), nullable=False, comment="입력일시")
    done_yn = Column(CHAR(1), default="N", nullable=False, comment="완료YN")
    done_dt = Column(DateTime, nullable=True, comment="완료일시")
