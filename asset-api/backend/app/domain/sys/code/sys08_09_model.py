from sqlalchemy import Column, String, BigInteger,  DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sys08CodeKind(Base):
    __tablename__ = 'sys08_code_kind'
    
    sys08_code_kind_id = Column(BigInteger, primary_key=True)
    sys08_kind_cd = Column(String(50), nullable=False)
    sys08_kind_nm = Column(String(100), nullable=False)
    sys08_sys_yn = Column(String(10))
    sys08_note = Column(String(400))


class Sys09Code(Base):
    __tablename__ = 'sys09_code'
    
    sys09_code_id = Column(BigInteger, primary_key=True)
    sys09_code = Column(String(10), nullable=False)
    sys09_name = Column(String(400), nullable=False)
    sys09_seq = Column(String(10))
    sys09_note = Column(String(1000))
    sys09_apply_date = Column(DateTime, nullable=False)
    sys09_close_yn = Column(String(10))
    sys09_code_kind_id = Column(BigInteger, ForeignKey('sys08_code_kind.sys08_code_kind_id'), nullable=False)
    sys09_company_id = Column(BigInteger, ForeignKey('sys01_company.sys01_company_id'), nullable=False)
    sys09_close_date = Column(DateTime)

    company = relationship("Sys01Company", back_populates="codes")
    code_kind = relationship("Sys08CodeKind")