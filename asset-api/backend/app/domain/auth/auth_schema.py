# auth_schema.py
"""
모듈 설명: 
    - open api에 등록한 회사에게 jwt 토큰을 발급하는 모델

작성자: 김도영
작성일: 2024-10-10
버전: 1.0
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator

# jwt 토큰 발급 요청 시 사용하는 모델
class AuthRequest(BaseModel):
    app_key: str = Field(..., description="App key is required")
    app_secret_key: str = Field(..., description="App secret key is required")

    # app_key와 app_secret_key가 비어있는지 검증하는 validator 추가
    # Pydantic v2 스타일의 field_validator
    @field_validator('app_key', 'app_secret_key', mode='before')
    def not_empty(cls, v, field):
        if not v or v.strip() == '':
            raise ValueError(f'{field.name} cannot be empty')
        return v
    
class AuthResponse(BaseModel):
    company_id: int
    service_id: str
    start_ymd: str
    end_ymd:str
    token:str
