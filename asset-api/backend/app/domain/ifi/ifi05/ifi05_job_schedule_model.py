# models.py
from sqlalchemy import Column, Numeric, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ifi05JobSchedule(Base):
    __tablename__ = "ifi05_job_schedule"
    __table_args__ = {"schema": "public"}  # 스키마 설정
    
    # 컬럼 정의
    ifi05_job_schedule_id = Column(Numeric, primary_key=True, nullable=False, comment="작업스케줄 관리ID(PK)")
    ifi05_job_schedule_nm = Column(String(100), nullable=True, comment="스케줄명")
    ifi05_run_type = Column(String(10), nullable=True, comment="구분(cron)")
    ifi05_cron_str = Column(String(100), nullable=True, comment="cron 표현식")
    ifi05_description = Column(Text, nullable=True, comment="설명")
    ifi05_note = Column(Text, nullable=True, comment="비고")

    def __repr__(self):
        return (
            f"<Ifi05JobSchedule("
            f"id={self.ifi05_job_schedule_id}, "
            f"name={self.ifi05_job_schedule_nm}, "
            f"run_type={self.ifi05_run_type}, "
            f"cron_str={self.ifi05_cron_str})>"
        )
