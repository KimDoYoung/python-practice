from sqlalchemy import BigInteger, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from backend.app.core.database import metadata

Base = declarative_base(metadata=metadata)

class Ifi91ConfigApi(Base):
    __tablename__ = 'ifi91_config_api'

    ifi91_config_api_id = Column(BigInteger, primary_key=True, comment='API관리ID(PK)')
    ifi91_config_id = Column(BigInteger, nullable=False, comment='I/F설정정보ID')
    ifi91_service_type = Column(String(3), nullable=True, comment='서비스구분')
    ifi91_api_nm = Column(String(100), nullable=True, comment='API명')
    ifi91_path = Column(String(100), nullable=True, comment='Path')
    ifi91_http_method = Column(String(3), nullable=True, comment='HTTP Method')
    ifi91_format = Column(String(2), nullable=True, comment='Format')
    ifi91_content_type = Column(String(50), nullable=True, comment='Content-Type')
    ifi91_layout_cd = Column(String(10), nullable=True, comment='레이아웃코드')
    ifi91_api_tr_cd = Column(String(10), nullable=True, comment='거래코드')
    ifi91_note = Column(Text, nullable=True, comment='비고')
    ifi91_link_table = Column(String(100), nullable=True, comment='맵핑테이블')
    ifi91_use_yn = Column(String(5), nullable=True, comment='사용여부')
