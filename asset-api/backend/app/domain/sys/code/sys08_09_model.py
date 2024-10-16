from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Sys08CodeKind 모델: 공통코드 종류를 정의하는 테이블
class Sys08CodeKind(Base):
    __tablename__ = 'sys08_code_kind'
    
    sys08_code_kind_id = Column(BigInteger, primary_key=True)  # 공통코드 종류 ID (기본키)
    sys08_kind_cd = Column(String(50), nullable=False)  # 공통코드 종류 코드
    sys08_kind_nm = Column(String(100), nullable=False)  # 공통코드 종류 명칭
    sys08_sys_yn = Column(String(10))  # 시스템 여부 (선택적 필드)
    sys08_note = Column(String(400))  # 비고 (선택적 필드)

# Sys09Code 모델: 공통코드를 정의하는 테이블
class Sys09Code(Base):
    __tablename__ = 'sys09_code'
    
    sys09_code_id = Column(BigInteger, primary_key=True)  # 공통코드 ID (기본키)
    sys09_code = Column(String(10), nullable=False)  # 공통코드
    sys09_name = Column(String(400), nullable=False)  # 공통코드명
    sys09_seq = Column(String(10))  # 순번 (선택적 필드)
    sys09_note = Column(String(1000))  # 비고 (선택적 필드)
    sys09_apply_date = Column(DateTime, nullable=False)  # 적용일
    sys09_close_yn = Column(String(10))  # 마감 여부 (선택적 필드)
    sys09_code_kind_id = Column(BigInteger, ForeignKey('sys08_code_kind.sys08_code_kind_id'), nullable=False)  # 공통코드 종류 ID (외래키)
    sys09_company_id = Column(BigInteger, ForeignKey('sys01_company.sys01_company_id'), nullable=False)  # 회사 ID (외래키)
    sys09_close_date = Column(DateTime)  # 마감일 (선택적 필드)

    company = relationship("Sys01Company", back_populates="codes")  # Sys01Company와의 관계 설정 (many-to-one)
    code_kind = relationship("Sys08CodeKind")  # Sys08CodeKind와의 관계 설정 (many-to-one)
