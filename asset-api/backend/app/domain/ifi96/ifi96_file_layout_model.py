from sqlalchemy import Column, Numeric, String, Text
from app.core.database import Base

class Ifi96FileLayout(Base):
    __tablename__ = 'ifi96_file_layout'

    ifi96_file_layout_id = Column(Numeric, primary_key=True, comment='파일레이아웃ID(PK)')
    ifi96_layout_cd = Column(String(10), nullable=False, comment='레이아웃코드')
    ifi96_seq = Column(Numeric, nullable=True, comment='순번')
    ifi96_element_nm = Column(String(100), nullable=True, comment='Element')
    ifi96_data_length = Column(Numeric, nullable=True, comment='데이터길이')
    ifi96_link_column = Column(String(200), nullable=True, comment='맵핑컬럼')
    ifi96_link_column_type = Column(String(10), nullable=True, comment='맵핑컬럼 데이터타입')
    ifi96_link_column_conv_cd = Column(String(50), nullable=True, comment='맵핑컬럼 변환코드')
    ifi96_required_yn = Column(String(5), nullable=True, comment='필수여부')
    ifi96_note = Column(Text, nullable=True, comment='비고')
