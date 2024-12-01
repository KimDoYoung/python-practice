from sqlalchemy import Column, Integer, String, Text, DateTime, CHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MovieReview(Base):
    __tablename__ = "movie_review"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="일련번호")
    title = Column(String(200), nullable=False, comment="제목")
    nara = Column(String(30), nullable=True, comment="제작국가")
    year = Column(CHAR(4), nullable=True, comment="제작년도")
    lvl = Column(Integer, nullable=True, comment="총평점수")
    ymd = Column(String(8), nullable=True, comment="본일자")
    content = Column(Text, nullable=True, comment="감상")
    lastmodify_dt = Column(DateTime, nullable=True, comment="최종수정일시")
