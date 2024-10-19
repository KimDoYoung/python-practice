from sqlalchemy import Column, Numeric, String, DateTime, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from backend.app.core.database import metadata

Base = declarative_base(metadata=metadata)

class Ifi11LawRecord(Base):
    __tablename__ = 'ifi11_law_record'

    ifi11_law_record_id = Column(Numeric, primary_key=True, comment='법규정보ID(PK)')
    ifi11_dml_type = Column(String(6), nullable=True, comment='DML구분(INSERT/UPDATE/DELETE)')
    ifi11_dml_date = Column(Date, nullable=True, comment='변경일자')
    ifi11_dml_date_time = Column(DateTime, nullable=True, comment='변경일시')
    ifi11_ics_class_tree_id = Column(Numeric, nullable=True, comment='법규ID(ics01_class_tree_id)')
    ifi11_deadline_id = Column(Numeric, nullable=True, comment='기한ID(sch03_deadline_id)')
    ifi11_class_tree_cd = Column(String(10), nullable=True, comment='법규코드')
    ifi11_class_tree_nm = Column(Text, nullable=True, comment='법규명')
    ifi11_related_law = Column(String(400), nullable=True, comment='관련법령')
    ifi11_submit_to = Column(String(200), nullable=True, comment='제출처')
    ifi11_content = Column(Text, nullable=True, comment='상세내용')
    ifi11_use_yn = Column(String(1), nullable=True, comment='사용여부')
    ifi11_deadline_nm = Column(String(200), nullable=True, comment='기한정보')
