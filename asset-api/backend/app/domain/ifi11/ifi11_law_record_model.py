from sqlalchemy import Column, Numeric, String, DateTime, Date
from app.core.database import Base

class Ifi11LawRecord(Base):
    __tablename__ = 'ifi11_law_record'

    ifi11_law_record_id = Column(Numeric, primary_key=True, comment='법규정보ID(PK)')
    ifi11_dml_type = Column(String(6), nullable=True, comment='DML구분(INSERT/UPDATE/DELETE)')
    ifi11_dml_date = Column(Date, nullable=True, comment='변경일자')
    ifi11_dml_date_time = Column(DateTime, nullable=True, comment='변경일시')
    ifi11_ics_class_tree_id = Column(Numeric, nullable=True, comment='법규ID(ics01_class_tree_id)')
