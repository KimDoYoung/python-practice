from sqlalchemy import Column, Numeric, String, Text
from sqlalchemy.ext.declarative import declarative_base
from backend.app.core.database import metadata

Base = declarative_base(metadata=metadata)

class Ifi92ApiLayout(Base):
    __tablename__ = 'ifi92_api_layout'

    ifi92_api_layout_id = Column(Numeric, primary_key=True, comment='API레이아웃ID(PK)')
    ifi92_layout_cd = Column(String(10), nullable=False, comment='레이아웃코드')
    ifi92_message_cd = Column(String(3), nullable=True, comment='메세지구분')
    ifi92_seq = Column(Numeric, nullable=True, comment='순번')
    ifi92_component_cd = Column(String(2), nullable=True, comment='구성요소')
    ifi92_element_nm = Column(String(100), nullable=True, comment='Element')
    ifi92_element_knm = Column(String(100), nullable=True, comment='Element 한글명')
    ifi92_data_type = Column(String(10), nullable=True, comment='데이터타입')
    ifi92_required_yn = Column(String(5), nullable=True, comment='필수여부')
    ifi92_data_length = Column(Numeric, nullable=True, comment='데이터길이')
    ifi92_description = Column(Text, nullable=True, comment='Description')
    ifi92_note = Column(Text, nullable=True, comment='비고')
    ifi92_link_column = Column(String(200), nullable=True, comment='맵핑컬럼')
    ifi92_link_column_type = Column(String(10), nullable=True, comment='맵핑컬럼 데이터타입')
    ifi92_link_column_conv_cd = Column(String(50), nullable=True, comment='맵핑컬럼 변환코드')
