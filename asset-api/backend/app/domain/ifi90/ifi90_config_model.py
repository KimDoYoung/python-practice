from sqlalchemy import Column, Numeric, String
from app.core.database import Base

class Ifi90Config(Base):
    __tablename__ = 'ifi90_config'

    ifi90_config_id = Column(Numeric, primary_key=True, comment='I/F설정정보ID(PK)')
    ifi90_if_cd = Column(String(50), nullable=True, comment='I/F코드')
    ifi90_if_nm = Column(String(100), nullable=True, comment='I/F명')
    ifi90_if_type = Column(String(2), nullable=True, comment='I/F방식(InterfaceType)')
    ifi90_local_ip = Column(String(50), nullable=True, comment='LOCAL IP')
    ifi90_local_port = Column(String(5), nullable=True, comment='LOCAL 포트')
    ifi90_local_account = Column(String(50), nullable=True, comment='LOCAL 계정ID')
    ifi90_local_pw = Column(String(128), nullable=True, comment='LOCAL 계정비밀번호')
    ifi90_local_path = Column(String(100), nullable=True, comment='LOCAL PATH')
    ifi90_local_key = Column(String(128), nullable=True, comment='LOCAL KEY')
    ifi90_target_ip = Column(String(50), nullable=True, comment='TARGET IP')
    ifi90_target_port = Column(String(5), nullable=True, comment='TARGET 포트')
    ifi90_target_account = Column(String(50), nullable=True, comment='TARGET 계정ID')
    ifi90_target_pw = Column(String(128), nullable=True, comment='TARGET 계정비밀번호')
    ifi90_target_path = Column(String(100), nullable=True, comment='TARGET PATH')
    ifi90_target_key = Column(String(128), nullable=True, comment='TARGET KEY')
    ifi90_note = Column(String(500), nullable=True, comment='비고')
