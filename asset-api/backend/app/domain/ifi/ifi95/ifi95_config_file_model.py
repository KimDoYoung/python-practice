from sqlalchemy import Column, Numeric, String, Text
from sqlalchemy.ext.declarative import declarative_base
from backend.app.core.database import metadata

Base = declarative_base(metadata=metadata)

class Ifi95ConfigFile(Base):
    __tablename__ = 'ifi95_config_file'

    ifi95_config_file_id = Column(Numeric, primary_key=True, comment='파일송수신관리ID(PK)')
    ifi95_config_id = Column(Numeric, nullable=False, comment='I/F설정정보ID(ifi90_config_id)')
    ifi95_send_recv_type = Column(String(4), nullable=True, comment='송수신구분(SendRecvType-SEND,RECV)')
    ifi95_file_nm = Column(String(100), nullable=True, comment='파일명')
    ifi95_link_table = Column(String(100), nullable=True, comment='맵핑테이블')
    ifi95_separator_cd = Column(String(2), nullable=True, comment='데이터분리코드')
    ifi95_file_layout_cd = Column(String(100), nullable=True, comment='레이아웃코드')
    ifi95_shell = Column(String(500), nullable=True, comment='Shell Script')
    ifi95_note = Column(Text, nullable=True, comment='비고')
    ifi95_use_yn = Column(String(5), nullable=True, comment='사용여부')
