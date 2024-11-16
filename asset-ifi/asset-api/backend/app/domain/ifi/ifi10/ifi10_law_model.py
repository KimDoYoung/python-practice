from sqlalchemy import Column, Numeric, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ifi10Law(Base):
    __tablename__ = 'ifi10_law'
    
    ifi10_law_id = Column(Numeric, primary_key=True, comment="법규정보ID(PK)")
    ifi10_law_cd = Column(String(10), nullable=True, comment="법규코드(ics01_class_tree_cd)")
    ifi10_law_nm = Column(String(200), nullable=True, comment="법규명")
    ifi10_relevant_law = Column(String(500), nullable=True, comment="근거법규")
    ifi10_submission = Column(String(500), nullable=True, comment="제출처(공시방법)")
    ifi10_cycle_type = Column(String(2), nullable=True, comment="정기/수시구분(10:정기, 20:수시)")
    ifi10_term_type = Column(String(2), nullable=True, comment="기간/날짜구분(10:기간, 20:날짜)")
    ifi10_interval_unit = Column(String(1), nullable=True, comment="주기구분(D:일, W:주, M:월, Q:분기, H:반기, Y:년, O:수시)")
    ifi10_std_date_type = Column(String(2), nullable=True, comment="기준일타입(10:말일, 20:트리거(이벤트))")
    ifi10_relative_position = Column(String(1), nullable=True, comment="이전/이후구분(A:이전(이내), B:이후)")
    ifi10_next_yn = Column(String(1), nullable=True, comment="익월/익일여부(Y/N)")
    ifi10_last_day_yn = Column(String(1), nullable=True, comment="말일여부(Y/N)")
    ifi10_value_month = Column(Numeric, nullable=True, comment="값_월")
    ifi10_value_week = Column(Numeric, nullable=True, comment="값_주")
    ifi10_value_weekday = Column(Numeric, nullable=True, comment="값_요일")
    ifi10_value_day = Column(Numeric, nullable=True, comment="값_일")
    ifi10_biz_calc_yn = Column(String(1), nullable=True, comment="영업일계산여부(Y/N)")
    ifi10_due_date_type = Column(String(2), nullable=True, comment="기한일처리(10:해당없음, 20:직후영업일, 30:직전영업일)")
    ifi10_start_date = Column(String(8), nullable=True, comment="적용시작일(YYYYMMDD)")
    ifi10_end_date = Column(String(8), nullable=True, comment="적용종료일(YYYYMMDD)")
    ifi10_deadline_nm = Column(String(200), nullable=True, comment="기한정보")
    ifi10_ics_class_tree_id = Column(Numeric, nullable=True, comment="법규ID(ics01_class_tree_id)")
    ifi10_deadline_id = Column(Numeric, nullable=True, comment="기한ID(sch03_deadline_id)")
