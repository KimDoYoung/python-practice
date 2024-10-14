from sqlalchemy import Column, Numeric, String
from app.core.database import Base

class Ifi10Law(Base):
    __tablename__ = 'ifi10_law'

    ifi10_law_id = Column(Numeric, primary_key=True, comment='법규정보ID(PK)')
    ifi10_law_cd = Column(String(10), nullable=True, comment='법규코드(ics01_class_tree_cd)')
    ifi10_law_nm = Column(String(200), nullable=True, comment='법규명')
    ifi10_relevant_law = Column(String(500), nullable=True, comment='근거법규')
    ifi10_submission = Column(String(500), nullable=True, comment='제출처(공시방법)')
    ifi10_cycle_type = Column(String(2), nullable=True, comment='정기/수시구분(10:정기, 20:수시)')
    ifi10_term_type = Column(String(2), nullable=True, comment='기간/날짜구분(10:기간, 20:날짜)')
