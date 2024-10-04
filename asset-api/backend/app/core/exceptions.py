# exceptions.py
"""
모듈 설명: 
    - 예외 처리 모듈
주요 기능:
    - credentials_exception : JWT 토큰 검증 실패 예외
    - AssetApiException : AssetApi  예외 처리

작성자: 김도영
작성일: 2024-10-04
버전: 1.0
"""
from fastapi import HTTPException, status

# JWT 토큰 검증 실패 예외
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

class AssetApiException(Exception):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(self.detail)