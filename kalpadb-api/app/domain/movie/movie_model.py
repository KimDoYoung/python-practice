from sqlalchemy import Column, Integer, String, CHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="ID")
    mid = Column(String(10), nullable=True, comment="영화 ID")
    gubun = Column(CHAR(1), nullable=False, comment="구분")
    title1 = Column(String(200), nullable=False, comment="제목(한글)")
    title2 = Column(String(200), nullable=True, comment="제목(영어)")
    title3 = Column(String(200), nullable=True, comment="제목(제작국 언어)")
    category = Column(String(100), nullable=True, comment="분야")
    gamdok = Column(String(100), nullable=True, comment="감독")
    make_year = Column(String(10), nullable=True, comment="제작년")
    nara = Column(String(50), nullable=True, comment="제작국적")
    dvd_id = Column(String(5), nullable=True, comment="DVD ID")
    title1num = Column(String(100), nullable=True, comment="검색문자열")
    title1title2 = Column(String(400), nullable=True, comment="검색어")
