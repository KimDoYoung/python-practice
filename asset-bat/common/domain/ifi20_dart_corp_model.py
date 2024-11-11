from sqlalchemy import Column, String, Numeric, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

# Base 클래스를 생성합니다.
Base = declarative_base()

class IFI20DartCorp(Base):
    __tablename__ = 'ifi20_dart_corp'
    
    # 테이블의 각 열을 SQLAlchemy 컬럼으로 정의
    ifi20_dart_corp_id = Column(Numeric, primary_key=True, nullable=False, comment="API요청데이터ID(PK)")
    ifi20_corp_cd = Column(String(8), nullable=True, comment="기관코드(DART고유번호)")
    ifi20_corp_nm = Column(String(100), nullable=True, comment="기관명")
    ifi20_stk_cd = Column(String(12), nullable=True, comment="종목코드")
    ifi20_modify_date = Column(String(8), nullable=True, comment="변경일자(DART자체)")
    ifi20_insert_time = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=True, comment="생성일시")
    
    def __repr__(self):
        return (f"<IFI20DartCorp(ifi20_dart_corp_id={self.ifi20_dart_corp_id}, "
                f"ifi20_corp_cd='{self.ifi20_corp_cd}', ifi20_corp_nm='{self.ifi20_corp_nm}', "
                f"ifi20_stk_cd='{self.ifi20_stk_cd}', ifi20_modify_date='{self.ifi20_modify_date}', "
                f"ifi20_insert_time={self.ifi20_insert_time})>")
