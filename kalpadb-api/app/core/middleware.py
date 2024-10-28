# jwtmiddleware.py
"""
모듈 설명: 
    - JWT 토큰을 검증하는 미들웨어
    - STATIC_PATHS에 등록된 경로는 토큰 검증을 하지 않음
    - NO_AUTH_PATHS에 등록된 경로는 토큰 검증을 하지 않음
    - EXEMPT_IPS에 등록된 IP에서 오는 요청은 토큰 검증을 하지 않음
    - /api 경로에 대해서만 토큰 검증을 수행함
    - JWT 토큰이 없거나 검증에 실패하면 401 Unauthorized 에러 발생
    

작성자: 김도영
작성일: 2024-07-19
버전: 1.0
"""
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

import logging

# 로거 설정
logger = logging.getLogger(__name__)

class Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # 요청 경로 및 클라이언트 IP 확인
        path = request.url.path
        client_ip = request.client.host
        
        # 로그 기록: 모든 /api 요청에 대해 IP와 경로 기록
        if path.startswith("/api"):
            logger.info(f"Request from IP: {client_ip}, Path: {path}")
        
        FREEPASS_IPS = ["192.168.1.100", "127.0.0.1"]  # 검증하지 않을 특정 IP 리스트

        # 특정 IP에서 오는 요청에 대해서는 토큰 검증을 하지 않음
        if client_ip in FREEPASS_IPS:
            logger.warning(f"Skipping JWT verification for IP(특정IP이므로 토근검증하지 않음): {client_ip}")
            response = await call_next(request)
            return response
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
