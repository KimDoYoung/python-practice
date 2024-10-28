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
from backend.app.core.security import verify_access_token

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from backend.app.core.security import verify_access_token

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from backend.app.core.security import verify_access_token
import logging

# 로거 설정
logger = logging.getLogger(__name__)

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = None

        # 요청 경로 및 클라이언트 IP 확인
        path = request.url.path
        client_ip = request.client.host
        logger.debug("------------------------------------------------------------")
        logger.debug(f"Request from IP: {client_ip}, Path: {path}")
        logger.debug("------------------------------------------------------------")
        
        # 로그 기록: 모든 /api 요청에 대해 IP와 경로 기록
        # if path.startswith("/api"):
        #     logger.info(f"Request from IP: {client_ip}, Path: {path}")
        
        # 토큰 검증을 하지 않을 경로 목록 (정적 파일, 렌더링되는 HTML 페이지 등)
        STATIC_PATHS = ["/public", "/favicon.ico"]
        NO_AUTH_PATHS = ["/main", "/page", "/template"]  # JWT 검증을 하지 않는 페이지 경로
        FREEPASS_IPS = ["192.168.1.100", "127.0.0.1"]  # 검증하지 않을 특정 IP 리스트

        # 정적 파일 및 토큰 검증이 필요 없는 경로 처리
        if any(path.startswith(static_path) for static_path in STATIC_PATHS) or any(path.startswith(no_auth_path) for no_auth_path in NO_AUTH_PATHS):
            response = await call_next(request)
            return response
        
        # 특정 IP에서 오는 요청에 대해서는 토큰 검증을 하지 않음
        if client_ip in FREEPASS_IPS:
            logger.warning(f"Skipping JWT verification for IP(특정IP이므로 토근검증하지 않음): {client_ip}")
            response = await call_next(request)
            return response
        
        # /api 경로에 대해서만 토큰 검증 수행
        if path.startswith("/api"):
            # Authorization 헤더에서 토큰 추출
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header[len("Bearer "):]

            try:
                if token:
                    verify_access_token(token)  # 토큰 검증 수행
                    response = await call_next(request)
                    return response
                else:
                    # 토큰이 없으면 401 Unauthorized 에러 발생
                    raise HTTPException(status_code=401, detail="Authentication credentials were not provided")
            except HTTPException as e:
                # 토큰 검증에 실패하면 401 Unauthorized 에러 발생
                raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        # 토큰 검증을 하지 않는 경로 처리
        return await call_next(request)
