from sqlalchemy import BigInteger, Column, Date, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from backend.app.core.database import metadata

Base = declarative_base(metadata=metadata)


class Ifi01CompanyApi(Base):
    __tablename__ = 'ifi01_company_api'

    ifi01_company_api_id = Column(BigInteger, primary_key=True, comment='AssetAPI고객사정보ID(PK)')
    ifi01_company_id = Column(BigInteger, nullable=False, comment='회사ID(sys01_company_id)')
    ifi01_config_api_id = Column(BigInteger, nullable=False, comment='API관리ID(ifi91_config_api_id)')
    ifi01_start_date = Column(Date, nullable=True, comment='서비스 시작일자')
    ifi01_close_date = Column(Date, nullable=True, comment='서비스 종료일자')
    ifi01_app_key = Column(String(64), nullable=True, comment='랜덤으로 생성된 appKey (회사에 제공한 고유 키)')
    ifi01_created_date = Column(DateTime, nullable=True, comment='레코드 생성 일자')
