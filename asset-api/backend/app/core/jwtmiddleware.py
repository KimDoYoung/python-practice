# jwtmiddleware.py
"""
모듈 설명: 
    -  JWT 토큰을 검증하는 미들웨어
주요 기능:
    -  header에서 토큰 추출 확인

작성자: 김도영
작성일: 2024-07-19
버전: 1.0
"""
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from backend.app.core.security import verify_access_token

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = None
        
        # 요청 경로 확인
        path = request.url.path
        
        # "/main" 경로일 때는 리다이렉트 하지 않도록 예외 처리
        if path == "/main":
            return await call_next(request)
        
        # Authorization 헤더에서 토큰 추출
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[len("Bearer "):]

        try:
            if token:
                verify_access_token(token)
                response = await call_next(request)
            else:
                return RedirectResponse(url="/main")
        except HTTPException:
            return RedirectResponse(url="/main")
        
        return response