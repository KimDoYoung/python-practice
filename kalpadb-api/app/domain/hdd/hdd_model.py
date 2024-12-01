from sqlalchemy import Column, Integer, String, CHAR, Double
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HDD(Base):
    __tablename__ = "hdd"

    id = Column(Integer, primary_key=True, autoincrement=False, comment="ID")
    volumn_name = Column(String(50), nullable=True, comment="볼륨 이름")
    gubun = Column(CHAR(1), nullable=False, comment="구분")
    path = Column(String(500), nullable=True, comment="경로")
    file_name = Column(String(300), nullable=True, comment="파일 이름")
    name = Column(String(300), nullable=False, comment="이름")
    pdir = Column(String(300), nullable=True, comment="상위 디렉터리")
    extension = Column(String(50), nullable=True, comment="확장자")
    size = Column(Double, nullable=True, comment="파일 크기")
    sha1_cd = Column(String(100), nullable=True, comment="SHA1 코드")
    srch_key = Column(String(300), nullable=True, comment="검색 키")
    last_modified_ymd = Column(String(20), nullable=True, comment="최종 수정일")
    pid = Column(Integer, nullable=True, comment="PID")
    right_pid = Column(Integer, nullable=True, comment="오른쪽 PID")
