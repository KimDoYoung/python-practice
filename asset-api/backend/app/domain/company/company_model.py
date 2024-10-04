# company_model.py
"""
모듈 설명: 
    - ifi01_company 테이블의 모델 정의
    
작성자: 김도영
작성일: 2024-10-04
버전: 1.0
"""
from sqlalchemy import Column, BigInteger, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = "ifi01_company"

    company_id = Column(BigInteger, primary_key=True)
    service_nm = Column(String(100), primary_key=True)
    start_ymd = Column(String(8), nullable=False)
    end_ymd = Column(String(8), default='99991231', nullable=False)
    app_key = Column(String(64), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
