# company_schema.py
"""
모듈 설명: 
    - company 도메인의 스키마를 정의하는 모듈
    - Pydantic을 사용하여 데이터 검증 및 타입 힌트를 제공   

작성자: 김도영
작성일: 2024-10-11
버전: 1.0
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

# 요청 시 사용하는 모델 (요청에 app_key와 app_secret_key는 포함되지 않음)
class CompanyRequest(BaseModel):
    company_id: int
    service_id: str = Field(..., max_length=100)
    start_ymd: str = Field(..., max_length=8)  # YYYYMMDD 형태로 받기
    end_ymd: Optional[str] = Field(default='99991231', max_length=8)

# 응답 시 사용하는 모델 (app_key와 app_secret_key 포함)
class CompanyResponse(CompanyRequest):
    app_key: Optional[str] = Field(None, max_length=64)
    app_secret_key: Optional[str] = Field(None, max_length=64)
    created_at: Optional[datetime] 
    # Pydantic v2 방식으로 변경
    class Config:
        from_attributes = True  # SQLAlchemy 모델을 Pydantic으로 변환 가능하게 설정    